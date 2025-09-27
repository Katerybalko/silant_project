from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Machine, Maintenance, Claim
from .filters import MachineFilter, MaintenanceFilter, ClaimFilter
from .serializers import MachineSerializer, MaintenanceSerializer, ClaimSerializer


# ==================
# HTML Views
# ==================

def welcome(request):
    """Приветственная страница (без входа)."""
    serial = request.GET.get("serial")
    machine = None
    if serial:
        machine = Machine.objects.filter(serial_number__iexact=serial).first()
    return render(request, "core/welcome.html", {"machine": machine})


@login_required
def dashboard(request):
    """Личный кабинет пользователя."""
    qs_m = Machine.objects.all()

    # Ограничение по ролям
    if request.user.groups.filter(name="client").exists():
        qs_m = qs_m.filter(client=request.user)
    elif request.user.groups.filter(name="service").exists():
        if hasattr(request.user, "profile") and request.user.profile.company_name:
            qs_m = qs_m.filter(service_company__name=request.user.profile.company_name)
        else:
            qs_m = Machine.objects.none()

    # Фильтры
    machines_filter = MachineFilter(request.GET or None, queryset=qs_m.order_by("-factory_ship_date"))
    machines = machines_filter.qs

    tos = MaintenanceFilter(request.GET or None, queryset=Maintenance.objects.filter(machine__in=qs_m).order_by("-date"))
    claims = ClaimFilter(request.GET or None, queryset=Claim.objects.filter(machine__in=qs_m).order_by("-failure_date"))

    tab = request.GET.get("tab", "machines")

    return render(
        request,
        "core/dashboard.html",
        {
            "machines": machines,
            "machines_filter": machines_filter,
            "tos": tos.qs,
            "claims": claims.qs,
            "tab": tab,
        },
    )


@login_required
def machine_detail(request, pk):
    """Детальная страница машины."""
    machine = get_object_or_404(Machine, pk=pk)

    # Проверка доступа client
    if request.user.groups.filter(name="client").exists() and machine.client != request.user:
        return HttpResponseForbidden("У вас нет доступа к этой машине")

    # Проверка доступа service
    if request.user.groups.filter(name="service").exists():
        if not hasattr(request.user, "profile") or request.user.profile.company_name != machine.service_company.name:
            return HttpResponseForbidden("У вас нет доступа к этой машине")

    return render(request, "core/machine_detail.html", {"machine": machine})


# ==================
# API Views
# ==================

class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all().order_by("-factory_ship_date")
    serializer_class = MachineSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all().order_by("-date")
    serializer_class = MaintenanceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ClaimViewSet(viewsets.ModelViewSet):
    queryset = Claim.objects.all().order_by("-failure_date")
    serializer_class = ClaimSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
