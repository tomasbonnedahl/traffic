import unittest

from math import hypot

from coordinate_utils import distance_between, calculate_step_size
from coordinate_generator import RawCoordinateGenerator
from coordinate import Coordinate, CoordinateBox, open_database_connection, close_database_connection
from box_creator import create_boxes_and_coordinates

class TestingClass(unittest.TestCase):
    def setUp(self):
        self.south = 100.0
        self.north = 200.0
        self.west = 200.0
        self.east = 300.0
        self.generator = RawCoordinateGenerator()
        open_database_connection(persistent=False)

    def tearDown(self):
        close_database_connection()

    def get_coordinate_lines(self):
        south = 58.900000  # Horizontal line
        north = 59.800000  # Horizontal line
        west =  17.700000  # Vertical line
        east =  18.600000  # Vertical line
        return south, north, west, east

    def set_precision_on_box(self, box, precision):
        box.precision = precision
        box.save()

    def test_nbr_of_raw_coordinates_generated(self):
        num_of_steps = 3
        raw_coordinates = self.generator.generate_raw_coordinates(self.south, self.north, self.west, self.east, num_of_steps)
        self.assertEqual(len(raw_coordinates), 9)

        num_of_steps = 15
        raw_coordinates = self.generator.generate_raw_coordinates(self.south, self.north, self.west, self.east, num_of_steps)
        self.assertEqual(len(raw_coordinates), 225)

    def test_lat_lon_distance(self):
        num_of_steps = 3
        raw_coordinates = self.generator.generate_raw_coordinates(self.south, self.north, self.west, self.east, num_of_steps)
        self.assertEqual(self.generator.get_lat_distance_between_coords(), 33.333333)
        self.assertEqual(self.generator.get_lon_distance_between_coords(), 33.333333)

    def test_distance_matches_hypot_3_3(self):
        num_of_steps = 3
        raw_coordinates = self.generator.generate_raw_coordinates(self.south, self.north, self.west, self.east, num_of_steps)
        hypot_value = round(hypot(self.generator.get_lat_distance_between_coords(), self.generator.get_lon_distance_between_coords()), 6)
        self.assertEqual(distance_between(raw_coordinates[0], raw_coordinates[4]), hypot_value)
        self.assertEqual(distance_between(raw_coordinates[4], raw_coordinates[0]), hypot_value)
        self.assertEqual(distance_between(raw_coordinates[2], raw_coordinates[4]), hypot_value)
        self.assertEqual(distance_between(raw_coordinates[4], raw_coordinates[2]), hypot_value)

    def test_distance_matches_hypot_15_15(self):
        num_of_steps = 15
        raw_coordinates = self.generator.generate_raw_coordinates(self.south, self.north, self.west, self.east, num_of_steps)
        hypot_value = round(hypot(self.generator.get_lat_distance_between_coords(), self.generator.get_lon_distance_between_coords()), 6)
        self.assertEqual(distance_between(raw_coordinates[0], raw_coordinates[16]), hypot_value)
        self.assertEqual(distance_between(raw_coordinates[16], raw_coordinates[0]), hypot_value)
        self.assertEqual(distance_between(raw_coordinates[2], raw_coordinates[16]), hypot_value)
        self.assertEqual(distance_between(raw_coordinates[16], raw_coordinates[2]), hypot_value)

    def test_distance_between(self):
        num_of_steps = 3
        raw_coordinates = self.generator.generate_raw_coordinates(self.south, self.north, self.west, self.east, num_of_steps)

        self.assertEqual(distance_between(raw_coordinates[0], raw_coordinates[4]), distance_between(raw_coordinates[4], raw_coordinates[0]))
        self.assertEqual(distance_between(raw_coordinates[2], raw_coordinates[4]), distance_between(raw_coordinates[4], raw_coordinates[2]))
        self.assertEqual(distance_between(raw_coordinates[0], raw_coordinates[4]), distance_between(raw_coordinates[4], raw_coordinates[2]))

    def test_coordinates_generated(self):
        num_of_steps = 3
        raw_coordinates = self.generator.generate_raw_coordinates(self.south, self.north, self.west, self.east, num_of_steps)
        self.assertEqual(raw_coordinates[0], (116.666667, 216.666667))
        self.assertEqual(raw_coordinates[2], (116.666667, 283.333333))
        self.assertEqual(raw_coordinates[8], (183.333333, 283.333333))

    def test_distance_between(self):
        num_of_steps = 15
        raw_coordinates = self.generator.generate_raw_coordinates(self.south, self.north, self.west, self.east, num_of_steps)
        hypot_value = round(hypot(self.generator.get_lat_distance_between_coords(), self.generator.get_lon_distance_between_coords()), 6)

        # Single
        self.assertEqual(distance_between(raw_coordinates[0], raw_coordinates[16]), distance_between(raw_coordinates[16], raw_coordinates[0]))
        self.assertEqual(distance_between(raw_coordinates[2], raw_coordinates[16]), distance_between(raw_coordinates[16], raw_coordinates[2]))
        self.assertEqual(distance_between(raw_coordinates[0], raw_coordinates[16]), distance_between(raw_coordinates[16], raw_coordinates[2]))
        self.assertEqual(distance_between(raw_coordinates[0], raw_coordinates[16]), hypot_value)

        # Double
        self.assertEqual(distance_between(raw_coordinates[0], raw_coordinates[32]), distance_between(raw_coordinates[32], raw_coordinates[0]))
        self.assertEqual(distance_between(raw_coordinates[4], raw_coordinates[32]), distance_between(raw_coordinates[32], raw_coordinates[4]))
        self.assertEqual(distance_between(raw_coordinates[0], raw_coordinates[32]), distance_between(raw_coordinates[32], raw_coordinates[4]))
        self.assertEqual(distance_between(raw_coordinates[0], raw_coordinates[32]), 2*hypot_value)

    def test_create_one_box_15_15_coords_validate_neighbours_prec_2(self):
        south, north, west, east = self.get_coordinate_lines()

        create_boxes_and_coordinates(south, north, west, east, 1, 15)
        box = CoordinateBox.get(CoordinateBox.id == 1).get()
        self.set_precision_on_box(box, 2)

        coordinates = box.coordinates
        self.assertEqual(len(coordinates), 225)

        center_coordinates = box.center_coordinates()
        self.assertEqual(len(center_coordinates), 25)
        self.assertEqual(center_coordinates[0], coordinates[16])

        for center_coordinate in center_coordinates:
            neighbours = box.neighbours(center_coordinate)
            self.assertEqual(len(neighbours), 8, 'Failed for coordinate: {}, len was {}'.format(center_coordinate, len(neighbours)))

    def test_create_one_box_15_15_coords_validate_neighbours_prec_3(self):
        south, north, west, east = self.get_coordinate_lines()

        create_boxes_and_coordinates(south, north, west, east, 1, 15)
        box = CoordinateBox.get(CoordinateBox.id == 1).get()
        self.set_precision_on_box(box, 3)

        self.assertEqual(len(box.coordinates), 225)

        center_coordinates = box.center_coordinates()
        self.assertEqual(len(center_coordinates), 9)
        self.assertEqual(center_coordinates[0], box.coordinates[32])

        for center_coordinate in center_coordinates:
            neighbours = box.neighbours(center_coordinate)
            self.assertEqual(len(neighbours), 24, 'Failed for coordinate: {}, len was {}'.format(center_coordinate, len(neighbours)))
