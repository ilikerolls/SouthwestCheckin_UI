import pytest
import southwest
from checkin import CheckIN
from my_vcr import custom_vcr

my_vcr = custom_vcr()
r = southwest.Reservation('XXXXXX', 'John', 'Smith')


@my_vcr.use_cassette()
def test_generate_headers():
    headers = southwest.Reservation.generate_headers()
    assert(headers['Content-Type'] == 'application/json')
    assert(headers['X-API-Key'] == 'l7xx0a43088fe6254712b10787646d1b298e')


@my_vcr.use_cassette()
def test_reservation_lookup():
    try:
        r.lookup_existing_reservation()
    except Exception:
        pytest.fail("Error looking up reservation")


@my_vcr.use_cassette()
def test_checkin():
    try:
        data = r.checkin()
        assert data['flights'][0]['flightNumber'] == '1614'
    except Exception:
        pytest.fail("Error checking in. Error: ")


@my_vcr.use_cassette()
def test_checkin_without_passes():
    try:
        r.checkin()
    except Exception:
        pytest.fail("Error checking in")


@my_vcr.use_cassette()
def test_openflights_api():
    assert southwest.timezone_for_airport('LAX').zone == "America/Los_Angeles"


@my_vcr.use_cassette()
def test_cli():
    try:
        check_in = CheckIN('XXXXXX', 'John', 'Smith')
        check_in.auto_checkin()
    except Exception:
        pytest.fail("cli error")