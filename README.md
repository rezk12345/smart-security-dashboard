# Smart Security Dashboard

A modular Python project for basic cyber threat monitoring and visualization.

## Features

- Suspicious URL monitoring with rule-based checks
- Email phishing pattern detection
- Data breach tracking from mock/public-style datasets
- Automated daily/weekly report generation (JSON + CSV)
- Trend visualization with matplotlib charts
- Secure dashboard login (Flask session + password hashing)

## Project Structure

```
Smart Security Dashboard/
├── backend/
│   ├── __init__.py
│   ├── breach_tracker.py
│   ├── email_checker.py
│   ├── report_generator.py
│   ├── trend_visualizer.py
│   └── url_monitor.py
├── dashboard/
│   ├── __init__.py
│   ├── app.py
│   ├── static/
│   │   └── style.css
│   └── templates/
│       ├── dashboard.html
│       └── login.html
├── data/
│   ├── breach_sources.json
│   ├── sample_emails.txt
│   ├── sample_urls.csv
│   └── reports/
├── utils/
│   ├── __init__.py
│   ├── config.py
│   ├── file_utils.py
│   └── logger.py
├── main.py
└── requirements.txt
```

## Setup

1. Create and activate virtual environment:

```bash
python -m venv .venv
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Run full analysis pipeline

```bash
python main.py
```

This will:
- scan URLs from `data/sample_urls.csv`
- analyze emails from `data/sample_emails.txt`
- evaluate breach data from `data/breach_sources.json`
- generate summary reports in `data/reports/`
- generate charts in `data/reports/charts/`

### Run dashboard

```bash
python dashboard/app.py
```

Open `http://127.0.0.1:5000`

Default login credentials:
- Username: `admin`
- Password: `SmartSecure123!`

## Sample Output Files

- `data/reports/security_report_daily.json`
- `data/reports/security_report_weekly.csv`
- `data/reports/charts/threat_trend.png`
- `data/reports/charts/phishing_trend.png`

## Notes

- Public API integration can be added inside `backend/breach_tracker.py` and `backend/url_monitor.py` where hooks are already provided.
- Current implementation includes robust mock-data processing suitable for demo and GitHub upload.
