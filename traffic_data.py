import requests
import time
import pickle

from coordinate_generator import generate_coordinates

key = '9e7af9db97e54776b410b2b3e61c6146'

def get_payload(coordinate):
    payload = {'key': key,
               'numTrips': '1',
               'originCoordLat': coordinate.get_latitude_as_str(),
               'originCoordLong': coordinate.get_longitude_as_str(),
               'originCoordName': 'Stockholm',
               'destId': '300109000',
               'date': '2016-03-07',
               'time': '08:30',
               'searchForArrival': '1'}
    return payload

def execute_request(coordinate):
    payload = get_payload(coordinate)
    print 'Requesting for coordinate:', coordinate
    try:
        response = requests.get('http://api.sl.se/api2/TravelplannerV2/trip.json', params=payload, timeout=5.0)
    except requests.exceptions.Timeout as err:
        print '### Timeout exception received:', err
        response = None
    time.sleep(2)
    return response

def get_duration_from_trip_data(trip_data):
    duration = None
    if isinstance(trip_data, dict):
        duration = trip_data['dur']
    elif isinstance(trip_data, list):
        for leg in trip_data:
            leg_duration = leg['dur']
            if duration:
                if leg_duration < duration:
                    duration = leg_duration
            else:
                duration = leg_duration
    return str(duration)

def get_duration_from_request(r):
    duration = None
    if r:
        if r.status_code == requests.codes.ok:
            try:
                json_data = r.json()
            except ValueError, e:
                print '### Error getting json: {}'.format(e)
            else:
                trip_list = json_data['TripList']
                if 'errorCode' in trip_list:
                    print 'has error code:', trip_list['errorCode']
                else:
                    trip_data = trip_list['Trip']
                    duration = get_duration_from_trip_data(trip_data)
                    print 'Duration was {} minutes'.format(duration)
        else:
            print '### Status was: {}'.format(r.status_code)
    return duration

def write_updated_coordinates_to_file(coordinates):
    with open('coordinates_traffic_minutes.txt', 'wb') as handle:
        pickle.dump(coordinates, handle)

def write_traffic_data_to_file():
    coordinates = generate_coordinates()
    for coordinate in coordinates.coordinates():
        r = execute_request(coordinate)
        duration = get_duration_from_request(r)
        if duration:
            coordinate.set_duration(duration)
    write_updated_coordinates_to_file(coordinates)

write_traffic_data_to_file()
