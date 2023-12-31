from django.db import models
from django.core.validators import RegexValidator
from ..houses.models import House


# Create your models here.

class Producers(models.Model):
    name = models.CharField()
    active = models.BooleanField(default=False)
    website = models.URLField(blank=True,
                              null=True)
    comment = models.TextField(blank=True,
                               null=True)

    def __str__(self):
        return self.name



class Devices(models.Model):
    THERMAL_AND_HUMIDITY = 'tah'

    TYPES_CHOICES = (
        (THERMAL_AND_HUMIDITY, 'Thermal and Humidity'),
    )

    HTTP = 'http'

    PROTOCOL_CHOICES = (
        (HTTP, 'http'),
    )

    name = models.CharField()
    producer = models.ForeignKey(Producers,
                                 on_delete=models.CASCADE)
    api_url = models.URLField(null=True,
                              blank=True)
    type = models.CharField(choices=TYPES_CHOICES)
    house = models.ForeignKey(House,
                              on_delete=models.DO_NOTHING)

    active = models.BooleanField(default=True)

    ip_address = models.CharField(validators=[
        RegexValidator(r"^[0-9]+[0-9]?[0-9]?\.[0-9]+[0-9]?[0-9]?\.[0-9]+[0-9]?[0-9]?\.[0-9]+[0-9]?[0-9]?$",
                       "IP address should be numeric like '0.0.0.0'.")
    ])

    port = models.IntegerField()
    protocol = models.CharField(choices=PROTOCOL_CHOICES, default=HTTP)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('type',)


class BaseResult(models.Model):
    device = models.ForeignKey(Devices,
                               on_delete=models.CASCADE)

    created = models.DateTimeField()

    class Meta:
        abstract = True


class TempResults(BaseResult):
    temp_value = models.FloatField()

    heat_index = models.FloatField(null=True,
                                   blank=True)

    def __str__(self):
        return f"{self.device.name} at {self.created}"


class HumidityResults(BaseResult):
    humidity = models.FloatField()
    absolute_humidity = models.FloatField()

    def __str__(self):
        return f"{self.device.name} at {self.created}"
