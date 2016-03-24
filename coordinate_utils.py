from math import hypot

def distance_between(coord1, coord2):
    lat_diff = coord1[0] - coord2[0]
    lon_diff = coord1[1] - coord2[1]
    return round(hypot(lat_diff, lon_diff), 6)

def calculate_step_size(low, high, num_of_steps):
    total_distance = high - low
    step_size = round(total_distance/num_of_steps, 6)
    return step_size

def round_and_str(value):
    return str(round(value, 6))

def construct_str(lat, lon):
    return round_and_str(lat) + ',' + round_and_str(lon)

def almost_equal(value1, value2):
    return round(value1, 6) == round(value2, 6)
