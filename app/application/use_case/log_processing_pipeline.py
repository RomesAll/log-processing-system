import os
import time
from multiprocessing import Queue
from app.application.stages.base import PipelineStage
from app.application.stages.log_analysis import LogAnalyzerStage
from app.application.stages.log_analysis_result import ResultAggregatorStage
from app.application.stages.log_parser import LogParserStage
from app.application.stages.log_reader import LogReaderStage


class LogProcessingPipeline:
    def __init__(self,
                 file_path: str,
                 count_reader_workers: int | None = None,
                 count_parser_workers: int | None = None):
        self.file_path = file_path
        self.count_parser_workers = count_reader_workers or os.cpu_count()
        self.count_analyzer_workers = count_parser_workers or os.cpu_count()

        self.q_raw_chunk = Queue()
        self.q_entries = Queue()
        self.q_partial_analysis = Queue()
        self.q_final_report = Queue()

        self.stages: list[PipelineStage] = []
        self.aggregator: ResultAggregatorStage | None = None

    def build(self):
        self.stages.append(
            LogReaderStage(
                filepath=self.file_path,
                output_queue=self.q_raw_chunk,
                chunk_size=10_000,
                consumer_processes=self.count_parser_workers
            )
        )
        self.stages.append(
            LogParserStage(
                input_queue=self.q_raw_chunk,
                output_queue=self.q_entries,
                worker_process=self.count_parser_workers
            )
        )
        self.stages.append(
            LogAnalyzerStage(
                input_queue=self.q_entries,
                output_queue=self.q_partial_analysis,
                worker_process=self.count_analyzer_workers
            )
        )
        self.aggregator = ResultAggregatorStage(
            input_queue=self.q_partial_analysis,
            output_queue=self.q_final_report,
            analysis_worker=self.count_analyzer_workers
        )

    def run(self):
        start_time = time.time()
        self.build()
        self.aggregator.start()

        for stage in reversed(self.stages):
            stage.start()
            time.sleep(0.1)

        for stage in self.stages:
            stage.join()

        self.aggregator.join()

        end_time = time.time()
        processing_time = end_time - start_time

        report = self.aggregator.get_final_report(timeout=10)
        if report:
            report.processing_time_seconds = processing_time

        return report

    def cleanup(self):
        for stage in self.stages:
            stage.terminate()
        if self.aggregator:
            self.aggregator.terminate()
