from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.


STATUSES = (
    ("started", "STARTED"),
    ("blocked", "BLOCKED"),
    ("stopped", "STOPPED"),
)

__VALIDATOR_STATUSES = (status[0] for status in STATUSES)


def validator_statuses(status) -> bool:
    if status in __VALIDATOR_STATUSES:
        return True


class VPS(models.Model):
    class Meta:
        verbose_name = "VPS"
        verbose_name_plural = "VPS"
        ordering = "id",

    uid = models.CharField(max_length=50, db_index=True, unique=True, blank=False, null=False)
    cpu = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(32)], blank=False,
                              null=False)
    ram = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(32)], blank=False,
                              null=False)
    hdd = models.IntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(2000)], blank=False,
                              null=False)
    status = models.CharField(default=STATUSES[0][0], validators=[validator_statuses], max_length=7, choices=STATUSES,
                              blank=False, null=False)
