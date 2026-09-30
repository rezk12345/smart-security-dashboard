"""Data breach tracking logic using local/public-style datasets."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class BreachRecord:
    company: str
    breach_date: str
    records_exposed: int
    severity: str


class BreachTracker:
    """Analyzes breach entries and computes severity."""

    @staticmethod
    def _severity_from_records(records_exposed: int) -> str:
        if records_exposed >= 1_000_000:
            return "critical"
        if records_exposed >= 100_000:
            return "high"
        if records_exposed >= 10_000:
            return "medium"
        return "low"

    def process_entries(self, entries: list[dict]) -> list[BreachRecord]:
        records: list[BreachRecord] = []
        for item in entries:
            company = str(item.get("company", "Unknown"))
            breach_date = str(item.get("breach_date", datetime.utcnow().date()))
            records_exposed = int(item.get("records_exposed", 0))
            severity = item.get("severity") or self._severity_from_records(records_exposed)

            records.append(
                BreachRecord(
                    company=company,
                    breach_date=breach_date,
                    records_exposed=records_exposed,
                    severity=str(severity),
                )
            )
        return records

    def summary(self, records: list[BreachRecord]) -> dict:
        counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        for record in records:
            if record.severity in counts:
                counts[record.severity] += 1

        return {
            "total_breaches": len(records),
            "total_records_exposed": sum(r.records_exposed for r in records),
            "severity_breakdown": counts,
        }
