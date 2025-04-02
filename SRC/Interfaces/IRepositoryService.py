from abc import ABC, abstractmethod

class IDataService(ABC):
  
    @abstractmethod
    def read_courses_from_file(self, filename):
        """ Reads a file and converts it into a list of Course objects """
        pass
    
    @abstractmethod
    def write_courses_to_file(self, filename, courses):
        """ Writes a list of courses to a file in the required format """
        pass
    
    @abstractmethod
    def read_course_numbers_from_file(self, filename):
        """ Reads a file and converts it into a list of course numbers """
        pass
