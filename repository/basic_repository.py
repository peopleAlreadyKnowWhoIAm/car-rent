from abc import ABC, abstractmethod
from constants import ABCSingletonMeta


class BasicRepository(ABC, metaclass=ABCSingletonMeta):
    @abstractmethod
    def get_all_entities(self):
        pass

    @abstractmethod
    def get_entity_by_id(self, entity_id: int):
        pass

    @abstractmethod
    def add_entity(self, **kwargs):
        pass

    @abstractmethod
    def update_entity(self, entity_id: int, **kwargs):
        pass

    @abstractmethod
    def delete_entity(self, entity_id: int):
        pass
