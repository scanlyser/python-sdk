from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Generic, TypeVar

T = TypeVar("T")


class ScanStatus(StrEnum):
    PENDING = "pending"
    CRAWLING = "crawling"
    ANALYSING = "analysing"
    COMPLETED = "completed"
    FAILED = "failed"
    RESCANNING = "rescanning"


class WcagLevel(StrEnum):
    A = "A"
    AA = "AA"
    AAA = "AAA"


class IssueCategory(StrEnum):
    WCAG = "wcag"
    SEO = "seo"
    PERFORMANCE = "performance"
    UX = "ux"
    SITEWIDE = "sitewide"
    OTHER = "other"


class IssueSeverity(StrEnum):
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"
    INFO = "info"


@dataclass(frozen=True)
class Team:
    id: str
    name: str
    personal_team: bool
    created_at: str
    updated_at: str

    @classmethod
    def from_dict(cls, data: dict) -> Team:
        return cls(
            id=data["id"],
            name=data["name"],
            personal_team=data["personal_team"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )


@dataclass(frozen=True)
class ScanScores:
    overall: float
    wcag: float
    seo: float
    performance: float
    ux: float
    sitewide: float
    other: float

    @classmethod
    def from_dict(cls, data: dict) -> ScanScores:
        return cls(
            overall=float(data["overall"]),
            wcag=float(data["wcag"]),
            seo=float(data["seo"]),
            performance=float(data["performance"]),
            ux=float(data["ux"]),
            sitewide=float(data["sitewide"]),
            other=float(data["other"]),
        )


@dataclass(frozen=True)
class Scan:
    id: str
    site_id: str
    status: ScanStatus
    wcag_level: WcagLevel
    pages_crawled: int
    pages_total: int
    issues_count: int
    created_at: str
    scores: ScanScores | None = None
    completed_at: str | None = None
    failed_at: str | None = None
    failure_reason: str | None = None

    @property
    def is_terminal(self) -> bool:
        return self.status in (ScanStatus.COMPLETED, ScanStatus.FAILED)

    @classmethod
    def from_dict(cls, data: dict) -> Scan:
        return cls(
            id=data["id"],
            site_id=data["site_id"],
            status=ScanStatus(data["status"]),
            wcag_level=WcagLevel(data["wcag_level"]),
            pages_crawled=data["pages_crawled"],
            pages_total=data["pages_total"],
            issues_count=data["issues_count"],
            scores=ScanScores.from_dict(data["scores"]) if data.get("scores") else None,
            created_at=data["created_at"],
            completed_at=data.get("completed_at"),
            failed_at=data.get("failed_at"),
            failure_reason=data.get("failure_reason"),
        )


@dataclass(frozen=True)
class Site:
    id: str
    name: str
    url: str
    created_at: str
    updated_at: str
    latest_scan: Scan | None = None
    scans_count: int | None = None

    @classmethod
    def from_dict(cls, data: dict) -> Site:
        return cls(
            id=data["id"],
            name=data["name"],
            url=data["url"],
            latest_scan=Scan.from_dict(data["latest_scan"]) if data.get("latest_scan") else None,
            scans_count=data.get("scans_count"),
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )


@dataclass(frozen=True)
class Issue:
    type: str
    category: IssueCategory
    severity: IssueSeverity
    message: str
    url: str
    culprits: list[str] = field(default_factory=list)
    help_url: str | None = None

    @classmethod
    def from_dict(cls, data: dict) -> Issue:
        return cls(
            type=data["type"],
            category=IssueCategory(data["category"]),
            severity=IssueSeverity(data["severity"]),
            message=data["message"],
            url=data["url"],
            culprits=data.get("culprits", []),
            help_url=data.get("help_url"),
        )


@dataclass(frozen=True)
class ScanPage:
    id: str
    url: str
    status: ScanStatus
    issues_count: int
    completed_at: str | None = None
    issues: list[Issue] | None = None

    @classmethod
    def from_dict(cls, data: dict) -> ScanPage:
        return cls(
            id=data["id"],
            url=data["url"],
            status=ScanStatus(data["status"]),
            issues_count=data["issues_count"],
            issues=[Issue.from_dict(issue) for issue in data["issues"]] if data.get("issues") else None,
            completed_at=data.get("completed_at"),
        )


@dataclass(frozen=True)
class PaginatedResponse(Generic[T]):
    data: list[T]
    current_page: int
    per_page: int
    total: int
    last_page: int
