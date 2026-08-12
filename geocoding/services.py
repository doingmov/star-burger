import requests
from django.conf import settings
from django.utils import timezone

from .models import Place
from .geocoder import fetch_coordinates


CACHE_LIFETIME = timezone.timedelta(days=30)


def _is_stale(place):
    return place.lat is not None and (timezone.now() - place.requested_at) > CACHE_LIFETIME


def get_coordinates_for_addresses(addresses):
    addresses = set(addresses)

    existing_places = {
        place.address: place
        for place in Place.objects.filter(address__in=addresses)
    }

    coordinates_by_address = {}
    places_to_create = []

    for address in addresses:
        place = existing_places.get(address)

        if place and place.lat is not None and not _is_stale(place):
            coordinates_by_address[address] = (place.lat, place.lon)
            continue

        try:
            coordinates = fetch_coordinates(settings.YANDEX_GEOCODER_API_KEY, address)
        except requests.exceptions.RequestException:
            coordinates = None

        coordinates_by_address[address] = coordinates

        if place:
            if coordinates:
                place.lat, place.lon = coordinates
                place.save(update_fields=['lat', 'lon', 'requested_at'])
        else:
            lat, lon = coordinates if coordinates else (None, None)
            places_to_create.append(Place(address=address, lat=lat, lon=lon))

    if places_to_create:
        Place.objects.bulk_create(places_to_create)

    return coordinates_by_address