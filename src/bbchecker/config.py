from configparser import ConfigParser

_REQUIRED_SECTIONS = ['bbdata', 'bot', 'flink', 'input']


class Config(ConfigParser):
    def __init__(self, filepath):
        # trick to keep comments on write, see https://stackoverflow.com/a/52306763
        super().__init__(comment_prefixes='⟶', allow_no_value=True)

        self._filepath = filepath
        self.read(filepath)

        for section in _REQUIRED_SECTIONS:
            if not self.has_section(section):
                raise Exception(f'Missing required section "{section}" in config file.')

    def persist(self):
        with open(self._filepath, 'w') as f:
            self.write(f)
