import logging

from django.core.management import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Get Weatherlink data"

    def handle(self, *args, **options):
        from wis2box_adl.core.registries import plugin_registry
        logger.info('[WEATHERLINK_PLUGIN]: Getting Weatherlink data...')

        plugin = plugin_registry.get('wis2box_adl_weatherlink_v2_plugin')

        plugin.run_process()
