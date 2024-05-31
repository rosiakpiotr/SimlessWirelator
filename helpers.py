import csv
from entities import *

def read_equipment_csv(filename: str):
    type_mapping = {
        'UE': UserEquipment,
        'C': CircularAntenna,
        'Y': YagiAntenna,
        'R': RectangularObstacle
    }
    equipment, obstacles = [], []
    with open(filename) as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            kind = row[0]
            match kind:
                case 'UE':
                    row = np.float_(row[1:])
                    location = row[0:2]
                    ue_params = row[2:]
                    equipment.append(type_mapping[kind](
                        location, *list(ue_params)))
                case 'A':
                    antenna_type = row[1]
                    row = np.float_(row[2:])
                    location = row[0:2]
                    antenna_params = row[2:]
                    equipment.append(type_mapping[antenna_type](
                        location, *list(antenna_params)))
                case 'O':
                    obstacle_type = row[1]
                    row = np.float_(row[2:])
                    center=row[0:2]
                    obstacles.append(type_mapping[obstacle_type](
                        tuple(center), *list(row[2:])
                    ))
                    

    return equipment, obstacles

from shapely.geometry import Point, LineString
import networkx as nx
from math import sqrt

def shortest_path_in_polygon(polygon, start, end):
    def is_visible(p1, p2, polygon):
        line = LineString([p1, p2])
        return polygon.contains(line)

    def create_visibility_graph(polygon, start, end):
        points = [start, end] + list(polygon.exterior.coords)
        G = nx.Graph()

        for i, p1 in enumerate(points):
            for j, p2 in enumerate(points):
                if i != j and is_visible(p1, p2, polygon):
                    G.add_edge(tuple(p1), tuple(p2), weight=Point(p1).distance(Point(p2)))

        return G
    
    def calculate_path_length(path):
        length = 0.0
        for i in range(len(path) - 1):
            p1 = path[i]
            p2 = path[i + 1]
            length += sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
        return length
    
    G = create_visibility_graph(polygon, start, end)
    start = tuple(start)
    end = tuple(end)

    path = nx.shortest_path(G, source=start, target=end, weight='weight')
    return calculate_path_length(path), path, G
