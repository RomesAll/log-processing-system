import os

from app.application.base import PipelineStage
from multiprocessing import Queue, Process
from collections import Counter

from app.domain_models.log_entry import LogEntry
from app.domain_models.partial_analysis_result import PartialAnalysisResult


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

    def start(self):
        for i in range(self.num_workers):
            p = Process(
                target=self._analyzer_worker,
                args=(i,),
                name=f'{self.name}_{i}'
            )
            p.start()
            self._workers.append(p)

    def _analyzer_worker(self):
        pid = os.getpid()
        print(f'{self.name} pid: {pid} запущен')
        while True:
            entries: list[LogEntry] = self.input_queue.get()
            if entries is None:
                print(f'{self.name} pid: {pid} получил стоп сигнал, обработано чанков: {processed_chunk}')
                self.output_queue.put(None)
                break
            counter_status = Counter()
            counter_url = Counter()
            referer = Counter()
            error_ips = set()
            count_entries = 0
            total_size = 0
            sample_entries = entries[:5]
            for entry in entries:
                counter_status[entry.status_code] += 1
                counter_url[entry.url] += 1
                referer[entry.referer] += 1
                count_entries += 1
                total_size += entry.size

                if entry.status_code == "500":
                    error_ips.add(entry.ip)

            result = PartialAnalysisResult(
                count_entries=count_entries,
                counter_url=counter_url,
                counter_status=counter_status,
                total_size=total_size,
                error_ips=error_ips,
                sample_entries=sample_entries,
            )
            self.output_queue.put(result)


    def join(self, timeout=None):
        for worker in self._workers:
            worker.join(timeout)