import datetime
import requests

from key import key

def get_business_date_as_str():
    business_date = datetime.date.today()
    delta = 1
    if business_date.weekday() in [4, 5, 6]: # Weekend
        delta = 3
    business_date = business_date + datetime.timedelta(delta)
    return str(business_date)

def get_payload(latitude, longitude):
    payload = {'key': key,
               'numTrips': '1',
               'originCoordLat': str(latitude),
               'originCoordLong': str(longitude),
               'originCoordName': 'Stockholm',
               'destId': '300109000',
               'date': get_business_date_as_str(),
               'time': '08:30',
               'searchForArrival': '1'}
    return payload

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

def get_duration_from_request(request):
    duration = None
    if request:
        if request.status_code == requests.codes.ok:
            try:
                json_data = request.json()
            except ValueError, e:
                print '### Error getting json: {}'.format(e)
            else:
                trip_list = json_data['TripList']
                if 'errorCode' in trip_list:
                    print 'Error code in trip list:', trip_list['errorCode']
                else:
                    trip_data = trip_list['Trip']
                    duration = get_duration_from_trip_data(trip_data)
                    print 'Duration was {} minutes'.format(duration)
        else:
            print '### Status was: {}'.format(request.status_code)
    return duration