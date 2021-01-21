from logger import levels
from datetime import datetime


class Logger:
    def __init__(self, file: str, debug: bool = False):
        self.debug = debug
        self.file = file

    def write(self, text: str, fileout: bool, level: levels.Level = levels.INFO):
        if not (level == levels.DEBUG and not self.debug):
            now = datetime.now().strftime("%Y-%m-%dT%H-%M-%SZ")
            content = f"{now} => {str(level)}: {text}\n"
            print(content, end="")
            if fileout:
                with open(self.file, "a") as log_file:
                    log_file.write(content)
                    log_file.close()
