from django import forms
from wagtail.admin.forms import WagtailAdminModelForm

from .models import (
    WeatherLinkStationMapping,
    WeatherLinkStationParameterMapping,
    WeatherLinkStationDataStructureMapping
)
from .constants import CURRENT_CONDITIONS_DATA_STRUCTURES


class WeatherLinkParameterMappingForm(WagtailAdminModelForm):
    data_structure_mapping = forms.ModelChoiceField(queryset=WeatherLinkStationDataStructureMapping.objects.all(),
                                                    widget=forms.HiddenInput())
    weatherlink_parameter = forms.ChoiceField(choices=[])

    class Meta:
        model = WeatherLinkStationParameterMapping
        fields = ["parameter", "weatherlink_parameter"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        initial = kwargs.get("initial", {})
        data_structure_mapping_id = initial.get("data_structure_mapping")

        data_structure_mapping = WeatherLinkStationDataStructureMapping.objects.get(id=data_structure_mapping_id)

        existing_parameters = WeatherLinkStationParameterMapping.objects.filter(
            data_structure_mapping_id=data_structure_mapping_id)
        existing_weatherlink_parameters = [parameter.weatherlink_parameter for parameter in existing_parameters]

        current_conditions_data_structure_type = data_structure_mapping.data_structure_type

        parameters = data_structure_mapping.station_mapping.data_structure_parameters.get(
            str(current_conditions_data_structure_type))

        parameter_key_label = []
        for key, value in parameters.items():
            parameter_key_label.append({"key": key, "label": f"{key} - ({value.get('units')})"})

        parameter_choices = [parameter for parameter in parameter_key_label if
                             parameter.get("key") not in existing_weatherlink_parameters]

        existing_parameters_ids = [parameter.parameter_id for parameter in existing_parameters]

        # Filter out parameters that are already mapped
        self.fields["parameter"].queryset = self.fields["parameter"].queryset.exclude(id__in=existing_parameters_ids)

        empty_choice = [("", "---------")]
        self.fields["weatherlink_parameter"].choices = empty_choice + [(parameter.get("key"), parameter.get("label"))
                                                                       for parameter in
                                                                       parameter_choices]


class WeatherLinkStationDataStructureForm(WagtailAdminModelForm):
    station_mapping = forms.ModelChoiceField(queryset=WeatherLinkStationMapping.objects.all(),
                                             widget=forms.HiddenInput())
    current_conditions_data_structure_type = forms.ChoiceField(choices=[], required=False)

    class Meta:
        model = WeatherLinkStationDataStructureMapping
        fields = ["current_conditions_data_structure_type"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        initial = kwargs.get("initial", {})
        station_mapping_id = initial.get("station_mapping")

        station_mapping = WeatherLinkStationMapping.objects.get(id=station_mapping_id)

        data_structure_types = [
            ("", "---------")
        ]

        for entry in station_mapping.sensor_catalog:
            if entry.get("data_structures"):
                sensor_type = entry["sensor_type"]
                data_structures = entry["data_structures"]
                for data_structure in data_structures:
                    data_structure_type = data_structure.get("data_structure_type")

                    if data_structure_type in CURRENT_CONDITIONS_DATA_STRUCTURES:
                        value = f"{sensor_type}_{data_structure_type}"
                        label = f"Sensory Type: {sensor_type} -  {data_structure['description']} - DS Type: {data_structure_type}"
                        data_structure_types.append((value, label))

        self.fields["current_conditions_data_structure_type"].choices = data_structure_types
