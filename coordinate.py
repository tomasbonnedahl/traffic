from minutes_to_color import minutes_to_color_5, minutes_to_color_10

class Coordinate(object):
    def __init__(self, lat, lon):
        self._lat = lat
        self._lon = lon
        self._minutes = None

    def __str__(self):
        return self.get_latitude_as_str() + ', ' + self.get_longitude_as_str()

    def __gt__(self, other):
        if self.get_latitude() == other.get_latitude():
            return self.get_longitude() > self.get_longitude()
        return self.get_latitude() > other.get_latitude()

    def __lt__(self, other):
        if self.get_latitude() == other.get_latitude():
            return self.get_longitude() < self.get_longitude()
        return self.get_latitude() < other.get_latitude()

    def __ge__(self, other):
        if self.get_latitude() == other.get_latitude():
            return self.get_longitude() <= self.get_longitude()
        return self.get_latitude() <= other.get_latitude()

    def __le__(self, other):
        if self.get_latitude() == other.get_latitude():
            return self.get_longitude() <= self.get_longitude()
        return self.get_latitude() <= other.get_latitude()

    def get_latitude(self):
        return self._lat

    def get_longitude(self):
        return self._lon

    def get_latitude_as_str(self):
        return str(self._lat)

    def get_longitude_as_str(self):
        return str(self._lon)

    def set_duration(self, minutes):
        self._minutes = minutes

    def get_duration(self):
        return self._minutes

    def has_duration(self):
        return self._minutes != None

    def get_minutes_to_color_mapping(self):
        return minutes_to_color_5

    def get_color(self):
        color = None
        minutes_to_color = self.get_minutes_to_color_mapping()
        if self.has_duration():
            for key in sorted(minutes_to_color.keys()):
                if int(self.get_duration()) < key and not color:
                    color = minutes_to_color[key]
        if not color:
            color = minutes_to_color[95]
        return color

    def round_and_str(self, value):
        return str(round(value, 6))

    def construct_str(self, lat, lon):
        return self.round_and_str(lat) + ',' + self.round_and_str(lon)

    def get_square_nw_as_str(self, lat_delta, lon_delta):
        return self.construct_str(self.get_latitude() + lat_delta, self.get_longitude() - lon_delta)

    def get_square_sw_as_str(self, lat_delta, lon_delta):
        return self.construct_str(self.get_latitude() - lat_delta, self.get_longitude() - lon_delta)

    def get_square_se_as_str(self, lat_delta, lon_delta):
        return self.construct_str(self.get_latitude() - lat_delta, self.get_longitude() + lon_delta)

    def get_square_ne_as_str(self, lat_delta, lon_delta):
        return self.construct_str(self.get_latitude() + lat_delta, self.get_longitude() + lon_delta)

class Coordinates(object):
    def __init__(self):
        self._lat_delta = None
        self._lon_delta = None
        self._coordinates = []

    def set_lat_delta(self, lat_delta):
        self._lat_delta = lat_delta

    def set_lon_delta(self, lon_delta):
        self._lon_delta = lon_delta

    def get_lat_delta(self):
        return self._lat_delta

    def get_lon_delta(self):
        return self._lon_delta

    def add_coordinate(self, coordinate):
        self._coordinates.append(coordinate)

    def coordinates(self):
        return self._coordinates