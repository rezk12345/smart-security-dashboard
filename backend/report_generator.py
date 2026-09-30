"""Generate daily/weekly security reports."""

from datetime import datetime
from typing import Any

from utils.file_utils import write_csv, write_json


class ReportGenerator:
    """Builds report files from aggregated threat data."""

    def build_report_payload(
        self,
        url_results: list[Any],
        email_results: list[Any],
        breach_summary: dict,
    ) -> dict:
        return {
            "generated_at": datetime.utcnow().isoformat(),
            "url_monitoring": {
                "total_urls": len(url_results),
                "high_risk_count": sum(1 for item in url_results if item.status == "high_risk"),
                "suspicious_count": sum(
                    1 for item in url_results if item.status == "suspicious"
                ),
            },
            "email_monitoring": {
                "total_emails": len(email_results),
                "phishing_likely_count": sum(
                    1 for item in email_results if item.status == "phishing_likely"
                ),
                "needs_review_count": sum(
                    1 for item in email_results if item.status == "needs_review"
                ),
            },
            "breach_tracking": breach_summary,
        }

    def save_daily_json(self, path, payload: dict) -> None:
        write_json(path, payload)

    def save_weekly_csv(self, path, payload: dict) -> None:
        rows = [
            {
                "metric": "total_urls",
                "value": payload["url_monitoring"]["total_urls"],
            },
            {
                "metric": "high_risk_urls",
                "value": payload["url_monitoring"]["high_risk_count"],
            },
            {
                "metric": "suspicious_urls",
                "value": payload["url_monitoring"]["suspicious_count"],
            },
            {
                "metric": "total_emails",
                "value": payload["email_monitoring"]["total_emails"],
            },
            {
                "metric": "phishing_likely_emails",
                "value": payload["email_monitoring"]["phishing_likely_count"],
            },
            {
                "metric": "needs_review_emails",
                "value": payload["email_monitoring"]["needs_review_count"],
            },
            {
                "metric": "total_breaches",
                "value": payload["breach_tracking"]["total_breaches"],
            },
            {
                "metric": "total_records_exposed",
                "value": payload["breach_tracking"]["total_records_exposed"],
            },
        ]
        write_csv(path, rows)
