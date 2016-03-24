import time

from coordinate import Coordinate, CoordinateBox
from traffic_data import handle_request
from traffic_data_utils import get_duration_from_request

def set_traffic_data():
    for box in CoordinateBox.select():
        print 'Getting traffic for box', box
        center_coordinates = box.center_coordinates()
        for center_coordinate in center_coordinates:
            if not center_coordinate.minutes:
                request = handle_request(center_coordinate.latitude, center_coordinate.longitude)
                duration = get_duration_from_request(request)
                if duration:
                    center_coordinate.minutes = duration
                    center_coordinate.save()