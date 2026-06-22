from pydantic import BaseModel, Field

class PartialAnalysisResult(BaseModel):
    count_entries: int = Field(default=0, ge=0)
    counter_url: dict[str, int] = Field(default_factory=dict)
    counter_status: dict[str, int] = Field(default_factory=dict)
    counter_ip: dict[str, int] = Field(default_factory=dict)
    counter_method: dict[str, int] = Field(default_factory=dict)
    counter_referer: dict[str, int] = Field(default_factory=dict)
    total_size: int = Field(default=0, ge=0)
    error_ips: set = Field(default_factory=set)