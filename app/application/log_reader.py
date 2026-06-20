from app.application.base import PipelineStage
from multiprocessing import Queue
import os

class LogReaderStage(PipelineStage):

    def __init__(self, filepath: str, output_queue: Queue,
                 chunk_size: int = 10_000, num_consumer: int | None = None):
        super().__init__('LogReader')
        self.filepath = filepath
        self.output_queue = output_queue
        self.chunk_size = chunk_size
        self.num_consumer = num_consumer or os.cpu_count()

