from pydantic import BaseModel, Field
import re

class LogEntry(BaseModel):
    ipv4: str = Field(pattern=r'^(\d{1,3}\.){3}\d{1,3}$')
    ident: str = Field(pattern=r'^\w*|-$')
    auth_user: str = Field(pattern=r'^\w*|-$')
    timestamp: str = Field(pattern=r'^\[[0-9]{1,2}[\/.][a-zA-Z]{2,4}[\/.]\d{4}\:\d{1,2}\:\d{1,2}\:\d{1,2} \+\d{1,6}\]$')
    http_method: str = Field(pattern=r'^POST|GET|PUT|DELETE|OPTIONS$')
    url: str = Field(pattern=r'^\/[a-zA-Z?=0-9\/\.]*$')
    protocol: str = Field(pattern=r'^[A-Z]*$')
    protocol_version: str = Field(pattern=r'^[0-9]\.[0-9]$')
    status_code: str = Field(pattern=r'^\d{3}$')
    size_byte: str = Field(pattern=r'^\d*$')
    referer: str = Field(pattern=r'^[a-z0-9A-Z\.:\/?=а-я+\-]*$')
    user_agent: str = Field(pattern=r'^[\S ]*$')

    @classmethod
    def from_line(cls,
                  line: str,
                  pattern: re.Pattern) -> "LogEntry | None":
        """Фабричный метод для создания LogEntry из строки"""
        match = pattern.search(line)
        if not match:
            return None
        return cls(
            ipv4=match.group(1),
            ident=match.group(2),
            auth_user=match.group(3),
            timestamp=match.group(4),
            http_method=match.group(5),
            url=match.group(6),
            protocol=match.group(7),
            protocol_version=match.group(8),
            status_code=match.group(9),
            size_byte=match.group(10),
            referer=match.group(11),
            user_agent=match.group(12),
        )