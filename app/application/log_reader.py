from app.application.base import PipelineStage
from multiprocessing import Queue, Process
import os

class LogReaderStage(PipelineStage):

    def __init__(self, filepath: str, output_queue: Queue,
                 chunk_size: int = 5_000, num_consumer: int | None = None):
        super().__init__('LogReader')
        self.filepath = filepath
        self.output_queue = output_queue
        self.chunk_size = chunk_size
        self.num_consumer = num_consumer or os.cpu_count()

    def start(self):
        self.process = Process(target=self._read_file, name=self.name)
        self.process.start()

    def _read_file(self):
        print(f"[{self.name}] запущен в процессе {os.getpid()}")
        try:
            with open(self.filepath) as file:
                chunk = []
                for line in file:
                    chunk.append(line.strip())
                    if len(chunk) >= self.chunk_size:
                        self.output_queue.put(chunk)
                        chunk = []
                if chunk:
                    self.output_queue.put(chunk)
        except FileNotFoundError:
            print(f"[ERROR] {self.name}]: файл не найден - {self.filepath}")
        finally:
            for _ in range(self.num_consumer):
                self.output_queue.put(None)
            print(f"[OK] обработка в процессе {os.getpid()} завершена, "
                  f"передано {self.num_consumer} стоп-сигналов")