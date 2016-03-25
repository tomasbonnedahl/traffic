import time

from coordinate import Coordinate, CoordinateBox
from traffic_data import handle_request
from traffic_data_utils import get_duration_from_request

def should_request_traffic_data(coordinate, include_exception_coordinates):
    should_request = False
    if not coordinate.minutes:
        if not coordinate.exception or (coordinate.exception and include_exception_coordinates):
            should_request = True
    return should_request

def set_traffic_data(include_exception_coordinates = False):
    for box in CoordinateBox.select():
        print 'Getting traffic for box', box
        center_coordinates = box.center_coordinates()
        for center_coordinate in center_coordinates:
            if should_request_traffic_data(center_coordinate, include_exception_coordinates):
                request = handle_request(center_coordinate.latitude, center_coordinate.longitude)
                duration = get_duration_from_request(request)
                if duration:
                    center_coordinate.minutes = duration
                else:
                    center_coordinate.exception = True
                center_coordinate.save()