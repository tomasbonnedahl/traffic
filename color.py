from coordinate import Coordinate, CoordinateBox

from minutes_to_color import minutes_to_color_5, minutes_to_color_10

def get_color_from_minutes(minutes):
    color = None
    sorted_keys = sorted(minutes_to_color_10.keys())
    for key in sorted_keys:
        if minutes <= key and not color:
            color = minutes_to_color_10[key]
    if not color:
        color = max(sorted_keys)
    return color

def set_color_from_traffic():
    print '-- COLOR ---'
    for box in CoordinateBox.select():
        center_coordinates = box.center_coordinates()
        for center_coordinate in center_coordinates:
            # Get color for center coordinate
            if center_coordinate.minutes is not None:
                center_coordinate.color = get_color_from_minutes(center_coordinate.minutes)
                center_coordinate.save()

            for neighbour in box.neighbours(center_coordinate):
                # Color neighbours to center coordinate
                neighbour.color = center_coordinate.color
                neighbour.save()