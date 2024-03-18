from dataclasses import dataclass, field


@dataclass(frozen=True)
class Request:
    body: dict = field(default_factory=dict)
    params: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Response:
    status_code: int
    body: bytes
