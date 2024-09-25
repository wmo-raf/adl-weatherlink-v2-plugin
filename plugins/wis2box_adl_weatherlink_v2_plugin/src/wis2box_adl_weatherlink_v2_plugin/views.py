from django.shortcuts import render
from django.utils.translation import gettext
from wagtail_modeladmin.helpers import AdminURLHelper

from .models import WeatherLinkStationMapping


def wis2box_adl_weather_plugin_index(request):
    template_name = 'wis2box_adl_weatherlink_plugin/index.html'

    breadcrumbs_items = [
        {"url": "", "label": gettext("WeatherLink Plugin")},
    ]

    station_mapping_admin_helper = AdminURLHelper(WeatherLinkStationMapping)
    station_mapping_index_url = station_mapping_admin_helper.get_action_url("index")

    adcon_plugin_menu_items = [
        {
            "label": WeatherLinkStationMapping._meta.verbose_name_plural,
            "url": station_mapping_index_url,
            "icon_name": "snippet",
        }
    ]

    context = {
        "breadcrumbs_items": breadcrumbs_items,
        "menu_items": adcon_plugin_menu_items,
    }

    return render(request, template_name, context)
