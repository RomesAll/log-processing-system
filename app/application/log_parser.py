from app.application.base import PipelineStage
from multiprocessing import Queue, Process
import os, re

class LogParserStage(PipelineStage):
    def __init__(self,
                 input_queue: Queue,
                 output_queue: Queue,
                 parse_pattern: re.Pattern,
                 num_workers: int | None = None):
        super().__init__('LogParser')
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.num_workers = num_workers or os.cpu_count()
        self._workers: list[Process] = []
        self.parse_pattern = parse_pattern