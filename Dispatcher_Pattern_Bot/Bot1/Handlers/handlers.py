from abc import ABC, abstractmethod

class Handler(ABC):
    @abstractmethod
    def can_handle(self,update) ->bool:...
    @abstractmethod
    def handle(self,update) -> bool: ...
        