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