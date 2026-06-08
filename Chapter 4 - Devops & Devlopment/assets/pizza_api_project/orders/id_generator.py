from abc import ABC, abstractmethod
from uuid import uuid4


class IdGenerator(ABC):
    @abstractmethod
    def generate_id(self) -> int:
        ...
        
class UUIDGenerator(IdGenerator):
    def generate_id(self) -> int:
        return uuid4().int
    
    