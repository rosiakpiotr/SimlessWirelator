import logging

import matplotlib.pyplot as plt
import obstacle_casting
import plotting
import helpers
from configuration import Configuration

logger = logging.getLogger(__name__)


def run_through_configuration(conf: Configuration, from_: int, to_: int):
    plt.close("all")
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

    from_to_str = f'from [no. {from_+1} - {equipment[from_]}] to [no. {to_+1} - {equipment[to_]}]'
    try:
        logger.info(f"Finding path {from_to_str}...")
        dst, path = helpers.nx.single_source_dijkstra(
            G, source=equipment[from_], target=equipment[to_]
        )

        path_stringified = " -> ".join([str(eq) for eq in path])
        path_log_msg = f"Path {from_to_str} found [{path_stringified}] (distance={dst:.2f})."
        print(path_log_msg)
        logger.info(path_log_msg)
        plotting.plot_path(equipment, obstacles, path, path_stringified)
        plt.tight_layout()
    except helpers.nx.NetworkXNoPath:
        print("No path found, plotting.")
        logger.info(f"No path {from_to_str} found.")
        plotting.plot_path(equipment, obstacles, [])
        plt.tight_layout()

    print("Finishing...")
    logger.info("Simulation finished.")
    plt.show()
