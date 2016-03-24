import requests
import time

from traffic_data_utils import get_duration_from_request, get_payload

URL = 'http://api.sl.se/api2/TravelplannerV2/trip.json'

def execute_request(latitude, longitude):
    response = None
    payload = get_payload(latitude, longitude)
    try:
        response = requests.get(URL, params=payload, timeout=10.0)
    except requests.exceptions.Timeout as err:
        print '### Timeout exception received:', err
        raise
    except requests.exceptions.ConnectionError as err:
        print '### Connection error:', err
        raise
    except Exception as err:
        print '### Other exception:', err
        raise
    return response

def handle_request(latitude, longitude):
    response = None
    print 'Requesting traffic data for coordinate:', latitude, longitude
    try:
        response = execute_request(latitude, longitude)
    except Exception as err:
        print 'Exception:', err
    time.sleep(1.2)
    return response



