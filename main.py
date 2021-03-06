from coordinate import CoordinateBox, create_db_tables, open_database_connection, close_database_connection

from box_creator import create_boxes_and_coordinates
from traffic_proxy import set_traffic_data
from color import set_color_from_traffic
from output_file import write_output_file

south = 58.900000  # Horizontal line
north = 59.800000  # Horizontal line
west =  17.700000  # Vertical line
east =  18.600000  # Vertical line

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
    d = {32: 1, 42: 1, 31: 1, 41: 1, 49: 1}
    for key, value in d.iteritems():
        box = CoordinateBox.get(CoordinateBox.id == key)
        if not box.precision == value:
            box.precision = value
            box.save()
            print 'updated box...'

def clean_boxes():
    boxes = [54, 55, 64, 65]
    for box_index in boxes:
        box = CoordinateBox.get(CoordinateBox.id == box_index)
        for coordinate in box.coordinates:
            coordinate.minutes = None
            coordinate.color = None
            coordinate.save()

'''
    Main application
'''
def set_color_and_write_to_file():
    print '-- Set color from traffic'
    set_color_from_traffic()

    print '-- Writing output file'
    write_output_file()

def run():
    #create_persistent_tables_and_boxes()
    print '-- Setting traffic data'
    set_traffic_data()
    set_color_and_write_to_file()

def run_with_exception_coordinates():
    print '-- Setting traffic data'
    set_traffic_data(include_exception_coordinates=True)
    set_color_and_write_to_file()

def execute():
    #clean_boxes()
    run()
    #run_with_exception_coordinates()
    #update_box()
    #show_all_boxes()
    #set_color_and_write_to_file()
try:
    open_database_connection()
    execute()
except Exception as e:
    print '### Received exception:', e
finally:
    print 'Closing db connection'
    close_database_connection()
