from coordinate import CoordinateBox, create_db_tables

from coordinate_sql import create_boxes_and_coordinates # TODO: Change name of file and method
from traffic_proxy import set_traffic_data
from color import set_color_from_traffic
from output_file import write_output_file

south = 58.900000  # Horizontal line
north = 59.800000  # Horizontal line
west =  17.700000  # Vertical line
east =  18.600000  # Vertical line

def set_box_to_useless(box):
    box.precision = 5
    for coordinate in box.coordinates:
        coordinate.minutes = None
        coordinate.color = None
        coordinate.save()
    box.save()

def set_box_to_4(box):
    box.precision = 4
    box.save()

def set_box_precision():
    # Starts with 1, 2, 8, 9
    # Ends with 1, 2, 7, 8, 9
    for box in CoordinateBox.select():
        index = [int(x) for x in str(box.id)]
        if len(index) < 2 or index[0] in [1, 2, 6, 7, 8, 9] or index[1] in [0, 1, 2, 7, 8, 9]:
            set_box_to_useless(box)

def show_all_boxes():
    for box in CoordinateBox.select():
        print box, box.precision

def create_persistent_tables_and_boxes():
    print 'creating db tables'
    create_db_tables()
    print 'creating boxes and coords'
    create_boxes_and_coordinates(south, north, west, east, num_boxes_in_dir=10, num_coords_in_dir=15)
    print 'DONE'

def create_test_boxes():
    create_boxes_and_coordinates(south, north, west, east, num_boxes_in_dir=10, num_coords_in_dir=15)

def update_box():
    d = {33: 3, 34: 3, 35: 3, 36: 3, 37 : 3, 47: 3, 57: 3, 74: 2, 75: 2}
    for key, value in d.iteritems():
        box = CoordinateBox.get(CoordinateBox.id == key)
        box.precision = value
        box.save()
        print 'updated box...'

'''
    Main application
'''
def run():
    #create_persistent_tables_and_boxes()
    #print '-- Setting box precision'
    #set_box_precision()

    print '-- Showing all boxes'
    show_all_boxes()

    print '-- Setting traffic data'
    set_traffic_data()

    print '-- Set color from traffic'
    set_color_from_traffic()

    print '-- Writing output file'
    write_output_file()

run()
#show_all_boxes()


