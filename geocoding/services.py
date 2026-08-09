import requests
from django.conf import settings
from django.utils import timezone

from .models import Place
from .geocoder import fetch_coordinates


CACHE_LIFETIME = timezone.timedelta(days=30)


def get_or_create_place(address):
    place, created = Place.objects.get_or_create(address=address, defaults={'lat': 0, 'lon': 0})

    is_stale = not created and (timezone.now() - place.requested_at) > CACHE_LIFETIME

    if created or is_stale:
        try:
            coordinates = fetch_coordinates(settings.YANDEX_GEOCODER_API_KEY, address)
        except requests.exceptions.RequestException:
            coordinates = None

        if coordinates:
            place.lat, place.lon = coordinates
            place.save(update_fields=['lat', 'lon', 'requested_at'])
        elif created:
            place.delete()
            return None

    return place