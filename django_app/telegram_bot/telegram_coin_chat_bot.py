import time
from pprint import pprint

import telepot

from config.settings.base import config_secret_common
token = config_secret_common['telegram']['access_key']


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    pprint(msg)
    if content_type == 'text':
        bot.sendMessage(chat_id, msg['text'])


bot = telepot.Bot(token)
bot.message_loop(handle)
print('대기중...')

while 1:
    time.sleep(10)
