from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):

    def __init__(self, name: str):
        self.name = name
    
        #Main execution method for all agents.
        
    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
       
        pass