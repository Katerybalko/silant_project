from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MachineViewSet, MaintenanceViewSet, ClaimViewSet, welcome, dashboard, machine_detail

router = DefaultRouter()
router.register(r'machines', MachineViewSet)
router.register(r'maintenances', MaintenanceViewSet)
router.register(r'claims', ClaimViewSet)

urlpatterns = [
    path("", welcome, name="welcome"),
    path("dashboard/", dashboard, name="dashboard"),
    path("machine/<int:pk>/", machine_detail, name="machine_detail"),
    path("api/", include(router.urls)),   # <-- вот эта строка для API
]
