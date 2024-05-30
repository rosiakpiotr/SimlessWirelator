import numpy as np
from shapely.geometry import Point, Polygon, LineString

def cast_points_to_shape(x, y, center, obstacle_points):
    """
    Cast points onto an obstacle shape if they are in line with the center of the shape.

    Parameters:
    x (np.ndarray): x-coordinates of the points to be cast.
    y (np.ndarray): y-coordinates of the points to be cast.
    center (tuple): The (x, y) coordinates of the center of the shape.
    obstacle_points (np.ndarray): The points representing the obstacle shape.

    Returns:
    np.ndarray: Adjusted x-coordinates of the points.
    np.ndarray: Adjusted y-coordinates of the points.
    """
    center = Point(center)
    obstacle = Polygon(obstacle_points)
    
    new_x, new_y = np.copy(x), np.copy(y)

    # Vectorized operation to cast points
    shape_points = np.vstack((x, y)).T
    for i, point in enumerate(shape_points):
        line = LineString([center, Point(point)])
        if obstacle.intersects(line):
            intersection = line.intersection(obstacle.boundary)
            if intersection.geom_type == 'Point':
                new_x[i], new_y[i] = intersection.x, intersection.y
            elif intersection.geom_type == 'MultiPoint':
                # Find the closest intersection point
                closest_point = min(intersection.geoms, key=lambda pt: center.distance(pt))
                new_x[i], new_y[i] = closest_point.x, closest_point.y

    return new_x, new_y