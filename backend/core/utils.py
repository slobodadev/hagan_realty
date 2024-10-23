from django.conf import settings
from geopy.geocoders import Nominatim
from enums import UsStateChoices


def get_state_by_point(point):
    if settings.TESTING:
        return "NY"

    geolocator = Nominatim(user_agent="factour_com")
    location = geolocator.reverse(f"{point.y}, {point.x}")

    if not location:
        return None

    address = location.raw.get("address")

    # get ISO3166-2-lvl4 from the address
    info = address.get("ISO3166-2-lvl4", None)
    if not info:
        return None

    state_code = info.split("-")[-1]
    if not state_code:
        return None

    # check if the state is valid
    if state_code not in dict(UsStateChoices.choices).keys():
        return None

    return state_code
