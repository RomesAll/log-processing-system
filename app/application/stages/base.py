import os
from abc import ABC, abstractmethod
from multiprocessing import Process


class PipelineStage(ABC):
    """Абстрактный класс для этапов обработки логов"""
    def __init__(self,
                 name: str,
                 worker_process: int | None = None):
        self.name = name
        self.worker_processes = worker_process or 1
        self.processes: list[Process] = []

    @abstractmethod
    def _target(self):
        pass

    def start(self):
        for i in range(self.worker_processes):
            p = Process(
                target=self._target,
                name=f'{self.name}_worker_{i}'
            )
            p.start()
            self.processes.append(p)

    def join(self, timeout=None):
        if self.processes:
            for process in self.processes:
                process.join(timeout)

    def terminate(self, timeout=10):
        if not self.processes:
            return
        for process in self.processes:
            if process and process.is_alive():
                process.terminate()
                process.join(timeout=timeout)