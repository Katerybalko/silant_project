from django.contrib.auth.models import User
from django.db import models


# --- Справочники ---
class NamedDict(models.Model):
    """Универсальный справочник: тип + название + описание."""
    class DictType(models.TextChoices):
        MODEL_TECH = "model_tech", "Модель техники"
        MODEL_ENGINE = "model_engine", "Модель двигателя"
        MODEL_TRANS = "model_trans", "Модель трансмиссии"
        MODEL_AXLE_DRIVE = "model_axle_drive", "Модель ведущего моста"
        MODEL_AXLE_STEER = "model_axle_steer", "Модель управляемого моста"
        TO_TYPE = "to_type", "Вид ТО"
        FAILURE_NODE = "failure_node", "Узел отказа"
        RECOVERY_METHOD = "recovery_method", "Способ восстановления"
        SERVICE_COMPANY = "service_company", "Сервисная компания"  # по ТЗ как справочник

    dtype = models.CharField(max_length=40, choices=DictType.choices)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        indexes = [models.Index(fields=["dtype", "name"])]
        unique_together = (("dtype", "name"),)
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"

    def __str__(self):
        return f"{self.get_dtype_display()}: {self.name}"


# Профили для ролей (клиент/сервисная организация)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.get_username()


# --- Машина ---
class Machine(models.Model):
    serial_number = models.CharField("Зав. № машины", max_length=128, unique=True)

    model_tech = models.ForeignKey(
        NamedDict, on_delete=models.PROTECT,
        limit_choices_to={"dtype": NamedDict.DictType.MODEL_TECH},
        related_name="machines_as_tech",
        verbose_name="Модель техники"
    )
    model_engine = models.ForeignKey(
        NamedDict, on_delete=models.PROTECT,
        limit_choices_to={"dtype": NamedDict.DictType.MODEL_ENGINE},
        related_name="machines_as_engine",
        verbose_name="Модель двигателя"
    )
    engine_serial = models.CharField("Зав. № двигателя", max_length=128)

    model_trans = models.ForeignKey(
        NamedDict, on_delete=models.PROTECT,
        limit_choices_to={"dtype": NamedDict.DictType.MODEL_TRANS},
        related_name="machines_as_trans",
        verbose_name="Модель трансмиссии"
    )
    trans_serial = models.CharField("Зав. № трансмиссии", max_length=128)

    model_axle_drive = models.ForeignKey(
        NamedDict, on_delete=models.PROTECT,
        limit_choices_to={"dtype": NamedDict.DictType.MODEL_AXLE_DRIVE},
        related_name="machines_as_drive_axle",
        verbose_name="Модель ведущего моста"
    )
    axle_drive_serial = models.CharField("Зав. № ведущего моста", max_length=128)

    model_axle_steer = models.ForeignKey(
        NamedDict, on_delete=models.PROTECT,
        limit_choices_to={"dtype": NamedDict.DictType.MODEL_AXLE_STEER},
        related_name="machines_as_steer_axle",
        verbose_name="Модель управляемого моста"
    )
    axle_steer_serial = models.CharField("Зав. № управляемого моста", max_length=128)

    supply_contract = models.CharField("Договор поставки №, дата", max_length=255, blank=True)
    factory_ship_date = models.DateField("Дата отгрузки с завода")
    consignee = models.CharField("Грузополучатель (конечный потребитель)", max_length=255, blank=True)
    operation_address = models.CharField("Адрес поставки (эксплуатации)", max_length=255, blank=True)
    options = models.TextField("Комплектация (доп. опции)", blank=True)

    # Привязки по правам
    client = models.ForeignKey(
        User, on_delete=models.PROTECT,
        related_name="machines_as_client",
        verbose_name="Клиент"
    )
    service_company = models.ForeignKey(
        NamedDict, on_delete=models.PROTECT,
        limit_choices_to={"dtype": NamedDict.DictType.SERVICE_COMPANY},
        related_name="machines_as_service_company",
        verbose_name="Сервисная компания"
    )

    class Meta:
        ordering = ["-factory_ship_date"]  # сортировка по умолчанию по ТЗ
        verbose_name = "Машина"
        verbose_name_plural = "Машины"

    def __str__(self):
        return f"{self.serial_number}"


# --- ТО ---
class Maintenance(models.Model):
    to_type = models.ForeignKey(
        NamedDict, on_delete=models.PROTECT,
        limit_choices_to={"dtype": NamedDict.DictType.TO_TYPE},
        related_name="maintenances_as_type",
        verbose_name="Вид ТО"
    )
    date = models.DateField("Дата проведения ТО")
    uptime_mh = models.PositiveIntegerField("Наработка, м/час")
    order_no = models.CharField("№ заказ-наряда", max_length=128, blank=True)
    order_date = models.DateField("Дата заказ-наряда", null=True, blank=True)

    org = models.ForeignKey(
        NamedDict, on_delete=models.PROTECT,
        limit_choices_to={"dtype": NamedDict.DictType.SERVICE_COMPANY},
        related_name="maintenances_as_org",
        verbose_name="Организация, проводившая ТО"
    )
    machine = models.ForeignKey(
        Machine, on_delete=models.CASCADE,
        related_name="maintenances"
    )
    service_company = models.ForeignKey(
        NamedDict, on_delete=models.PROTECT,
        limit_choices_to={"dtype": NamedDict.DictType.SERVICE_COMPANY},
        related_name="maintenances_as_service",
        verbose_name="Сервисная компания"
    )

    class Meta:
        ordering = ["-date"]
        verbose_name = "ТО"
        verbose_name_plural = "ТО"


# --- Рекламация ---
class Claim(models.Model):
    failure_date = models.DateField("Дата отказа")
    uptime_mh = models.PositiveIntegerField("Наработка, м/час")

    failure_node = models.ForeignKey(
        NamedDict, on_delete=models.PROTECT,
        limit_choices_to={"dtype": NamedDict.DictType.FAILURE_NODE},
        related_name="claims_as_failure_node",
        verbose_name="Узел отказа"
    )
    failure_desc = models.TextField("Описание отказа", blank=True)

    recovery_method = models.ForeignKey(
        NamedDict, on_delete=models.PROTECT,
        limit_choices_to={"dtype": NamedDict.DictType.RECOVERY_METHOD},
        related_name="claims_as_recovery_method",
        verbose_name="Способ восстановления"
    )
    used_parts = models.TextField("Используемые запасные части", blank=True)

    recovery_date = models.DateField("Дата восстановления")
    downtime_hours = models.IntegerField("Время простоя техники", editable=False)

    machine = models.ForeignKey(
        Machine, on_delete=models.CASCADE,
        related_name="claims"
    )
    service_company = models.ForeignKey(
        NamedDict, on_delete=models.PROTECT,
        limit_choices_to={"dtype": NamedDict.DictType.SERVICE_COMPANY},
        related_name="claims_as_service",
        verbose_name="Сервисная компания"
    )

    def save(self, *args, **kwargs):
        if self.recovery_date and self.failure_date:
            self.downtime_hours = (self.recovery_date - self.failure_date).days * 24
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-failure_date"]
        verbose_name = "Рекламация"
        verbose_name_plural = "Рекламации"
