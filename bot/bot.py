#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports
import os
from random import randint

import vk_api
from dotenv import load_dotenv
# import vk_api.bot_longpoll
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

# # Настройка окружения
load_dotenv()
GROUP_NUMBER = os.getenv('GROUP_NUMBER')
TOKEN_API_VK = os.getenv('TOKEN_API_VK')


class Bot:
    def __init__(self, group_id, token):
        self.token = token
        self.group_id = group_id
        self.vk = vk_api.VkApi(token=token)
        self.api = self.vk.get_api()

        self.long_poller = VkBotLongPoll(self.vk, group_id=self.group_id)

    def run(self):
        for event in self.long_poller.listen():
            # print('Получено событие:')
            try:
                self.on_event(event)
            except Exception as err:
                print(err)

    def on_event(self, event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            self.api.messages.send(
                random_id=randint(1, 2 ** 20),
                message=event.obj.message['text'],
                peer_id=event.message.peer_id,
            )
        else:
            print('Не знаю что за событие', event.type)


if __name__ == '__main__':
    bot = Bot(GROUP_NUMBER, TOKEN_API_VK)
    bot.run()
