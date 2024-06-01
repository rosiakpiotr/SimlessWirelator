import matplotlib.pyplot as plt
import obstacle_casting
import plotting
import helpers
from configuration import Configuration


def run_through_configuration(conf: Configuration, from_: int, to_: int):
    equipment, obstacles = conf.equipment.copy(), conf.obstacles.copy()
    obstacle_casting.apply_obstacles(equipment, obstacles)
    plotting.plot_map(equipment, obstacles, "Map")
    plt.tight_layout()

    print("Creating directional graph...")
    G = helpers.create_directional_graph(equipment)
    print("Created directional graph...")

    # def on_obstacle_click(event):
    #     for obstacle in obstacles:
    #         if obstacle.polygon.contains(
    #             Point(event.mouseevent.xdata, event.mouseevent.ydata)
    #         ):
    #             obstacles.remove(obstacle)
    #             c = Configuration(conf.equipment, obstacles)
    #             plt.cla()
    #             run_through_configuration(c)
    #             break

    try:
        dst, path = helpers.nx.single_source_dijkstra(
            G, source=equipment[from_], target=equipment[to_]
        )

        print(f"Path found (distance={dst}), plotting.")
        plotting.plot_path(equipment, obstacles, path)
        plt.tight_layout()
    except helpers.nx.NetworkXNoPath:
        print("No path found, plotting.")
        plotting.plot_path(equipment, obstacles, [])
        plt.tight_layout()

    print("Finishing...")
    plt.show()