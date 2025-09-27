from django.contrib import admin
from .models import NamedDict, Machine, Maintenance, Claim, Profile


# --- Inline ---
class MaintenanceInline(admin.TabularInline):
    model = Maintenance
    extra = 0
    show_change_link = True


class ClaimInline(admin.TabularInline):
    model = Claim
    extra = 0
    show_change_link = True


# --- Справочники ---
@admin.register(NamedDict)
class NamedDictAdmin(admin.ModelAdmin):
    list_display = ("dtype", "name", "description")
    list_filter = ("dtype",)
    search_fields = ("name", "description")
    ordering = ("dtype", "name")


# --- Профиль пользователя ---
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "company_name")
    search_fields = ("user__username", "company_name")
    ordering = ("user",)


# --- Машины ---
@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = (
        "serial_number",
        "model_tech",
        "model_engine",
        "factory_ship_date",
        "client",
        "service_company",
    )
    search_fields = (
        "serial_number",
        "engine_serial",
        "trans_serial",
        "axle_drive_serial",
        "axle_steer_serial",
        "consignee",
        "operation_address",
        "client__username",
    )
    list_filter = (
        "model_tech",
        "model_engine",
        "model_trans",
        "model_axle_drive",
        "model_axle_steer",
        "service_company",
    )
    date_hierarchy = "factory_ship_date"
    ordering = ("-factory_ship_date",)
    inlines = [MaintenanceInline, ClaimInline]


# --- ТО ---
@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ("machine", "to_type", "date", "uptime_mh", "org", "service_company")
    list_filter = ("to_type", "service_company", "org")
    search_fields = ("machine__serial_number", "order_no")
    date_hierarchy = "date"
    ordering = ("-date",)


# --- Рекламации ---
@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = (
        "machine",
        "failure_date",
        "failure_node",
        "recovery_method",
        "recovery_date",
        "downtime_hours",
        "service_company",
    )
    list_filter = ("failure_node", "recovery_method", "service_company")
    search_fields = ("machine__serial_number", "used_parts")
    date_hierarchy = "failure_date"
    ordering = ("-failure_date",)
