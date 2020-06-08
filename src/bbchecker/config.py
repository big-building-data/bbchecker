from configparser import ConfigParser

_REQUIRED_SECTIONS = ['bbdata', 'bot', 'flink', 'input']


class Config(ConfigParser):
    def __init__(self, filepath):
        super().__init__()

        self._filepath = filepath
        self.read(filepath)

        for section in _REQUIRED_SECTIONS:
            if not self.has_section(section):
                raise Exception(f'Missing required section "{section}" in config file.')

    def persist(self):
        with open(self._filepath, 'w') as f:
            self.write(f)
