import numpy as np
import enum

from shapely import Polygon, Point


class EntityType(enum.Enum):
    USER = 0
    CIRCULAR_ANTENNA = 1
    YAGI_ANTENNA = 2

    RECTANGULAR_OBSTACLE = 3


class Entity(object):
    def __init__(self, source: tuple[2], xs: np.ndarray, ys: np.ndarray, entity_type: EntityType):
        self._source_cords = Point(source)
        self._polygon = Polygon(np.vstack((xs, ys)).T)
        self._entity_type = entity_type

    @property
    def source_point(self) -> Point:
        return self._source_cords

    @property
    def polygon(self) -> Polygon:
        return self._polygon

    @property
    def entity_type(self) -> EntityType:
        return self._entity_type


def create_circular(center, radiation_diameter):
    theta = np.linspace(0, 2*np.pi, int(360*0.5))
    xs = radiation_diameter*0.5*np.sin(theta)
    ys = radiation_diameter*0.5*np.cos(theta)
    return xs + center[0], ys + center[1]

def create_user_equipment(center, radiation_diameter):
    xs, ys = create_circular(center, radiation_diameter)
    return Entity(center, xs, ys, EntityType.USER)

def create_circular_antenna(center, radiation_diameter):
    xs, ys = create_circular(center, radiation_diameter)
    return Entity(center, xs, ys, EntityType.CIRCULAR_ANTENNA)


def create_yagi_antenna(center, tilt, length, width):
    length = length*0.5
    width = width*0.5
    tilt_angle = np.deg2rad(-tilt+90)
    theta = np.linspace(0, 2*np.pi, int(360*0.5))
    xs = np.sin(tilt_angle)*width + length*np.cos(theta) * \
        np.cos(tilt_angle) - width*np.sin(theta)*np.sin(tilt_angle)
    ys = -width*np.cos(tilt_angle) + length*np.cos(theta) * \
        np.sin(tilt_angle) + width*np.sin(theta)*np.cos(tilt_angle)
    return Entity(center, xs+center[0], ys+center[1], EntityType.YAGI_ANTENNA)


def create_rectangular_obstacle(center, width, height, angle):
    w = width*0.5
    h = height*0.5
    angle = np.deg2rad(angle)
    corners = np.array([[-w, -h], [w, -h], [w, h], [-w, h]])
    rot_matrix = np.array(
        [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    corners = np.dot(corners, rot_matrix.T) + center
    return Entity(center, corners[:, 0], corners[:, 1], EntityType.RECTANGULAR_OBSTACLE)
