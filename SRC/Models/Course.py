class Course:
      
    def __init__(self, name: str = "", code: str = "", semester: int = 0, lectures: list = None, exercises: list = None, labs: list = None, departmentHours: list = None, reinforcement: list = None, traning: list = None, notes:str = ""):
        self._name = name  # course name
        self._code = code  # course number
        self._semester = semester  # course semester
        self._lectures = lectures if lectures is not None else []  # list of lectures in the course
        self._exercises = exercises if exercises is not None else []  # list of exercises in the course
        self._labs = labs if labs is not None else []  # list of labs in the course
        self._departmentHours = departmentHours if departmentHours is not None else []  # department hours
        self._reinforcement = reinforcement if reinforcement is not None else []  # reinforcement sessions
        self._traning = traning if traning is not None else []  # training sessions
        self._notes =  notes  

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = value

    @property
    def semester(self):
        return self._semester

    @semester.setter
    def semester(self, value):
        self._semester = value

    @property
    def lectures(self):
        return self._lectures

    @lectures.setter
    def lectures(self, value):
        self._lectures = value

    @property
    def exercises(self):
        return self._exercises

    @exercises.setter
    def exercises(self, value):
        self._exercises = value

    @property
    def labs(self):
        return self._labs

    @labs.setter
    def labs(self, value):
        self._labs = value

    @property
    def departmentHours(self):
        return self._departmentHours

    @departmentHours.setter
    def departmentHours(self, value):
        self._departmentHours = value

    @property
    def reinforcement(self):
        return self._reinforcement

    @reinforcement.setter
    def reinforcement(self, value):
        self._reinforcement = value

    @property
    def traning(self):
        return self._traning

    @traning.setter
    def traning(self, value):
        self._traning = value
  

