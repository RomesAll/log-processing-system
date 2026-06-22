from app.application.stages.base import PipelineStage
from app.domain_models.log_entry import LogEntry
from multiprocessing import Queue
import os, re

PATTERN_LOG_STRING = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) (\w*|-) (\w*|-) (\[[\S ]*\]) \"(\w+) (\/\S*) (\w*)\/([0-9\.]*)\" (\d*) (\d*) \"(\S*)\" \"([\S ]*)\"')

class LogParserStage(PipelineStage):
    def __init__(self,
                 input_queue: Queue,
                 output_queue: Queue,
                 parse_pattern: re.Pattern = PATTERN_LOG_STRING,
                 worker_process: int | None = None):
        super().__init__('LogParser', worker_process)
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.parse_pattern = parse_pattern

    def _target(self):
        pid = os.getpid()
        processed_chunk: int = 0
        while True:
            row_chunk = self.input_queue.get()
            if row_chunk is None:
                self.output_queue.put(None)
                break
            parsed_entries = []
            for chunk in row_chunk:
                entry = LogEntry.from_line(
                    chunk,
                    self.parse_pattern,
                )
                if entry:
                    parsed_entries.append(entry)
            if parsed_entries:
                processed_chunk += 1
                self.output_queue.put(parsed_entries)