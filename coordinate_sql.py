from peewee import Model, SqliteDatabase, FloatField, IntegerField, BooleanField, ForeignKeyField, CharField

#PERSISTENT_DB   = 'traffic_data.db'
TESTING_DB = ':memory:'

database = SqliteDatabase(TESTING_DB)

class BaseModel(Model):
    class Meta:
        database = database

class CoordinatesSql(BaseModel):
    #area_id = IntegerField()
    latitude_delta = FloatField(null=True)
    longitude_delta = FloatField(null=True)
    precision = IntegerField(default=1)

    def __str__(self):
        return 'Area ' + str(self.id)

class CoordinateSql(BaseModel):
    latitude = FloatField()
    longitude = FloatField()
    minutes = IntegerField(null=True)
    color = CharField(null=True)
    exception = BooleanField(default=False)
    area = ForeignKeyField(CoordinatesSql, related_name='coordinates')

    def __str__(self):
        return str(self.latitude) + ', ' + str(self.longitude)

database.connect()
database.create_tables([CoordinatesSql, CoordinateSql])

#NORTHERN_LATITUDE = 59.514256 # Horizontal
#SOUTHERN_LATITUDE = 59.244676 # Horizontal
#WESTERN_LONGITUDE = 17.756988 # Vertical
#EASTERN_LONGITUDE = 18.449288 # Vertical

NORTHERN_LATITUDE = 200.0 # Horizontal
SOUTHERN_LATITUDE = 100.0 # Horizontal
WESTERN_LONGITUDE = 100.0 # Vertical
EASTERN_LONGITUDE = 200.0 # Vertical


def get_diff(value1, value2):
    return (value1 - value2)/2

#GRID_LINES = 2

class CoordinateGenerator(object):
    def __init__(self, north, south, west, east):
        self._north = north
        self._south = south
        self._west = west
        self._east = east
        self._deltas = {}

    def get_delta(self, lat_or_lon):
        return self._deltas[lat_or_lon]

    def generate_coordinates_in_one_direction(self, lat_or_lon, from_line, to_line, grid_lines):
        distance = to_line - from_line
        delta = distance / grid_lines
        self._deltas[lat_or_lon] = delta
        return [round(from_line + i * delta, 6) for i in range(grid_lines + 1)]

    def generate_latitude(self, grid_lines):
        return self.generate_coordinates_in_one_direction('LAT', SOUTHERN_LATITUDE, NORTHERN_LATITUDE, grid_lines)

    def generate_longitude(self, grid_lines):
        return self.generate_coordinates_in_one_direction('LON', WESTERN_LONGITUDE, EASTERN_LONGITUDE, grid_lines)

    def generate_raw_coordinates(self, grid_lines):
        latitude_coords = self.generate_latitude(grid_lines)
        longitude_coords = self.generate_longitude(grid_lines)
        coords = [(latitude_coords[i], longitude_coords[j])
                  for i in range(len(latitude_coords))
                  for j in range(len(longitude_coords))]
        return coords

    def generate(self, grid_lines):
        '''
        Returns a Coordinates object with Coordinate objects in it
        '''
        coordinates = Coordinates()
        raw_coordinates = self.generate_raw_coordinates(grid_lines)
        for raw_coordinate in raw_coordinates:
            coordinate = Coordinate(raw_coordinate[0], raw_coordinate[1])
            coordinates.add_coordinate(coordinate)

        coordinates.set_lat_delta(self._deltas['LAT'])
        coordinates.set_lon_delta(self._deltas['LON'])

        return coordinates

'''
def generate_coordinates():
    coordinate_generator = CoordinateGenerator(NORTHERN_LATITUDE, SOUTHERN_LATITUDE, WESTERN_LONGITUDE, EASTERN_LONGITUDE)
    return coordinate_generator.generate(GRID_LINES)
'''

class ChangeName(object):
    def __init__(self):
        self._deltas = {}

    def get_delta(self, lat_or_lon):
        return self._deltas[lat_or_lon]

    def generate_coordinates_in_one_direction(self, from_line, to_line, grid_lines, lat_or_lon):
        distance = to_line - from_line
        delta = distance / grid_lines
        self._deltas[lat_or_lon] = delta
        return [round(from_line + i * delta, 6) for i in range(grid_lines + 1)]

    def generate_latitude(self, from_latitude, to_latitude, grid_lines):
        return self.generate_coordinates_in_one_direction(from_latitude, to_latitude, grid_lines, 'LAT')

    def generate_longitude(self, from_longitude, to_longitude, grid_lines):
        return self.generate_coordinates_in_one_direction(from_longitude, to_longitude, grid_lines, 'LON')

    def generate_raw_coordinates(self, from_latitude, to_latitude, from_longitude, to_longitude, grid_lines):
        latitude_coords = self.generate_latitude(from_latitude, to_latitude, grid_lines)
        longitude_coords = self.generate_longitude(from_longitude, to_longitude, grid_lines)
        coords = [(latitude_coords[i], longitude_coords[j])
                  for i in range(len(latitude_coords))
                  for j in range(len(longitude_coords))]
        return coords

north_south_distance = get_diff(NORTHERN_LATITUDE, SOUTHERN_LATITUDE)
east_west_distance = get_diff(EASTERN_LONGITUDE, WESTERN_LONGITUDE)

print 'north_south', north_south_distance
print 'east west', east_west_distance

def save_data():
    print '-- SAVE --'
    for i in xrange(2):
        for j in xrange(2):
            coords = CoordinatesSql()

            south = SOUTHERN_LATITUDE+i*north_south_distance
            north = south+north_south_distance

            west = WESTERN_LONGITUDE+j*east_west_distance
            east = west+east_west_distance

            print 'north', north
            print 'south', south
            print 'east', east
            print 'west', west

            coord_objs = []
            change_name = ChangeName()
            raw_coordinates = change_name.generate_raw_coordinates(south, north, west, east, grid_lines=2)
            for raw_coordinate in raw_coordinates:
                coord = CoordinateSql(latitude=raw_coordinate[0], longitude=raw_coordinate[1], area=coords)
                coord_objs.append(coord)
                print 'Created coord object', raw_coordinate[0], raw_coordinate[1]

            print 'LAT:', change_name.get_delta('LAT')
            print 'LON:', change_name.get_delta('LON')

            coords.save()
            for coord in coord_objs:
                coord.save()

def read_data():
    print '-- READ --'
    print 'coords len', len(CoordinatesSql.select())
    '''
    coordinates = CoordinatesSql.get(CoordinatesSql.id == 1).get()
    for coord in coordinates.coordinates:
        pass #print 'COORD', coord
    '''
    print 'coord len', len(CoordinateSql.select())
    for coord in CoordinateSql.select():
        pass #print 'coord:', coord

    for coords in CoordinatesSql.select():
        print 'coords:', coords
        for coord in coords.coordinates:
            print coord

save_data()
read_data()