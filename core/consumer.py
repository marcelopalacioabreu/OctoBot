#  Drakkar-Software OctoBot
#  Copyright (c) Drakkar-Software, All rights reserved.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3.0 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library.
import asyncio
from abc import ABCMeta, abstractmethod
from asyncio import Queue, Task

from tools import get_logger


class Consumer:
    __metaclass__ = ABCMeta

    def __init__(self, queue: Queue):
        self.logger = get_logger(self.__class__.__name__)

        self.queue: Queue = queue
        self.consume_task: Task = None
        self.should_stop: bool = False

    async def consume(self):
        """
        Should implement self.queue.get() in a while loop

        while not self.should_stop:
            await self.queue.get()

        :return:
        """
        while not self.should_stop:
            await self.perform(data=(await self.queue.get()))

    async def start(self):
        """
        Should be implemented for consumer's non-triggered tasks
        :return:
        """
        pass

    @abstractmethod
    async def perform(self, **kwargs):
        """
        Should implement consumer's non-triggered tasks
        Can be use to force producer to perform tasks
        :return:
        """
        pass

    async def stop(self):
        """
        Stops non-triggered tasks management
        :return:
        """
        self.should_stop = True

    def create_task(self):
        self.consume_task = asyncio.create_task(self.consume())

    async def run(self):
        await self.start()
        self.create_task()