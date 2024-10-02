from django.core.paginator import Paginator, InvalidPage
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext
from wagtail.admin import messages
from wagtail.admin.ui.tables import Column, Table, ButtonsColumnMixin
from wagtail.admin.widgets import HeaderButton, ListingButton
from wagtail_modeladmin.helpers import AdminURLHelper, PermissionHelper

from .forms import WeatherLinkStationDataStructureForm, WeatherLinkParameterMappingForm
from .models import (
    WeatherLinkStationMapping,
    WeatherLinkStationDataStructureMapping,
    WeatherLinkStationParameterMapping
)


def weatherlink_plugin_index(request):
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


def weatherlink_plugin_station_detail(request, weatherlink_station_id):
    template_name = 'wis2box_adl_weatherlink_plugin/station_detail.html'

    station = WeatherLinkStationMapping.objects.get(weatherlink_station_id=weatherlink_station_id)

    station_mapping_admin_helper = AdminURLHelper(WeatherLinkStationMapping)
    station_mapping_index_url = station_mapping_admin_helper.get_action_url("index")

    breadcrumbs_items = [
        {
            "url": station_mapping_index_url,
            "label": gettext("WeatherLink Station Mapping"),
        },
        {"url": "", "label": gettext("Station Detail")},
    ]

    station_detail_fields = [
        {"label": gettext("Weather Station ID"), "value": station.weatherlink_station_id},
        {"label": gettext("Subscription Type"), "value": station.subscription_type},
        {"label": gettext("Recording Interval"), "value": station.recording_interval},
    ]

    context = {
        "breadcrumbs_items": breadcrumbs_items,
        "station": station,
        "station_detail_fields": station_detail_fields,
    }

    return render(request, template_name, context)


def weatherlink_plugin_station_data_structure_assign(request, station_mapping_id):
    template_name = "wis2box_adl_weatherlink_plugin/station_data_structure_assign.html"

    station_mapping = get_object_or_404(WeatherLinkStationMapping, pk=station_mapping_id)

    station_mapping_admin_helper = AdminURLHelper(WeatherLinkStationMapping)
    station_mapping_index_url = station_mapping_admin_helper.get_action_url("index")

    existing_data_structure_mapping = WeatherLinkStationDataStructureMapping.objects.filter(
        station_mapping=station_mapping)

    breadcrumbs_items = [
        {
            "url": "",
            "label": gettext("Assign Data Structure")},
    ]

    context = {
        "breadcrumbs_items": breadcrumbs_items,
        "header_icon": "snippet",
        "page_subtitle": gettext("Assign Data Structure"),
        "submit_button_label": gettext("Save"),
    }

    initial_data = {
        "station_mapping": station_mapping.id
    }

    if existing_data_structure_mapping.exists():
        initial_data[
            "current_conditions_data_structure_type"] = existing_data_structure_mapping.first().current_conditions_data_structure_type

    if request.method == "POST":
        form = WeatherLinkStationDataStructureForm(request.POST, initial=initial_data)

        if form.is_valid():
            data_structure_mapping_data = {
                "station_mapping": station_mapping,
            }

            if form.cleaned_data["current_conditions_data_structure_type"]:
                data_structure_mapping_data["current_conditions_data_structure_type"] = form.cleaned_data[
                    "current_conditions_data_structure_type"]
            else:
                data_structure_mapping_data["current_conditions_data_structure_type"] = None

            try:
                if existing_data_structure_mapping.exists():
                    existing_data_structure_mapping.update(**data_structure_mapping_data)
                else:
                    WeatherLinkStationDataStructureMapping.objects.create(**data_structure_mapping_data)

                messages.success(request, gettext("Station Data Structure Mapping assigned successfully."))

                return redirect(station_mapping_index_url)
            except Exception as e:
                form.add_error(None, e)
                context["form"] = form
                return render(request, template_name, context)
        else:
            context["form"] = form
            return render(request, template_name, context)

    form = WeatherLinkStationDataStructureForm(initial=initial_data)
    context["form"] = form

    return render(request, template_name, context)


