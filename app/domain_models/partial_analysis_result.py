from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.domain_models.log_entry import LogEntry

@dataclass
class PartialAnalysisResult:
    count_entries: int = field(default=0)
    counter_url: dict[str, int] = field(default_factory=dict)
    counter_status: dict[str, int] = field(default_factory=dict)
    total_size: int = field(default=0)
    error_ips: list[str] = field(default_factory=list)
    sample_entries: list['LogEntry'] = field(default_factory=list)