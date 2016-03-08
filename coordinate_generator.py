from coordinate import Coordinate, Coordinates

#NORTHERN_LATITUDE = 59.514256 # Horizontal
#SOUTHERN_LATITUDE = 59.244671 # Horizontal

#WESTERN_LONGITUDE = 17.756988 # Vertical
#EASTERN_LONGITUDE = 18.449283 # Vertical

NORTHERN_LATITUDE = 59.390876 # Horizontal  # Lidingo
SOUTHERN_LATITUDE = 59.338633 # Horizontal  # Lidingo

WESTERN_LONGITUDE = 18.095055 # Vertical    # Lidingo
EASTERN_LONGITUDE = 18.254978 # Vertical    # Lidingo

# TODO: Remove?
NW = (NORTHERN_LATITUDE, WESTERN_LONGITUDE) # NW Kungsangen
SW = (SOUTHERN_LATITUDE, WESTERN_LONGITUDE) # SW Botkyrka
SE = (SOUTHERN_LATITUDE, EASTERN_LONGITUDE) # SE Varmdo
NE = (NORTHERN_LATITUDE, EASTERN_LONGITUDE) # NE Ljustero

GRID_LINES = 30

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

def generate_coordinates():
    coordinate_generator = CoordinateGenerator(NORTHERN_LATITUDE, SOUTHERN_LATITUDE, WESTERN_LONGITUDE, EASTERN_LONGITUDE)
    return coordinate_generator.generate(GRID_LINES)
