from django.apps import AppConfig

from wis2box_adl.core.registries import plugin_registry


class WeatherLinkV2PluginConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "wis2box_adl_weatherlink_v2_plugin"

    def ready(self):
        from .plugins import WeatherLinkV2Plugin

        plugin_registry.register(WeatherLinkV2Plugin())
