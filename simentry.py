import logging

import matplotlib.pyplot as plt
import obstacle_casting
import plotting
import helpers
from configuration import Configuration

logger = logging.getLogger(__name__)

def run_through_configuration(conf: Configuration, from_: int, to_: int):
    logger.info("Starting simulation...")
    equipment, obstacles = conf.equipment.copy(), conf.obstacles.copy()
    logger.info("Restricting equipment areas according to obstacles...")
    obstacle_casting.apply_obstacles(equipment, obstacles)
    logger.info("Plotting map...")
    plotting.plot_map(equipment, obstacles, "Map")
    plt.tight_layout()

    logger.info("Creating directional graph...")
    print("Creating directional graph...")
    G = helpers.create_directional_graph(equipment)
    print("Created directional graph...")

    try:
        logger.info(f"Finding path from {from_} to {to_}...")
        dst, path = helpers.nx.single_source_dijkstra(
            G, source=equipment[from_], target=equipment[to_]
        )

        print(f"Path found (distance={dst}), plotting.")
        logger.info(f"Path from {from_} to {to_} found (distance={dst}).")
        plotting.plot_path(equipment, obstacles, path)
        plt.tight_layout()
    except helpers.nx.NetworkXNoPath:
        print("No path found, plotting.")
        logger.info(f"No path from {from_} to {to_} found.")
        plotting.plot_path(equipment, obstacles, [])
        plt.tight_layout()

    print("Finishing...")
    logger.info("Simulation finished.")
    plt.show()