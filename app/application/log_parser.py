from app.application.base import PipelineStage
from app.domain_models.log_entry import LogEntry
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

    def start(self):
        for i in range(self.num_workers):
            p = Process(target=self._parser_worker, name=f'{self.name}_{i}')
            p.start()
            self._workers.append(p)

    def _parser_worker(self):
        pid = os.getpid()
        processed_chunk: int = 0
        print(f'{self.name} pid: {pid} запущен')
        while True:
            row_chunk = self.input_queue.get()
            if row_chunk is None:
                print(f'{self.name} pid: {pid} получил стоп сигнал, обработано чанков: {processed_chunk}')
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

    def join(self, timeout=None):
        for p in self._workers:
            p.join(timeout)