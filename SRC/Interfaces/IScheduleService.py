from abc import ABC, abstractmethod
from itertools import product

class IScheduleService(ABC):
    @abstractmethod
    def generate_schedules(self, courses: list) -> list:
        """
        Receives a list of courses and returns a list of possible schedules without conflicts.
        """
        pass