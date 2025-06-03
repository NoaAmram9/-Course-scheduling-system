from abc import ABC, abstractmethod

class IFileManager(ABC):
    @abstractmethod
    def read_from_file(self):
        pass