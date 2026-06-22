from app.application.stages.base import PipelineStage
from multiprocessing import Queue
from collections import Counter

from app.domain_models.final_analysis_result import FinalAnalysisResult
from app.domain_models.partial_analysis_result import PartialAnalysisResult


class ResultAggregatorStage(PipelineStage):
    def __init__(self, input_queue: Queue, output_queue: Queue, analysis_worker: int):
        super().__init__('LogAnalysisResult', 1)
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.analysis_worker = analysis_worker
        self.final_report: FinalAnalysisResult | None = None

    def _target(self):
        completed_analyzers: int = 0
        total_entries: int = 0
        total_methods = Counter()
        total_status = Counter()
        total_referer = Counter()
        top_urls = Counter()
        top_ips = Counter()
        suspicious_ips_error = set()
        total_size_traffic: int = 0

        while completed_analyzers < self.analysis_worker:
            partial_analysis: PartialAnalysisResult = self.input_queue.get()
            if partial_analysis is None:
                completed_analyzers += 1
                continue
            total_entries += partial_analysis.count_entries
            total_size_traffic += partial_analysis.total_size
            suspicious_ips_error.update(partial_analysis.error_ips)
            total_methods.update(partial_analysis.counter_method)
            total_status.update(partial_analysis.counter_status)
            total_referer.update(partial_analysis.counter_referer)
            top_urls.update(partial_analysis.counter_url)
            top_ips.update(partial_analysis.counter_ip)

        self.final_report = FinalAnalysisResult(
            total_entries=total_entries,
            total_methods=total_methods,
            total_status=total_status,
            total_referer=total_referer,
            top_urls=top_urls,
            top_ips=top_ips,
            suspicious_ips_error=suspicious_ips_error,
            total_size_traffic=total_size_traffic
        )
        self.output_queue.put(self.final_report)

    def get_final_report(self, timeout: int = 10):
        return self.output_queue.get(timeout=timeout)