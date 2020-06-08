# -*- coding: utf-8 -*-

from pytgbot import Bot

from .config import Config

PAUSE_COMMANDS = ['pause', 'stop']
START_COMMANDS = ['start', 'resume']


class BBBot:

    def __init__(self, config: Config):
        """Create a bot using the config. Required keys: bot.key, bot.running, bot.chat_id, bot.offset"""
        self.config = config
        self.running = config.get('bot', 'running') == 'True'

        self._bot = Bot(config.get('bot', 'key'))
        self._chat_id = int(config.get('bot', 'chat_id'))

        self.consume_messages()

    def consume_messages(self):
        offset = int(self.config.get('bot', 'offset'))
        for msg in self._bot.do('getUpdates', offset=offset, request_timeout=100):
            if 'channel_post' in msg and msg['channel_post']['chat']['id'] == self._chat_id \
                    and 'text' in msg['channel_post']:
                text = msg['channel_post']['text'].lower()
                if text in PAUSE_COMMANDS:
                    self.running = False
                elif text in START_COMMANDS:
                    self.running = True

            offset = msg['update_id']

        self.config.set('bot', 'running', str(self.running))
        self.config.set('bot', 'offset', str(offset))
        self.config.persist()

    def send_message(self, message: str, formatting='HTML'):
        self._bot.send_message(self._chat_id, message, parse_mode=formatting)
