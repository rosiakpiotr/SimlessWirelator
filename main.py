import numpy as np
import matplotlib.pyplot as plt
from entities import *
import helpers
import plotting

import file_operations as fo
equipment, obstacles = fo.read_configuration_csv("configuration.txt")


def run_through_configuration():
    from obstacle_casting import cast_points_to_shape

    # Apply obstacles blockage to signal boundary points
    for i, eq in enumerate(equipment):
        x, y = eq.polygon.exterior.coords.xy
        for obstacle in obstacles:
            cast_points_to_shape(x, y, eq.source_point, obstacle.polygon)
        equipment[i] = Entity(eq.source_point.xy, x, y, eq.entity_type)

    plotting.plot_map(equipment, obstacles)
    # plt.show()

    # print("Creating directional graph...")
    G = helpers.create_directional_graph(equipment)
    # print("Created directional graph...")

    def on_obstacle_click(event):
        for obstacle in obstacles:
            if obstacle.polygon.contains(Point(event.mouseevent.xdata, event.mouseevent.ydata)):
                print("Obstacle:", obstacle.entity_type)
                obstacles.remove(obstacle)
                # run_through_configuration()
                break
    
    try:
        dst, path = helpers.nx.single_source_dijkstra(
            G, source=equipment[0], target=equipment[1])
        
        centres = [eq.source_point for eq in path]
        plt.figure()
        plt.clf()
        
        plotting.plot_map(equipment, obstacles, selected_eqs=path)
        
        plt.gcf().canvas.mpl_connect('pick_event', on_obstacle_click)
        carr = np.array(centres)
        # Plot arrows between points
        for i in range(len(carr) - 1):
            x1, y1 = carr[i].coords[0]
            x2, y2 = carr[i + 1].coords[0]
            plt.arrow(x1, y1, (x2 - x1), (y2 - y1), head_width=0.1,
                    head_length=0.1, fc='r', ec='r')
        plt.grid(False)
    except helpers.nx.NetworkXNoPath as e:
        # plt.clf()
        print(e)

    print("Finishing...")
    plt.show()

run_through_configuration()