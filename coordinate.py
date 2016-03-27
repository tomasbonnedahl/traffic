from math import hypot

from peewee import Model, SqliteDatabase, FloatField, IntegerField, BooleanField, ForeignKeyField, CharField
from coordinate_utils import construct_str, almost_equal

PERSISTENT_DB   = 'traffic.db'
TESTING_DB = ':memory:'
DB_NAME = PERSISTENT_DB

database = SqliteDatabase(None)

''' Models '''
class BaseModel(Model):
    class Meta:
        database = database

# Subclasses depending on precision? Own impl of neighbours, center_coord, etc?
class CoordinateBox(BaseModel):
    latitude_distance_to_next_coordinate = FloatField(null=True)
    longitude_distance_to_next_coordinate = FloatField(null=True)
    precision = IntegerField(default=1)

    def __str__(self):
        return 'Box ' + str(self.id)

    def center_coordinates(self):
        center_coordinates = []
        if self.precision == 1:
            # Precision 1 is all coordinates
            center_coordinates = list(self.coordinates)

        elif self.precision == 2:    # TODO: Enum
            delta_index = [16, 19, 22, 25, 28]
            big_count = [0, 45, 90, 135, 180]
            return self.get_center_coordinate_list(delta_index, big_count)

        elif self.precision == 3:
            # TODO: Only one list with the indexes, possibly map to nbr of coordinates in the box (15)
            delta_index = [2, 7, 12]
            big_count = [30, 105, 180]
            return self.get_center_coordinate_list(delta_index, big_count)

        elif self.precision == 4:
            # Least precision, one coordinate of all 15x15
            delta_index = [7]
            big_count = [120]
            return self.get_center_coordinate_list(delta_index, big_count)

        elif self.precision == 5:
            # No coordinates at all - box should be blank
            pass

        else:
            raise Exception('Should not have precision more than 5')
        return center_coordinates

    def get_center_coordinate_list(self, delta_index, big_count):
        center_coordinates = []
        sorted_coordinates = list(self.coordinates)
        center_coordinate_indexes = []
        for i in big_count:
            center_coordinate_indexes += [i+delta for delta in delta_index]

        for center_coordinate_index in center_coordinate_indexes:
            center_coordinates.append(sorted_coordinates[center_coordinate_index])
        return center_coordinates

    def neighbours(self, to_coordinate):
        neighbours = []
        if self.precision == 1 or self.precision == 5:
            # No neighbours
            pass
        elif self.precision == 2 or self.precision == 3:
            for coordinate in self.coordinates:
                if coordinate.is_neightbour_to(to_coordinate):
                    neighbours.append(coordinate)
        elif self.precision == 4:
            # All are neighbours except the coordinate requested
            # TODO: Do something more clever here to remove one, we know the index...?
            for coordinate in self.coordinates:
                if coordinate != to_coordinate:
                    neighbours.append(coordinate)
        return neighbours

class Coordinate(BaseModel):
    latitude = FloatField()
    longitude = FloatField()
    minutes = IntegerField(null=True)
    color = CharField(null=True)
    exception = BooleanField(default=False)
    box = ForeignKeyField(CoordinateBox, related_name='coordinates')

    def _unrounded_single_hypot(self):
        return hypot(self.box.latitude_distance_to_next_coordinate, self.box.longitude_distance_to_next_coordinate)

    def get_single_hypot(self):
        return round(self._unrounded_single_hypot(), 6)

    def get_double_hypot(self):
        return round(2*self._unrounded_single_hypot(), 6)

    def is_neightbour_to(self, to_coordinate):
        neighbour = False

        if almost_equal(self.latitude, to_coordinate.latitude) and almost_equal(self.longitude, to_coordinate.longitude):
            return False # Same coordinate

        if self.box.precision == 2:
            dist = round(hypot(self.latitude - to_coordinate.latitude, self.longitude - to_coordinate.longitude), 6)
            if dist <= self.get_single_hypot():

                return True

        elif self.box.precision == 3:
            dist = round(hypot(self.latitude - to_coordinate.latitude, self.longitude - to_coordinate.longitude), 6)
            if dist <= self.get_double_hypot():
                return True

        return neighbour

    def get_abs_latitude_diff(self, to_coordinate):
        return abs(round(self.latitude - to_coordinate.latitude, 6))

    def get_abs_longitude_diff(self, to_coordinate):
        return abs(round(self.longitude - to_coordinate.longitude, 6))

    def get_square_nw_as_str(self, lat_distance_to_next_coordinate, lon_distance_to_next_coordinate):
        return construct_str(self.latitude + lat_distance_to_next_coordinate/2, self.longitude - lon_distance_to_next_coordinate/2)

    def get_square_sw_as_str(self, lat_distance_to_next_coordinate, lon_distance_to_next_coordinate):
        return construct_str(self.latitude - lat_distance_to_next_coordinate/2, self.longitude - lon_distance_to_next_coordinate/2)

    def get_square_se_as_str(self, lat_distance_to_next_coordinate, lon_distance_to_next_coordinate):
        return construct_str(self.latitude - lat_distance_to_next_coordinate/2, self.longitude + lon_distance_to_next_coordinate/2)

    def get_square_ne_as_str(self, lat_distance_to_next_coordinate, lon_distance_to_next_coordinate):
        return construct_str(self.latitude + lat_distance_to_next_coordinate/2, self.longitude + lon_distance_to_next_coordinate/2)

    def __str__(self):
        return str(self.latitude) + ', ' + str(self.longitude)

    def __gt__(self, other):
        if self.latitude == other.latitude:
            return self.longitude > self.longitude
        return self.latitude > other.latitude

    def __lt__(self, other):
        if self.latitude == other.latitude:
            return self.longitude < self.longitude
        return self.latitude < other.latitude

    def __ge__(self, other):
        if self.latitude == other.latitude:
            return self.longitude <= self.longitude
        return self.latitude <= other.latitude

    def __le__(self, other):
        if self.latitude == other.latitude:
            return self.longitude <= self.longitude
        return self.latitude <= other.latitude

    def __eq__(self, other):
        return self.latitude == other.latitude and self.longitude == other.longitude

def open_database_connection(persistent = True):
    if persistent:
        database.init(PERSISTENT_DB)
        database.connect()
    else:
        database.init(TESTING_DB)
        database.connect()
        database.create_tables([CoordinateBox, Coordinate], safe=True)

def close_database_connection():
    ''' Closes the database connection '''
    database.close()

def create_db_tables():
    database.create_tables([CoordinateBox, Coordinate], safe=True)
    print "Database configured"