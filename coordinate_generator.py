from coordinate_utils import calculate_step_size

class RawCoordinateGenerator(object):
    def __init__(self):
        self.distance_between_coordinates = {}

    def get_lat_distance_between_coords(self):
        return self.distance_between_coordinates['LAT']

    def get_lon_distance_between_coords(self):
        return self.distance_between_coordinates['LON']

    def create_one_direction(self, low, high, num_of_steps):
        step_size = calculate_step_size(low, high, num_of_steps)
        half_step_size = round(step_size/2, 6)
        start_value = low + half_step_size
        return [round(start_value + i * step_size, 6) for i in range(num_of_steps)], step_size

    def generate_latitude(self, south, north, num_of_steps):
        latitudes, dist = self.create_one_direction(south, north, num_of_steps)
        self.distance_between_coordinates['LAT'] = dist
        return latitudes

    def generate_longitude(self, west, east, num_of_steps):
        longitudes, dist = self.create_one_direction(west, east, num_of_steps)
        self.distance_between_coordinates['LON'] = dist
        return longitudes

    def generate_raw_coordinates(self, south, north, west, east, num_of_steps):
        latitude_coords = self.generate_latitude(south, north, num_of_steps)
        longitude_coords = self.generate_longitude(west, east, num_of_steps)
        coords = [(latitude_coords[i], longitude_coords[j])
                  for i in range(len(latitude_coords))
                  for j in range(len(longitude_coords))]
        return coords
