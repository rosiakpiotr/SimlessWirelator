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


import triangle
from shapely.geometry import Polygon, Point, LineString
import networkx as nx
from math import sqrt

def cdt_triangulate(polygon):
    coords = list(polygon.exterior.coords)
    segments = [(i, (i+1) % len(coords)) for i in range(len(coords)-1)]
    A = {'vertices': coords, 'segments': segments}
    B = triangle.triangulate(A, 'p')
    triangles = [Polygon(B['vertices'][triangle]) for triangle in B['triangles']]
    return triangles

def create_graph_from_triangulation(triangles):
    G = nx.Graph()
    for triangle in triangles:
        coords = list(triangle.exterior.coords)[:-1]  # Ignore the repeated last point
        for i, p1 in enumerate(coords):
            for j, p2 in enumerate(coords):
                if i != j:
                    G.add_edge(tuple(p1), tuple(p2), weight=Point(p1).distance(Point(p2)))
    return G

def calculate_path_length(path):
    length = 0.0
    for i in range(len(path) - 1):
        p1 = path[i]
        p2 = path[i + 1]
        length += sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    return length

def shortest_path_in_polygon(polygon, start, end):
    triangles = cdt_triangulate(polygon)
    G = create_graph_from_triangulation(triangles)
    G.add_node(tuple(start))
    G.add_node(tuple(end))

    for node in G.nodes:
        if is_visible(start, node, polygon):
            G.add_edge(tuple(start), node, weight=Point(start).distance(Point(node)))
        if is_visible(end, node, polygon):
            G.add_edge(tuple(end), node, weight=Point(end).distance(Point(node)))

    start = tuple(start)
    end = tuple(end)
    path = nx.shortest_path(G, source=start, target=end, weight='weight')
    return calculate_path_length(path), path, G

def is_visible(p1, p2, polygon):
    line = LineString([p1, p2])
    return polygon.contains(line) or polygon.touches(line)
