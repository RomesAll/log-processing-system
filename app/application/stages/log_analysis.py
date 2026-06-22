from app.application.stages.base import PipelineStage
from multiprocessing import Queue
from collections import Counter

from app.domain_models.log_entry import LogEntry
from app.domain_models.partial_analysis_result import PartialAnalysisResult
import os

class LogAnalyzerStage(PipelineStage):
    def __init__(self,
                 input_queue: Queue,
                 output_queue: Queue,
                 worker_process: int | None = None):
        super().__init__('LogAnalyzer', worker_process)
        self.input_queue = input_queue
        self.output_queue = output_queue

    def _target(self):
        pid = os.getpid()
        while True:
            entries: list[LogEntry] = self.input_queue.get()
            if entries is None:
                self.output_queue.put(None)
                break
            counter_ip = Counter()
            counter_status = Counter()
            counter_url = Counter()
            counter_referer = Counter()
            counter_method = Counter()
            error_ips = set()
            count_entries = 0
            total_size = 0
            for entry in entries:
                counter_status[entry.status_code] += 1
                counter_url[entry.url] += 1
                counter_referer[entry.referer] += 1
                counter_ip[entry.ipv4] += 1
                counter_method[entry.http_method] += 1
                count_entries += 1
                total_size += int(entry.size_byte)

                if entry.status_code == "500":
                    error_ips.add(entry.ipv4)

            result = PartialAnalysisResult(
                count_entries=count_entries,
                counter_url=counter_url,
                counter_status=counter_status,
                total_size=total_size,
                error_ips=error_ips,
                counter_ip=counter_ip,
                counter_referer=counter_referer,
                counter_method=counter_method,
            )
            self.output_queue.put(result)