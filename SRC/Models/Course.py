class Course:
    def __init__(self, name: str = "", code: str = "", lectures: list = None, exercises: list = None, labs: list = None):
        self._name = name  # שם הקורס
        self._code = code  # קוד הקורס
        self._lectures = lectures if lectures else []  # רשימת הרצאות בקורס
        self._exercises = exercises if exercises else []  # רשימת תרגולים בקורס
        self._labs = labs if labs else []  # רשימת מעבדות בקורס

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
