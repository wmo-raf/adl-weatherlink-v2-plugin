from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet

from .widgets import WeatherLinkStationSelectWidget


class WeatherLinkStationMapping(models.Model):
    station = models.OneToOneField("core.Station", on_delete=models.CASCADE, verbose_name=_("Station"),
                                   help_text=_("Station to link with ADCON"))
    weatherlink_station_id = models.PositiveIntegerField(verbose_name=_("WeatherLink Station ID"),
                                                         help_text=_("Select the WeatherLink Station ID"),
                                                         unique=True)
    last_imported = models.DateTimeField(verbose_name=_("Last Imported"), null=True, blank=True)

    panels = [
        FieldPanel('weatherlink_station_id', widget=WeatherLinkStationSelectWidget),
        FieldPanel('station'),
    ]

    class Meta:
        verbose_name = _("WeatherLink Station Link")
        verbose_name_plural = _("WeatherLink Stations Link")

    def __str__(self):
        return f"{self.station} - {self.weatherlink_station_id}"
