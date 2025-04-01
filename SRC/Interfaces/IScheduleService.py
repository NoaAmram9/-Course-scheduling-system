from abc import ABC, abstractmethod
from itertools import product

class IScheduleService(ABC):
    @abstractmethod
    def generate_schedules(self, courses: list) -> list:
        """
        מקבלת רשימה של קורסים ומחזירה רשימה של מערכות שעות אפשריות ללא התנגשויות.
        """
        pass