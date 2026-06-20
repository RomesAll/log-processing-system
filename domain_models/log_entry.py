from dataclasses import dataclass
import re

@dataclass
class LogEntry:
    ip: str
    timestamp: str
    http_method: str
    url: str
    status_code: int
    size: int
    referer: str
    user_agent: str

    @classmethod
    def from_line(cls, line: str, pattern: re.Pattern) -> "LogEntry | None":
        """Фабричный метод для создания LogEntry из строки"""
        match = pattern.search(line)
        if not match:
            return None
        return cls(
            ip = match.group(0),
            timestamp = match.group(1),
            http_method = match.group(2),
            url = match.group(3),
            status_code = match.group(4),
            size = match.group(5),
            referer = match.group(6),
            user_agent = match.group(7),
        )