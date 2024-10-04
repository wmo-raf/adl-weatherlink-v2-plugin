import csv
import logging
from datetime import datetime, timezone
from io import StringIO

from django.core.files.base import ContentFile
from django.utils import timezone as dj_timezone
from django.utils.translation import gettext_lazy as _
from wis2box_adl.core.constants import WIS2BOX_CSV_HEADER
from wis2box_adl.core.models import DataIngestionRecord
from wis2box_adl.core.registries import Plugin
from wis2box_adl.core.units import units

from .models import WeatherLinkStationMapping

logger = logging.getLogger(__name__)


class WeatherLinkV2Plugin(Plugin):
    type = "wis2box_adl_weatherlink_v2_plugin"
    label = _("WeatherLink V2 Plugin")

    def get_urls(self):
        return []

    def get_data(self):
        logger.info("[WEATHERLINK_PLUGIN] Getting data from WeatherLink...")

        station_mappings = WeatherLinkStationMapping.objects.filter(
            data_structure_mapping__current_conditions_data_structure_type__isnull=False).distinct()

        ingestion_record_ids = []

        if station_mappings:
            count = station_mappings.count()

            logger.info(f"[WEATHERLINK_PLUGIN] Found {count} stations")

            for i, station_mapping in enumerate(station_mappings):
                station = station_mapping.station
                logger.info(f"[WEATHERLINK_PLUGIN] Getting data for station {station.name} ({i + 1}/{count})")

                parameter_mappings = station_mapping.data_structure_mapping.weatherlink_station_parameter_mappings.all()
                parameters_as_dict = {}
                for parameter_mapping in parameter_mappings:
                    parameters_as_dict[parameter_mapping.parameter.parameter] = {
                        "parameter": parameter_mapping.parameter,
                        "weatherlink_parameter": parameter_mapping.weatherlink_parameter,
                        "units_pint": parameter_mapping.units_pint
                    }

                weatherlink_data = station_mapping.get_current_conditions_data()

                if not weatherlink_data:
                    logger.warning(
                        f"[WEATHERLINK_PLUGIN] No data found for station {station.name}. "
                        f"Please check that the data structure and parameter mappings are set correctly.")

                for ts, params_data in weatherlink_data.items():
                    station_wis2box_csv_metadata = station.wis2box_csv_metadata

                    data_date_utc = datetime.fromtimestamp(ts).replace(tzinfo=timezone.utc)

                    date_info = {
                        "year": data_date_utc.year,
                        "month": data_date_utc.month,
                        "day": data_date_utc.day,
                        "hour": data_date_utc.hour,
                        "minute": data_date_utc.minute,
                    }

                    data_converted = {}

                    for key, value in params_data.items():
                        parameter = parameters_as_dict.get(key)

                        if parameter:
                            logger.info(f"[WEATHERLINK_PLUGIN] Converting units")

                            try:
                                units_pint = parameter.get("units_pint")
                                final_units = parameter.get("parameter").units_pint

                                # convert the value to the final units
                                quantity = value * units(units_pint)
                                value_converted = quantity.to(final_units).magnitude

                                data_converted[key] = value_converted

                                logger.info(f"[WEATHERLINK_PLUGIN] Converted {key} from {units_pint} to {final_units}")
                            except Exception as e:
                                logger.error(f"[WEATHERLINK_PLUGIN] Error converting units: "
                                             f"from {units_pint} to {final_units}. Error: {e}")
                                continue

                    data = {
                        **station_wis2box_csv_metadata,
                        **date_info,
                        **params_data
                    }

                    filename = f"WIGOS_{station.wigos_id}_{data_date_utc.strftime('%Y%m%dT%H%M%S')}.csv"

                    output = StringIO()
                    writer = csv.writer(output)
                    writer.writerow(WIS2BOX_CSV_HEADER)

                    row_data = []
                    for col in WIS2BOX_CSV_HEADER:
                        col_data = data.get(col, "")
                        row_data.append(col_data)

                    writer.writerow(row_data)
                    csv_content = output.getvalue()
                    output.close()

                    file = ContentFile(csv_content, filename)

                    # check if the data ingestion record already exists
                    ingestion_record = DataIngestionRecord.objects.filter(station=station, time=data_date_utc).first()

                    if ingestion_record:
                        # delete the old file
                        ingestion_record.file.delete()
                        ingestion_record.file = file
                    else:
                        ingestion_record = DataIngestionRecord.objects.create(station=station, time=data_date_utc,
                                                                              file=file)
                    ingestion_record.save()

                    last_imported = dj_timezone.localtime(station_mapping.last_imported, timezone=timezone.utc)

                    if data_date_utc > last_imported:
                        station_mapping.last_imported = data_date_utc
                        station_mapping.save()

                    ingestion_record_ids.append(ingestion_record.pk)

                    logger.info(f"[WEATHERLINK_PLUGIN] Data saved for station {station.name} at {data_date_utc}")

        logger.info("[WEATHERLINK_PLUGIN] Done getting data from WeatherLink")
        return ingestion_record_ids
