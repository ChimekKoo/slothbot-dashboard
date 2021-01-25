class Level:
    def __init__(self, name):
        self.name = name.upper()

    def __str__(self):
        return self.name


DEBUG = Level("DEBUG")
INFO = Level("INFO")
WARNING = Level("WARNING")
ERROR = Level("ERROR")
FATAL = Level("FATAL")