def weatherlink_station_parameter_mapping_list(request, station_mapping_id):
    station_mapping = WeatherLinkStationMapping.objects.get(pk=station_mapping_id)

    queryset = WeatherLinkStationParameterMapping.objects.filter(
        data_structure_mapping=station_mapping.data_structure_mapping)

    station_mapping_admin_helper = AdminURLHelper(WeatherLinkStationMapping)
    station_mapping_index_url = station_mapping_admin_helper.get_action_url("index")

    breadcrumbs_items = [
        {"url": reverse("wis2box_adl_weatherlink_plugin_index"), "label": gettext("Weatherlink Plugin")},
        {"url": station_mapping_index_url, "label": WeatherLinkStationMapping._meta.verbose_name_plural},
        {"url": "", "label": gettext("WeatherLink Station Parameter Mapping")},
    ]

    # Get search parameters from the query string.
    try:
        page_num = int(request.GET.get("p", 0))
    except ValueError:
        page_num = 0

    user = request.user
    all_count = queryset.count()
    result_count = all_count
    paginator = Paginator(queryset, 20)

    try:
        page_obj = paginator.page(page_num + 1)
    except InvalidPage:
        page_obj = paginator.page(1)

    permission_helper = PermissionHelper(WeatherLinkStationParameterMapping)

    buttons = [
        HeaderButton(
            label=gettext('Add Weatherlink Station Parameter Mapping'),
            url=reverse("weatherlink_station_parameter_mapping_create", args=[station_mapping_id]),
            icon_name="plus",
        ),
    ]

    class ColumnWithButtons(ButtonsColumnMixin, Column):
        cell_template_name = "wagtailadmin/tables/title_cell.html"

        def get_buttons(self, instance, parent_context):
            delete_url = reverse("weatherlink_station_parameter_mapping_delete", args=[instance.id])
            return [
                ListingButton(
                    gettext("Delete"),
                    url=delete_url,
                    icon_name="bin",
                    priority=20,
                    classname="serious",
                ),
            ]

    columns = [
        Column("parameter", label=gettext("Parameter")),
        ColumnWithButtons("weatherlink_parameter", label=gettext("WeatherLink Parameter")),
    ]

    context = {
        "breadcrumbs_items": breadcrumbs_items,
        "all_count": all_count,
        "result_count": result_count,
        "paginator": paginator,
        "page_obj": page_obj,
        "object_list": page_obj.object_list,
        "user_can_create": permission_helper.user_can_create(user),
        "header_buttons": buttons,
        "table": Table(columns, page_obj.object_list),
    }

    return render(request, "wis2box_adl_weatherlink_plugin/station_parameter_mapping_list.html", context)


def weatherlink_station_parameter_mapping_create(request, station_mapping_id):
    template_name = "wis2box_adl_weatherlink_plugin/station_parameter_mapping_create.html"

    station_mapping_admin_helper = AdminURLHelper(WeatherLinkStationMapping)
    station_mapping_index_url = station_mapping_admin_helper.get_action_url("index")
    station_mapping = WeatherLinkStationMapping.objects.get(pk=station_mapping_id)

    breadcrumbs_items = [
        {
            "url": reverse("wis2box_adl_weatherlink_plugin_index"),
            "label": gettext("WeatherLink Plugin")},
        {

            "url": station_mapping_index_url,
            "label": WeatherLinkStationMapping._meta.verbose_name_plural},
        {
            "url": reverse("weatherlink_station_parameter_mapping_list", args=[station_mapping_id]),
            "label": gettext("WeatherLink Station Parameter Mapping")},
        {
            "url": "",
            "label": gettext("Create WeatherLink Station Parameter Mapping")},
    ]

    context = {
        "breadcrumbs_items": breadcrumbs_items,
        "header_icon": "snippet",
        "page_subtitle": gettext("Create WeatherLink Station Parameter Mapping"),
        "submit_button_label": gettext("Create"),
        "action_url": reverse("weatherlink_station_parameter_mapping_create", args=[station_mapping_id]),
    }

    if request.method == "POST":
        form = WeatherLinkParameterMappingForm(request.POST, initial={
            "data_structure_mapping": station_mapping.data_structure_mapping.id
        })

        if form.is_valid():
            station_parameter_mapping_data = {
                "data_structure_mapping": station_mapping.data_structure_mapping,
                "parameter": form.cleaned_data["parameter"],
                "weatherlink_parameter": form.cleaned_data["weatherlink_parameter"],
            }
            try:
                WeatherLinkStationParameterMapping.objects.create(**station_parameter_mapping_data)

                messages.success(request, gettext("WeatherLink Station Parameter Mapping created successfully."))

                return redirect(reverse("weatherlink_station_parameter_mapping_list", args=[station_mapping_id]))
            except Exception as e:

                form.add_error(None, e)
                context["form"] = form
                return render(request, template_name, context)
        else:
            context["form"] = form
            return render(request, template_name, context)
    else:
        form = WeatherLinkParameterMappingForm(
            initial={"data_structure_mapping": station_mapping.data_structure_mapping.id})
        context["form"] = form

    return render(request, template_name, context)


def weatherlink_station_parameter_mapping_delete(request, station_parameter_mapping_id):
    station_parameter_mapping = get_object_or_404(WeatherLinkStationParameterMapping, pk=station_parameter_mapping_id)

    if request.method == "POST":
        station_parameter_mapping.delete()
        messages.success(request, gettext("WeatherLink Station Parameter Mapping deleted successfully."))
        return redirect(
            reverse("weatherlink_station_parameter_mapping_list",
                    args=[station_parameter_mapping.data_structure_mapping.station_mapping.pk]))

    context = {
        "page_title": gettext("Delete %(obj)s") % {"obj": station_parameter_mapping},
        "header_icon": "snippet",
        "is_protected": False,
        "view": {
            "confirmation_message": gettext("Are you sure you want to delete this %(model_name)s?") % {
                "model_name": station_parameter_mapping._meta.verbose_name
            },
        },
    }

    return render(request, "wagtailadmin/generic/confirm_delete.html", context)
