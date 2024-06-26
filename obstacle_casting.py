import numpy as np
from shapely.geometry import Point, Polygon, LineString

from entities import Entity


def cast_points_to_shape(x: np.ndarray, y: np.ndarray, source: Point, obstacle: Polygon):
    """
    Cast points onto an obstacle shape if they are in line with the source of the shape.
    """
    shape_points = np.vstack((x, y)).T
    for i, point in enumerate(shape_points):
        line = LineString([source, Point(point)])
        if obstacle.intersects(line):
            intersection = line.intersection(obstacle.boundary)
            if intersection.geom_type == 'Point':
                x[i], y[i] = intersection.x, intersection.y
            elif intersection.geom_type == 'MultiPoint':
                # Find the closest intersection point
                closest_point = min(intersection.geoms,
                                    key=lambda pt: source.distance(pt))
                x[i], y[i] = closest_point.x, closest_point.y

def apply_obstacles(equipment: list[Entity], obstacles: list[Entity]):
    # Apply obstacles blockage to signal boundary points
    for i, eq in enumerate(equipment):
        x, y = eq.polygon.exterior.coords.xy
        for obstacle in obstacles:
            cast_points_to_shape(x, y, eq.source_point, obstacle.polygon)
        equipment[i] = Entity(eq.id_, eq.source_point.xy, x, y, eq.entity_type)