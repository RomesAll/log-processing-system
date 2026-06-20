from datetime import datetime, timezone
import json
from dataclasses import dataclass, field

@dataclass
class FinalAnalysisResult:
    total_entries: int = field(default=0)
    total_status: dict[str, int] = field(default_factory=dict)
    top_urls: dict[str, int] = field(default_factory=dict)
    top_ips: list = field(default_factory=list)
    suspicious_ips_error: dict[str, int] = field(default_factory=dict)
    total_size_traffic: float = field(default=0.0)
    sample_entries: list[dict] = field(default_factory=list)
    processing_time_seconds: float = field(default=0.0)

    def to_json(self, filepath: str) -> None:
        """Сохранение отчета в json-файл"""
        report_dict = {
            'report_metadata':{
                'generated_at': datetime.now(tz=timezone.utc),
                'total_entries': self.total_entries,
                'processing_time_seconds': self.processing_time_seconds,
            },
            'total_status': self.total_status,
            'top_urls': self.top_urls,
            'top_ips': self.top_ips,
            'suspicious_ips_error': self.suspicious_ips_error,
            'total_size_traffic': self.total_size_traffic,
            'sample_entries': self.sample_entries,
        }
        json.dump(report_dict, open(filepath, "w", encoding="utf-8"), indent=4)
