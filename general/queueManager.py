import asyncio
from queue import Queue
from general.logger import logging

#region QueueManager
class QueueManager:
    queue = Queue()
    processing = False

    @classmethod
    async def process_queue(self):
        while not self.queue.empty():
            task = self.queue.get()
            await task()

        self.processing = False

    @classmethod
    def enqueue(self, task):
        self.queue.put(task)
        if not self.processing:
            asyncio.create_task(self.process_queue())
            self.processing = True
#endregion