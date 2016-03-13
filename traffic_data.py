import requests
import time
import pickle

from coordinate_generator import generate_coordinates
from coordinate import ExceptionCoordinates
from traffic_data_utils import get_duration_from_request, get_payload

class CoordinateExceptionHandler(object):
    def __init__(self):
        self.exception_coordinates = ExceptionCoordinates()

    def handle_exception_for_coordinate(self, coordinate):
        self.exception_coordinates.add_coordinate(coordinate)

    def save_exception_coordinates(self, lat_delta, lon_delta):
        self.exception_coordinates.set_lat_delta(lat_delta)
        self.exception_coordinates.set_lon_delta(lon_delta)
        self.exception_coordinates.write_exception_coordinates_to_file()

class TrafficData(object):
    def __init__(self):
        self.coordinate_exception_handler = CoordinateExceptionHandler()

    def execute_request(self, coordinate):
        response = None
        payload = get_payload(coordinate)
        try:
            response = requests.get('http://api.sl.se/api2/TravelplannerV2/trip.json', params=payload, timeout=10.0)
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

    def handle_request(self, coordinate):
        response = None
        print 'Requesting for coordinate:', coordinate
        try:
            response = self.execute_request(coordinate)
        except Exception as err:
            self.coordinate_exception_handler.handle_exception_for_coordinate(coordinate)
        time.sleep(3)
        return response

    def write_updated_coordinates_to_file(self, coordinates):
        with open('coordinates_traffic_minutes.txt', 'wb') as handle:
            pickle.dump(coordinates, handle)

    def get_traffic_data(self):
        self.coordinates = generate_coordinates()
        for coordinate in self.coordinates.coordinates():
            request = self.handle_request(coordinate)
            duration = get_duration_from_request(request)
            if duration:
                coordinate.set_duration(duration)
        self.write_updated_coordinates_to_file(self.coordinates)
        self.coordinate_exception_handler.save_exception_coordinates(self.coordinates.get_lat_delta(),
                                                                     self.coordinates.get_lon_delta())

trafficData = TrafficData()
trafficData.get_traffic_data()

def x():
    from coordinate import Coordinates, Coordinate
    with open('coordinates_exception.txt', 'rb') as input_file:
        coordinates = pickle.loads(input_file.read())
        for coord in coordinates.coordinates():
            print 'coord', coord
        print coordinates.get_lat_delta()
        print coordinates.get_lon_delta()

#x()