import nest_asyncio
nest_asyncio.apply()
from queue import Queue

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
            nest_asyncio.asyncio.create_task(self.process_queue())
            self.processing = True
#endregion