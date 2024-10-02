from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet

from .http import weatherlink_api
from .widgets import WeatherLinkStationSelectWidget


class WeatherLinkStationMapping(models.Model):
    weatherlink_station_id = models.PositiveIntegerField(verbose_name=_("WeatherLink Station ID"),
                                                         help_text=_("Select the WeatherLink Station ID"),
                                                         unique=True)
    station = models.OneToOneField("core.Station", on_delete=models.CASCADE, verbose_name=_("Station"),
                                   help_text=_("Station to link"))
    last_imported = models.DateTimeField(verbose_name=_("Last Imported"), null=True, blank=True)

    panels = [
        FieldPanel('weatherlink_station_id', widget=WeatherLinkStationSelectWidget),
        FieldPanel('station'),
    ]

    class Meta:
        verbose_name = _("WeatherLink Station Link")
        verbose_name_plural = _("WeatherLink Stations Link")

    @property
    def station_info(self):
        return weatherlink_api.get_station(self.weatherlink_station_id)

    @property
    def subscription_type(self):
        station_info = self.station_info

        if station_info is None:
            return None

        return station_info.get("subscription_type")

    @property
    def recording_interval(self):
        station_info = self.station_info

        if station_info is None:
            return None

        return station_info.get("recording_interval")

    @property
    def sensor_catalog(self):
        catalog = weatherlink_api.get_sensor_catalog_for_station(self.weatherlink_station_id)

        return catalog

    @cached_property
    def data_structure_parameters(self):
        sensor_catalog = self.sensor_catalog
        data_structure_parameters = {}
        for entry in sensor_catalog:
            if entry.get("data_structures"):
                data_structures = entry["data_structures"]
                for ds in data_structures:
                    data_structure = ds.get("data_structure")
                    data_structure_parameters[ds.get("data_structure_type")] = data_structure

        return data_structure_parameters

    def get_current_conditions_data(self):
        data_structure_mapping = self.data_structure_mapping

        if not data_structure_mapping or not data_structure_mapping.is_complete:
            return None

        db_sensor_type = data_structure_mapping.sensor_type
        db_data_structure_type = data_structure_mapping.data_structure_type

        data = weatherlink_api.get_current_conditions(self.weatherlink_station_id)

        data_for_structure = {}

        for sensor_data in data.get("sensors"):
            sensor_type = str(sensor_data.get("sensor_type"))
            data_structure_type = str(sensor_data.get("data_structure_type"))

            # Compare the sensor type and data structure type with the database values
            if sensor_type == db_sensor_type and data_structure_type == db_data_structure_type:
                data_for_structure = sensor_data.get("data")[0]
                # Found the data for the structure,
                break

        parameters = data_structure_mapping.weatherlink_station_parameter_mappings.all()
        mapped_data = {}

        # Map the data to the parameters
        if data_for_structure:
            ts = data_for_structure.get("ts")
            mapped_data[ts] = {}
            for parameter in parameters:
                parameter_name = parameter.parameter.parameter
                weatherlink_parameter = parameter.weatherlink_parameter

                if weatherlink_parameter in data_for_structure:
                    mapped_data[ts].update({
                        parameter_name: data_for_structure[weatherlink_parameter]
                    })

            # Remove the data if it is empty
            if not mapped_data[ts]:
                mapped_data.pop(ts)

        return mapped_data

    def __str__(self):
        return f"{self.station}"


class WeatherLinkStationDataStructureMapping(models.Model):
    station_mapping = models.OneToOneField(WeatherLinkStationMapping, on_delete=models.CASCADE,
                                           verbose_name=_("Station Mapping"), related_name="data_structure_mapping")
    current_conditions_data_structure_type = models.CharField(blank=True, null=True)

    def __str__(self):
        return f"{self.station_mapping}"

    @property
    def ds_types_parts(self):
        if self.current_conditions_data_structure_type:
            parts = self.current_conditions_data_structure_type.split("_")
            return parts

    @property
    def sensor_type(self):
        if self.ds_types_parts:
            return self.ds_types_parts[0]
        return None

    @property
    def data_structure_type(self):
        if self.ds_types_parts:
            return self.ds_types_parts[1]
        return None

    @property
    def is_complete(self):
        return self.current_conditions_data_structure_type is not None


@register_snippet
class WeatherLinkStationParameterMapping(models.Model):
    data_structure_mapping = models.ForeignKey(WeatherLinkStationDataStructureMapping, on_delete=models.CASCADE,
                                               verbose_name=_("Station Mapping"),
                                               related_name="weatherlink_station_parameter_mappings")
    parameter = models.ForeignKey("core.DataParameter", on_delete=models.CASCADE, verbose_name=_("Parameter"))
    weatherlink_parameter = models.CharField(max_length=255, verbose_name=_("WeatherLink Parameter"))

    class Meta:
        verbose_name = _("WeatherLink Station Parameter Mapping")
        verbose_name_plural = _("WeatherLink Station Parameter Mapping")
        constraints = [
            models.UniqueConstraint(fields=['data_structure_mapping', 'parameter'],
                                    name='unique_weatherlink_station_mapping_parameter')
        ]

    def __str__(self):
        return f"{self.data_structure_mapping} - {self.parameter}"
