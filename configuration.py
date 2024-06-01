import file_operations as fo

from entities import Entity

class Configuration:
    
    def __init__(self, equipment=None, obstacles=None):
        self._equipment = equipment
        self._obstacles = obstacles

    def load(self, filename: str):
        self._equipment, self._obstacles = fo.read_configuration_csv(filename)

    @property
    def equipment(self) -> list[Entity]:
        return self._equipment
    
    @property
    def obstacles(self) -> list[Entity]:
        return self._obstacles