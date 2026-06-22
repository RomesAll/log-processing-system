from datetime import datetime, timezone
import json
from pydantic import BaseModel, Field

class FinalAnalysisResult(BaseModel):
    total_entries: int = Field(default=0, ge=0)
    total_methods: dict[str, int] = Field(default_factory=dict)
    total_status: dict[str, int] = Field(default_factory=dict)
    total_referer: dict[str, int] = Field(default_factory=dict)
    top_urls: dict[str, int] = Field(default_factory=dict)
    top_ips: dict[str, int] = Field(default_factory=dict)
    suspicious_ips_error: set = Field(default_factory=set)
    total_size_traffic: int = Field(default=int, ge=0)
    processing_time_seconds: float = Field(default=0.0)

    def to_json(self, filepath: str) -> None:
        """Сохранение отчета в json-файл"""
        report_dict = {
            'report_metadata':{
                'generated_at': datetime.now(tz=timezone.utc),
                'total_entries': self.total_entries,
                'processing_time_seconds': self.processing_time_seconds,
            },
            'total_referer': self.total_referer,
            'total_methods': self.total_methods,
            'total_status': self.total_status,
            'top_urls': self.top_urls,
            'top_ips': self.top_ips,
            'suspicious_ips_error': self.suspicious_ips_error,
            'total_size_traffic': self.total_size_traffic,
        }
        json.dump(report_dict, open(filepath, "w", encoding="utf-8"), indent=4)
