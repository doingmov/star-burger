from django.db import models


class Place(models.Model):
    address = models.CharField('адрес', max_length=200, unique=True)
    lat = models.FloatField('широта', blank=True, null=True)
    lon = models.FloatField('долгота', blank=True, null=True)
    requested_at = models.DateTimeField('дата запроса к геокодеру', auto_now=True)

    class Meta:
        verbose_name = 'место'
        verbose_name_plural = 'места'

    def __str__(self):
        return self.address