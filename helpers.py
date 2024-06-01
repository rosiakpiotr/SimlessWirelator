from math import sqrt
import networkx as nx
import numpy as np
from shapely.geometry import Polygon, Point, LineString
import shapely.ops


def cdt_triangulate(polygon):
    triangulated = np.array(shapely.ops.triangulate(polygon))
    return triangulated[polygon.contains(triangulated)]


def create_graph_from_triangulation(triangles):
    G = nx.Graph()
    for triangle in triangles:
        # Ignore the repeated last point
        coords = list(triangle.exterior.coords)[:-1]
        for i, p1 in enumerate(coords):
            for j, p2 in enumerate(coords):
                if i != j:
                    G.add_edge(tuple(p1), tuple(p2),
                               weight=Point(p1).distance(Point(p2)))
    return G


def calculate_path_length(path):
    length = 0.0
    for i in range(len(path) - 1):
        p1 = path[i]
        p2 = path[i + 1]
        length += sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    return length


def shortest_path_in_polygon(polygon, start, end):
    print("Shortest path in polygon")
    triangles = cdt_triangulate(polygon)
    print("Triangulated polygon", polygon)
    G = create_graph_from_triangulation(triangles)
    G.add_node(tuple(start))
    G.add_node(tuple(end))

    for node in G.nodes:
        if is_visible(start, node, polygon):
            G.add_edge(tuple(start), node, weight=Point(
                start).distance(Point(node)))
        if is_visible(end, node, polygon):
            G.add_edge(tuple(end), node, weight=Point(
                end).distance(Point(node)))

    start = tuple(start)
    end = tuple(end)
    path = nx.shortest_path(G, source=start, target=end, weight='weight')
    return calculate_path_length(path), path, G


def is_visible(p1, p2, polygon):
    line = LineString([p1, p2])
    return polygon.contains(line) or polygon.touches(line)


def create_directional_graph(equipment):
    G = nx.DiGraph()

    # Add nodes
    for eq in equipment:
        G.add_node(eq, pos=eq.source_point.coords[0])

    # Add edges with weights (distances)
    for eqA in equipment:
        for eqB in equipment:
            if eqA != eqB and eqA.polygon.contains(eqB.source_point):
                print("Checking edge from", eqA, "to", eqB)
                distance = shortest_path_in_polygon(
                    eqA.polygon, 
                    eqA.source_point.coords[0], 
                    eqB.source_point.coords[0])[0]
                G.add_edge(eqA, eqB, weight=distance)
                print("Added edge from", eqA, "to", eqB, "with distance", distance)

    print("Graph created")
    return G
