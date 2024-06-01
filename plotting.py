import shapely.plotting
from entities import EntityType
import matplotlib.pyplot as plt
import networkx as nx


def plot_map(equipment, obstacles, selected_eqs=None):
    if selected_eqs is None:
        selected_eqs = equipment

    # Plotting map
    for eq in equipment:
        shapely.plotting.plot_polygon(
            eq.polygon, add_points=False, facecolor='gray' if eq not in selected_eqs else 'blue', alpha=0.2 if eq not in selected_eqs else 0.45)

    for o in obstacles:
        shapely.plotting.plot_polygon(
            o.polygon, add_points=False, facecolor='red')

    marker_mapping = {
        EntityType.YAGI_ANTENNA: '*',
        EntityType.CIRCULAR_ANTENNA: '*',
        EntityType.USER: '$UE$'
    }
    for eq in equipment:
        shapely.plotting.plot_points(
            eq.source_point, marker=marker_mapping[eq.entity_type], color='yellow', markersize=10)

    plt.grid(False)
    plt.tight_layout()


def plot_graph(G):
    # Plotting directional graph
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()
