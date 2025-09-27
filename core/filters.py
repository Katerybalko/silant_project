# core/filters.py
import django_filters
from .models import Machine, Maintenance, Claim, NamedDict

class MachineFilter(django_filters.FilterSet):
    model_tech = django_filters.ModelChoiceFilter(
        field_name="model_tech",
        queryset=NamedDict.objects.filter(dtype=NamedDict.DictType.MODEL_TECH)
    )
    model_engine = django_filters.ModelChoiceFilter(
        field_name="model_engine",
        queryset=NamedDict.objects.filter(dtype=NamedDict.DictType.MODEL_ENGINE)
    )
    model_trans = django_filters.ModelChoiceFilter(
        field_name="model_trans",
        queryset=NamedDict.objects.filter(dtype=NamedDict.DictType.MODEL_TRANS)
    )
    model_axle_steer = django_filters.ModelChoiceFilter(
        field_name="model_axle_steer",
        queryset=NamedDict.objects.filter(dtype=NamedDict.DictType.MODEL_AXLE_STEER)
    )
    model_axle_drive = django_filters.ModelChoiceFilter(
        field_name="model_axle_drive",
        queryset=NamedDict.objects.filter(dtype=NamedDict.DictType.MODEL_AXLE_DRIVE)
    )
    class Meta:
        model = Machine
        fields = ["model_tech","model_engine","model_trans","model_axle_steer","model_axle_drive"]

class MaintenanceFilter(django_filters.FilterSet):
    to_type = django_filters.ModelChoiceFilter(
        field_name="to_type",
        queryset=NamedDict.objects.filter(dtype=NamedDict.DictType.TO_TYPE)
    )
    machine__serial_number = django_filters.CharFilter(field_name="machine__serial_number", lookup_expr="icontains")
    service_company = django_filters.ModelChoiceFilter(
        field_name="service_company",
        queryset=NamedDict.objects.filter(dtype=NamedDict.DictType.SERVICE_COMPANY)
    )
    class Meta:
        model = Maintenance
        fields = ["to_type","machine__serial_number","service_company"]

class ClaimFilter(django_filters.FilterSet):
    failure_node = django_filters.ModelChoiceFilter(
        field_name="failure_node",
        queryset=NamedDict.objects.filter(dtype=NamedDict.DictType.FAILURE_NODE)
    )
    recovery_method = django_filters.ModelChoiceFilter(
        field_name="recovery_method",
        queryset=NamedDict.objects.filter(dtype=NamedDict.DictType.RECOVERY_METHOD)
    )
    service_company = django_filters.ModelChoiceFilter(
        field_name="service_company",
        queryset=NamedDict.objects.filter(dtype=NamedDict.DictType.SERVICE_COMPANY)
    )
    class Meta:
        model = Claim
        fields = ["failure_node","recovery_method","service_company"]
