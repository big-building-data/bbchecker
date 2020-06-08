from configparser import ConfigParser


class Config(ConfigParser):
    def __init__(self, filepath):
        super().__init__()

        self._filepath = filepath
        self.read(filepath)

    def persist(self):
        with open(self._filepath, 'w') as f:
            self.write(f)
