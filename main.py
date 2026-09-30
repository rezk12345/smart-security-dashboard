"""Entry point for running the Smart Security Dashboard backend pipeline."""

from backend.breach_tracker import BreachTracker
from backend.email_checker import EmailPhishingChecker
from backend.report_generator import ReportGenerator
from backend.trend_visualizer import TrendVisualizer
from backend.url_monitor import URLMonitor
from utils.config import CHART_DIR, DATA_DIR, REPORT_DIR
from utils.file_utils import read_csv, read_json, read_text_lines
from utils.logger import get_logger

logger = get_logger(__name__)


def run_pipeline() -> dict:
    logger.info("Starting Smart Security Dashboard pipeline")
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    url_rows = read_csv(DATA_DIR / "sample_urls.csv")
    urls = [row.get("url", "").strip() for row in url_rows if row.get("url")]
    url_results = URLMonitor().scan_bulk(urls)

    emails = read_text_lines(DATA_DIR / "sample_emails.txt")
    email_results = EmailPhishingChecker().analyze_bulk(emails)

    breach_data = read_json(DATA_DIR / "breach_sources.json")
    breach_entries = breach_data.get("breaches", [])
    breach_tracker = BreachTracker()
    breach_records = breach_tracker.process_entries(breach_entries)
    breach_summary = breach_tracker.summary(breach_records)

    report_generator = ReportGenerator()
    report_payload = report_generator.build_report_payload(
        url_results, email_results, breach_summary
    )

    report_generator.save_daily_json(REPORT_DIR / "security_report_daily.json", report_payload)
    report_generator.save_weekly_csv(REPORT_DIR / "security_report_weekly.csv", report_payload)

    TrendVisualizer.create_bar_chart(
        {
            "safe": sum(1 for item in url_results if item.status == "safe"),
            "suspicious": sum(1 for item in url_results if item.status == "suspicious"),
            "high_risk": sum(1 for item in url_results if item.status == "high_risk"),
        },
        "URL Threat Trend",
        CHART_DIR / "threat_trend.png",
    )

    TrendVisualizer.create_bar_chart(
        {
            "safe": sum(1 for item in email_results if item.status == "safe"),
            "needs_review": sum(1 for item in email_results if item.status == "needs_review"),
            "phishing_likely": sum(
                1 for item in email_results if item.status == "phishing_likely"
            ),
        },
        "Phishing Email Trend",
        CHART_DIR / "phishing_trend.png",
    )

    logger.info("Pipeline completed successfully")
    return report_payload


if __name__ == "__main__":
    output = run_pipeline()
    print("Security pipeline complete.")
    print(output)
