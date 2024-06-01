import shapely.plotting
from entities import EntityType
import matplotlib.pyplot as plt
import networkx as nx


def plot_eq_obs(equipment, obstacles, selected_eqs=None):
    if selected_eqs is None:
        selected_eqs = equipment

    # Plotting map
    for eq in equipment:
        shapely.plotting.plot_polygon(
            eq.polygon, add_points=False, facecolor='gray' if eq not in selected_eqs else 'blue', alpha=0.2 if eq not in selected_eqs else 0.45)

    for o in obstacles:
        shapely.plotting.plot_polygon(
            o.polygon, picker=True, add_points=False, facecolor='red')

    
    for eq in equipment:
        marker_mapping = {
            EntityType.YAGI_ANTENNA: f'*${eq.id_}$',
            EntityType.CIRCULAR_ANTENNA: f'*${eq.id_}$',
            EntityType.USER: f'$U{eq.id_}$'
        }
        shapely.plotting.plot_points(
            eq.source_point, marker=marker_mapping[eq.entity_type], color='yellow', markersize=10)
        

def plot_map(equipment, obstacles, title: str, selected_eqs=None):
    # plt.figure()
    plot_eq_obs(equipment, obstacles, selected_eqs)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.gcf().set_size_inches(8, 8)
    plt.grid(False)
    plt.suptitle(title)

    
def plot_path(equipment, obstacles, path):
    plt.figure()
    plot_map(equipment, obstacles, title='Path results', selected_eqs=path)
    carr = [eq.source_point for eq in path]
    plot_arrows_between_points(carr)
    plt.gcf().set_size_inches(8, 8)
    plt.title('->'.join([str(eq) for eq in path]), fontsize=6)
    plt.grid(False)

def plot_dijkstra_graph(G):
    # Plotting directional graph
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

def plot_arrows_between_points(carr):
    # Plot arrows between points
    for i in range(len(carr) - 1):
        x1, y1 = carr[i].coords[0]
        x2, y2 = carr[i + 1].coords[0]
        plt.arrow(
            x1,
            y1,
            (x2 - x1),
            (y2 - y1),
            head_width=0.1,
            head_length=0.1,
            fc="r",
            ec="r",
        )
