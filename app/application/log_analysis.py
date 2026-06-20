from app.application.base import PipelineStage
from multiprocessing import Queue, Process

class LogAnalyzerStage(PipelineStage):
    def __init__(self,
                 input_queue: Queue,
                 output_queue: Queue,
                 num_workers: int | None = None):
        super().__init__('LogAnalyzer')
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.num_workers = num_workers
        self._workers: list[Process] = []