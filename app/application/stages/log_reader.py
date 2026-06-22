from app.application.stages.base import PipelineStage
from multiprocessing import Queue
import os

class LogReaderStage(PipelineStage):

    def __init__(self,
                 filepath: str,
                 output_queue: Queue,
                 chunk_size: int = 5_000,
                 consumer_processes: int | None = None):
        super().__init__('LogReader', 1)
        self.filepath = filepath
        self.output_queue = output_queue
        self.chunk_size = chunk_size
        self.consumer_processes = consumer_processes or os.cpu_count()

    def _target(self):
        try:
            pid = os.getpid()
            with open(self.filepath) as file:
                chunk = []
                for line in file:
                    chunk.append(line.strip())
                    if len(chunk) >= self.chunk_size:
                        self.output_queue.put(chunk)
                        chunk = []
                if chunk:
                    self.output_queue.put(chunk)
        except FileNotFoundError:
            pass
        finally:
            for _ in range(self.consumer_processes):
                self.output_queue.put(None)