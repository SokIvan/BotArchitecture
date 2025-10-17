from abc import ABC, abstractmethod

class TextCommand(ABC):
    @abstractmethod
    def is_command(self,update_or_str) -> bool: ...
    
    @abstractmethod
    def command(self,update) -> bool: ...