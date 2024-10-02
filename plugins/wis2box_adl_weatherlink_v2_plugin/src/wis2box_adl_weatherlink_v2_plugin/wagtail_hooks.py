from django.urls import reverse, path
from django.utils.safestring import mark_safe
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail_modeladmin.helpers import PermissionHelper
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from .models import WeatherLinkStationMapping
from .views import (
    weatherlink_plugin_index,
    weatherlink_plugin_station_detail,
    weatherlink_plugin_station_data_structure_assign,
    weatherlink_station_parameter_mapping_list,
    weatherlink_station_parameter_mapping_delete,
    weatherlink_station_parameter_mapping_create,
)


@hooks.register('register_admin_urls')
def urlconf_wis2box_adl_weather_plugin():
    return [
        path('wis2box-adl-weatherlink-plugin/', weatherlink_plugin_index,
             name='wis2box_adl_weatherlink_plugin_index'),

        path('wis2box-adl-weatherlink-plugin/station-detail/<str:weatherlink_station_id>/',
             weatherlink_plugin_station_detail,
             name='wis2box_adl_weatherlink_plugin_station_detail'),

        path('wis2box-adl-weatherlink-plugin/data-structure/<str:station_mapping_id>/',
             weatherlink_plugin_station_data_structure_assign,
             name='weatherlink_plugin_station_data_structure_assign'),

        path('wis2box-adl-weatherlink-plugin/station_parameter_mapping/<int:station_mapping_id>/',
             weatherlink_station_parameter_mapping_list, name='weatherlink_station_parameter_mapping_list'),
        path('wis2box-adl-weatherlink-plugin/station_parameter_mapping/delete/<int:station_parameter_mapping_id>/',
             weatherlink_station_parameter_mapping_delete, name='weatherlink_station_parameter_mapping_delete'),
        path('wis2box-adl-weatherlink-plugin/station_parameter_mapping/<int:station_mapping_id>/create/',
             weatherlink_station_parameter_mapping_create,
             name='weatherlink_station_parameter_mapping_create'),
    ]


class WeatherLinkStationMappingPermissionHelper(PermissionHelper):
    def user_can_edit_obj(self, user, obj):
        return False


class WeatherLinkStationMappingAdmin(ModelAdmin):
    model = WeatherLinkStationMapping
    add_to_admin_menu = False
    permission_helper_class = WeatherLinkStationMappingPermissionHelper

    list_display = ["station", "station_detail", "subscription_type", "data_structure_assign"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.list_display = (list(self.list_display) or []) + ["parameter_mapping"]

        self.station_detail.__func__.short_description = _('Weather Station ID')
        self.parameter_mapping.__func__.short_description = _('Parameter Mapping')
        self.data_structure_assign.__func__.short_description = _('Data Structure')

    def station_detail(self, obj):
        weatherlink_station_id = obj.weatherlink_station_id
        url = reverse("wis2box_adl_weatherlink_plugin_station_detail", args=[weatherlink_station_id])

        button_html = f"""
            <a href="{url}">
              {weatherlink_station_id}
            </a>
        """
        return mark_safe(button_html)

    def data_structure_assign(self, obj):

        try:
            if not hasattr(obj, "data_structure_mapping") or not obj.data_structure_mapping.is_complete:
                label = _("Assign Data Structure")
            else:
                label = _("Edit Data Structure")
        except Exception as e:
            print(e)

        url = reverse("weatherlink_plugin_station_data_structure_assign", args=[obj.id])

        button_html = f"""
            <a href="{url}" class="button button-small button--icon bicolor button-secondary">
                <span class="icon-wrapper">
                    <svg class="icon icon-edit icon" aria-hidden="true">
                        <use href="#icon-edit"></use>
                    </svg>
                </span>
              {label}
            </a>
        """
        return mark_safe(button_html)

    def parameter_mapping(self, obj):
        if not obj.data_structure_mapping or not obj.data_structure_mapping.is_complete:
            return None

        label = _("Parameter Mapping")

        url = reverse("weatherlink_station_parameter_mapping_list", args=[obj.id])

        button_html = f"""
            <a href="{url}" class="button button-small button--icon bicolor">
                <span class="icon-wrapper">
                    <svg class="icon icon-list-ul icon" aria-hidden="true">
                        <use href="#icon-list-ul"></use>
                    </svg>
                </span>
              {label}
            </a>
        """
        return mark_safe(button_html)


modeladmin_register(WeatherLinkStationMappingAdmin)


@hooks.register("register_wis2box_adl_plugin_menu_items")
def register_wis2box_adl_menu_items():
    url = reverse("wis2box_adl_weatherlink_plugin_index")

    menu_items = [
        MenuItem(label=gettext("WeatherLink"), url=url, icon_name="cog", order=1000)
    ]

    return menu_items
