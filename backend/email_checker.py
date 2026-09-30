"""Email phishing pattern detection."""

from dataclasses import dataclass

from utils.config import PHISHING_PATTERNS


@dataclass
class EmailScanResult:
    email_preview: str
    risk_score: int
    status: str
    matched_patterns: str


class EmailPhishingChecker:
    """Checks email text for common phishing indicators."""

    @staticmethod
    def analyze_email(content: str) -> EmailScanResult:
        text = content.lower()
        score = 0
        matches = []

        for pattern in PHISHING_PATTERNS:
            if pattern in text:
                score += 15
                matches.append(pattern)

        if "http://" in text or "bit.ly" in text or "tinyurl" in text:
            score += 20
            matches.append("Suspicious link format")

        if "dear customer" in text or "dear user" in text:
            score += 10
            matches.append("Generic greeting")

        if "!" in text and text.count("!") > 3:
            score += 5
            matches.append("Excessive urgency punctuation")

        status = "safe"
        if score >= 40:
            status = "phishing_likely"
        elif score >= 20:
            status = "needs_review"

        preview = content.replace("\n", " ").strip()[:80]
        return EmailScanResult(
            email_preview=preview + ("..." if len(content) > 80 else ""),
            risk_score=min(score, 100),
            status=status,
            matched_patterns=", ".join(matches) if matches else "None",
        )

    def analyze_bulk(self, emails: list[str]) -> list[EmailScanResult]:
        return [self.analyze_email(email) for email in emails]
