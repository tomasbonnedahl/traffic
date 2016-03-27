from coordinate import Coordinate, CoordinateBox

def write_output_file():
    print '-- WRITE ---'
    with open('coordinates_colored.txt', 'w') as output_file:
        for box in CoordinateBox.select():
            for coordinate in box.coordinates:
                if coordinate.color:
                    # TODO: get_square should be able to go the box itself and get lat and lon...
                    output_file.write('%s\n' % coordinate.get_square_nw_as_str(box.latitude_distance_to_next_coordinate, box.longitude_distance_to_next_coordinate))
                    output_file.write('%s\n' % coordinate.get_square_sw_as_str(box.latitude_distance_to_next_coordinate, box.longitude_distance_to_next_coordinate))
                    output_file.write('%s\n' % coordinate.get_square_se_as_str(box.latitude_distance_to_next_coordinate, box.longitude_distance_to_next_coordinate))
                    output_file.write('%s\n' % coordinate.get_square_ne_as_str(box.latitude_distance_to_next_coordinate, box.longitude_distance_to_next_coordinate))
                    output_file.write('%s\n' % coordinate.color)
                    output_file.write('%s\n' % coordinate.minutes)
    print 'File written'