from abc import ABC, abstractmethod
from enum import Enum

class HandlerStatus(Enum):
    CONTINUE = 1
    STOP = 2


class Handler(ABC):
    @abstractmethod
    def can_handle(self,update,state:str,order:dict) ->bool:...
    @abstractmethod
    def handle(self,update,state:str,order:dict) -> HandlerStatus: ...
        