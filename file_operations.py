import csv
from entities import *

def read_configuration_csv(filename: str) -> tuple[list[Entity], list[Entity]]:
    loader_f_mapping = {
        'UE': create_user_equipment,
        'C': create_circular_antenna,
        'Y': create_yagi_antenna,
        'R': create_rectangular_obstacle
    }
    equipment, obstacles = [], []
    with open(filename) as f:
        csvreader = csv.reader(f)
        id_ = 0
        for row in csvreader:
            kind = row[0]
            id_ += 1
            match kind:
                case 'UE':
                    row = np.float_(row[1:])
                    location = row[0:2]
                    ue_params = row[2:]
                    equipment.append(loader_f_mapping[kind](
                        id_, location, *list(ue_params)))
                case 'A':
                    antenna_type = row[1]
                    row = np.float_(row[2:])
                    location = row[0:2]
                    antenna_params = row[2:]
                    equipment.append(loader_f_mapping[antenna_type](
                        id_, location, *list(antenna_params)))
                case 'O':
                    obstacle_type = row[1]
                    row = np.float_(row[2:])
                    center = row[0:2]
                    obstacles.append(loader_f_mapping[obstacle_type](
                        id_, tuple(center), *list(row[2:])
                    ))

    return equipment, obstacles
