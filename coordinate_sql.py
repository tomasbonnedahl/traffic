from random import randint

from coordinate import Coordinate, CoordinateBox
from coordinate_generator import RawCoordinateGenerator
from coordinate_utils import calculate_step_size

def create_boxes_and_coordinates(south_in, north_in, west_in, east_in, num_boxes_in_dir, num_coords_in_dir):
    print '-- SAVE --'
    box_size_south_north = calculate_step_size(south_in, north_in, num_boxes_in_dir)
    box_size_west_east = calculate_step_size(west_in, east_in, num_boxes_in_dir)

    for latitude_index in xrange(num_boxes_in_dir):                # south - north
        for longitude_index in xrange(num_boxes_in_dir):           # west - east
            box = CoordinateBox()

            south = south_in + latitude_index * box_size_south_north
            north = south + box_size_south_north
            west = west_in + longitude_index * box_size_west_east
            east = west + box_size_west_east

            generator = RawCoordinateGenerator()
            raw_coord_list = generator.generate_raw_coordinates(south, north, west, east, num_coords_in_dir)
            box.latitude_distance_to_next_coordinate = generator.get_lat_distance_between_coords()
            box.longitude_distance_to_next_coordinate = generator.get_lon_distance_between_coords()
            box.precision = 4 # Default
            box.save()
            print 'Created: ', box
            for raw_coordinate in raw_coord_list:
                coordinate = Coordinate(latitude = raw_coordinate[0], longitude = raw_coordinate[1], box = box)
                coordinate.save()

def read_data():
    print '-- READ --'
    print 'boxes len', len(CoordinateBox.select())

    coordinates = CoordinateBox.get(CoordinateBox.id == 1).get()
    for coord in coordinates.coordinates:
        pass #print 'COORD', coord

    print 'coordinates len', len(Coordinate.select())
    for coord in Coordinate.select():
        pass #print 'coord:', coord

    for box in CoordinateBox.select():
        print 'box:', box
        for coord in box.coordinates:
            print coord
