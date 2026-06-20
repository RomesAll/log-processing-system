from abc import ABC, abstractmethod
from multiprocessing import Process

class PipelineStage(ABC):
    """Абстрактный класс для этапов обработки логов"""
    def __init__(self, name: str):
        self.name = name
        self.process: Process | None = None

    @abstractmethod
    def start(self):
        pass

    def join(self):
        if self.process:
            self.process.join()

    def terminate(self):
        if self.process and self.process.is_alive():
            self.process.terminate()
            self.process.join(timeout=10)