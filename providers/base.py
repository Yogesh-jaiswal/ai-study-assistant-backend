from abc import ABC, abstractmethod

class Provider(ABC):

    @abstractmethod
    def build(self, container):
        pass