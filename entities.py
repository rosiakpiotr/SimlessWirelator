import numpy as np
import shapely

class Equipment(object):
    def __init__(self, center):
        self.center_cords = center

    @property
    def center(self):
        return self.center_cords


class UserEquipment(Equipment):
    def __init__(self, center, radiation_diameter):
        super().__init__(center)
        self.__radiation_diameter = radiation_diameter
        self.__compute_outline()

    def __compute_outline(self):
        theta = np.linspace(0, 2*np.pi, int(360*0.2))
        xs = self.__radiation_diameter*0.5*np.sin(theta)
        ys = self.__radiation_diameter*0.5*np.cos(theta)
        self.__outline = (xs, ys)

    @property
    def outline(self):
        xs,ys=self.__outline
        return xs + self.center[0], ys + self.center[1]


class CircularAntenna(Equipment):

    def __init__(self, center: tuple, radiation_diameter: float):
        super().__init__(center)
        self.__radiation_diameter = radiation_diameter
        # print('Circular antenna, args: ', center, radiation_diameter)
        self.__compute_outline()

    def __compute_outline(self):
        theta = np.linspace(0, 2*np.pi, int(360*0.2))
        xs = self.__radiation_diameter*0.5*np.sin(theta)
        ys = self.__radiation_diameter*0.5*np.cos(theta)
        self.__outline = (xs, ys)

    @property
    def outline(self):
        xs,ys=self.__outline
        return xs + self.center[0], ys + self.center[1]

class YagiAntenna(Equipment):

    def __init__(self, center, tilt, length, width):
        super().__init__(center)
        self.tilt = tilt
        self.length = length
        self.width = width
        # print('Yagi antenna, args: ', center, tilt, length, width)
        self.__compute_outline()

    def __compute_outline(self):
        length = self.length*0.5
        width = self.width*0.5
        tilt_angle = np.deg2rad(-self.tilt+90)
        theta = np.linspace(0, 2*np.pi, int(360*0.5))
        xs = np.sin(tilt_angle)*width + length*np.cos(theta)*np.cos(tilt_angle) - width*np.sin(theta)*np.sin(tilt_angle)
        ys = -width*np.cos(tilt_angle) + length*np.cos(theta)*np.sin(tilt_angle) + width*np.sin(theta)*np.cos(tilt_angle)
        self.__outline = (xs,ys)

    @property
    def outline(self):
        xs,ys=self.__outline
        return xs + self.center[0], ys + self.center[1]
    
class RectangularObstacle(Equipment):

    def __init__(self, center, width, height, angle):
        super().__init__(center)
        self.width=width
        self.height=height
        self.angle=angle
        self.polygon = shapely.Polygon(self.corners)

    @property
    def corners(self):
        w = self.width*0.5
        h = self.height*0.5
        angle = np.deg2rad(self.angle)
        corners = np.array([[-w, -h], [w, -h], [w, h], [-w, h]])
        rot_matrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        return np.dot(corners, rot_matrix.T) + self.center # + np.array([-w, 2*h])
