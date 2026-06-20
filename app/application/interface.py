from abc import ABC

class PipelineStage(ABC):
    """Абстрактный класс для этапов обработки логов"""
    def __init__(self, name: str):
        self.name = name