from abc import ABC, abstractmethod
from typing import Dict

from constants import ABCSingletonMeta


class BasicController(ABC, metaclass=ABCSingletonMeta):
    @abstractmethod
    def get_all_entities(self) -> Dict:
        pass

    @abstractmethod
    def get_entity_by_id(self, entity_id: int) -> Dict:
        pass

    @abstractmethod
    def add_entity(self, **kwargs) -> Dict:
        pass

    @abstractmethod
    def update_entity(self, entity_id: int, **kwargs) -> Dict:
        pass

    @abstractmethod
    def delete_entity(self, entity_id: int) -> Dict:
        pass
