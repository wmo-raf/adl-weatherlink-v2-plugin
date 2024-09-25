from wis2box_adl.core.registries import Plugin
from django.utils.translation import gettext_lazy as _


class WeatherLinkV2Plugin(Plugin):
    type = "wis2box_adl_weatherlink_v2_plugin"
    label = _("WeatherLink V2 Plugin")

    def get_urls(self):
        return []
