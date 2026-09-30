"""URL monitoring and suspicious link detection."""

from dataclasses import dataclass
from urllib.parse import urlparse

from utils.config import SUSPICIOUS_URL_KEYWORDS


@dataclass
class URLScanResult:
    url: str
    risk_score: int
    status: str
    reasons: str


class URLMonitor:
    """Basic rule-based detector for suspicious URLs."""

    @staticmethod
    def scan_url(url: str) -> URLScanResult:
        score = 0
        reasons = []

        parsed = urlparse(url)
        host = parsed.netloc.lower()
        path = parsed.path.lower()
        full = f"{host}{path}"

        if parsed.scheme != "https":
            score += 20
            reasons.append("Non-HTTPS protocol")

        if host.count("-") >= 2:
            score += 15
            reasons.append("Hyphen-heavy domain")

        if len(host) > 30:
            score += 10
            reasons.append("Unusually long domain")

        for keyword in SUSPICIOUS_URL_KEYWORDS:
            if keyword in full:
                score += 8
                reasons.append(f"Suspicious keyword: {keyword}")

        if any(char.isdigit() for char in host):
            score += 8
            reasons.append("Numeric domain usage")

        status = "safe"
        if score >= 40:
            status = "high_risk"
        elif score >= 20:
            status = "suspicious"

        return URLScanResult(
            url=url,
            risk_score=min(score, 100),
            status=status,
            reasons=", ".join(reasons) if reasons else "No strong indicators",
        )

    def scan_bulk(self, urls: list[str]) -> list[URLScanResult]:
        return [self.scan_url(url) for url in urls]
