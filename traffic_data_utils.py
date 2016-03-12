import requests

key = '9e7af9db97e54776b410b2b3e61c6146'

def get_payload(coordinate):
    payload = {'key': key,
               'numTrips': '1',
               'originCoordLat': coordinate.get_latitude_as_str(),
               'originCoordLong': coordinate.get_longitude_as_str(),
               'originCoordName': 'Stockholm',
               'destId': '300109000',
               'date': '2016-03-15',
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
                    print 'has error code:', trip_list['errorCode']
                else:
                    trip_data = trip_list['Trip']
                    duration = get_duration_from_trip_data(trip_data)
                    print 'Duration was {} minutes'.format(duration)
        else:
            print '### Status was: {}'.format(request.status_code)
    return duration