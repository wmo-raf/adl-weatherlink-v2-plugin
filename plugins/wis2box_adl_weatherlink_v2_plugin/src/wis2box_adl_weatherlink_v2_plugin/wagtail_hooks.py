from django.urls import reverse, path
from django.utils.safestring import mark_safe
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail_modeladmin.helpers import PermissionHelper
from wagtail_modeladmin.options import ModelAdmin, modeladmin_register

from .models import WeatherLinkStationMapping
from .views import wis2box_adl_weather_plugin_index


@hooks.register('register_admin_urls')
def urlconf_wis2box_adl_weather_plugin():
    return [
        path('wis2box_adl_weatherlink_plugin/', wis2box_adl_weather_plugin_index,
             name='wis2box_adl_weatherlink_plugin_index'),
    ]


class WeatherLinkStationMappingPermissionHelper(PermissionHelper):
    def user_can_edit_obj(self, user, obj):
        return False


class WeatherLinkStationMappingAdmin(ModelAdmin):
    model = WeatherLinkStationMapping
    add_to_admin_menu = False
    permission_helper_class = WeatherLinkStationMappingPermissionHelper

    def __init__(self, parent=None):
        super().__init__(parent)
        self.list_display = (list(self.list_display) or []) + ["parameter_mapping"]

        self.parameter_mapping.__func__.short_description = _('Parameter Mapping')

    def parameter_mapping(self, obj):
        label = _("Parameter Mapping")

        url = "#"

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
