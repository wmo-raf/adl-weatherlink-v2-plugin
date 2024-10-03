import os

from django.core.exceptions import ImproperlyConfigured


def setup(settings):
    """
    This function is called after wis2box_adl has setup its own Django settings file but
    before Django starts. Read and modify provided settings object as appropriate
    just like you would in a normal Django settings file. E.g.:

    settings.INSTALLED_APPS += ["some_custom_plugin_dep"]
    """

    WEATHERLINK_API_KEY = os.getenv('WEATHERLINK_API_KEY')
    WEATHERLINK_API_SECRET = os.getenv('WEATHERLINK_API_SECRET')

    if not WEATHERLINK_API_KEY:
        raise ImproperlyConfigured('WEATHERLINK_API_KEY environment variable is not set')

    if not WEATHERLINK_API_SECRET:
        raise ImproperlyConfigured('WEATHERLINK_API_SECRET environment variable is not set')

    settings.WEATHERLINK_API_KEY = WEATHERLINK_API_KEY
    settings.WEATHERLINK_API_SECRET = WEATHERLINK_API_SECRET

    # Add wagtail_modeladmin to the installed apps if it is not already there.
    if 'wagtail_modeladmin' not in settings.INSTALLED_APPS:
        settings.INSTALLED_APPS += ['wagtail_modeladmin']
