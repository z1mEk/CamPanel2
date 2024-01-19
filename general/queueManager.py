import nest_asyncio
nest_asyncio.apply()
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
            logging.info(f"wlazłow queue1")
            await task()

        self.processing = False

    @classmethod
    def enqueue(self, task):
        self.queue.put(task)
        if not self.processing:
            nest_asyncio.asyncio.create_task(self.process_queue())
            logging.info(f"wlazłow queue2")
            self.processing = True
#endregion