import pickle

from coordinate import Coordinate

def get_coordinates_from_file():
    coordinates = None
    with open('coordinates_traffic_minutes.txt', 'rb') as input_file:
        coordinates = pickle.loads(input_file.read())
    return coordinates

def get_lat_lon_delta_from_coordinates(coordinates):
    lat_delta = coordinates.get_lat_delta()/2
    lon_delta = coordinates.get_lon_delta()/2
    return lat_delta, lon_delta

def write_coordinates_and_color_to_file(coordinates):
    lat_delta, lon_delta = get_lat_lon_delta_from_coordinates(coordinates)
    with open('coordinates_colored.txt', 'w') as output_file:
        for coordinate_obj in coordinates.coordinates():
            if coordinate_obj.has_duration():
                output_file.write('%s\n' % coordinate_obj.get_square_nw_as_str(lat_delta, lon_delta))
                output_file.write('%s\n' % coordinate_obj.get_square_sw_as_str(lat_delta, lon_delta))
                output_file.write('%s\n' % coordinate_obj.get_square_se_as_str(lat_delta, lon_delta))
                output_file.write('%s\n' % coordinate_obj.get_square_ne_as_str(lat_delta, lon_delta))
                output_file.write('%s\n' % coordinate_obj.get_color())

def create_colored_coordinates():
    coordinates = get_coordinates_from_file()
    write_coordinates_and_color_to_file(coordinates)
    print 'File written'

create_colored_coordinates()

''' Output file according to:
59.350000, 18.050000 # NW
59.340000, 18.050000 # SW
59.340000, 18.060000 # SE
59.350000, 18.060000 # NE
#193300
'''