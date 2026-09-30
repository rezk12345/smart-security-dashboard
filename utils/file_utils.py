"""File helper utilities for reading and writing project data."""

import csv
import json
from pathlib import Path
from typing import Any, Dict, List

from utils.logger import get_logger

logger = get_logger(__name__)


def read_csv(path: Path) -> List[Dict[str, str]]:
    try:
        with path.open("r", newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        logger.error("CSV file not found: %s", path)
        return []
    except Exception as exc:
        logger.exception("Failed reading CSV %s: %s", path, exc)
        return []


def read_text_lines(path: Path) -> List[str]:
    try:
        with path.open("r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        logger.error("Text file not found: %s", path)
        return []
    except Exception as exc:
        logger.exception("Failed reading text %s: %s", path, exc)
        return []


def read_json(path: Path) -> Dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        logger.error("JSON file not found: %s", path)
        return {}
    except json.JSONDecodeError as exc:
        logger.exception("Malformed JSON in %s: %s", path, exc)
        return {}
    except Exception as exc:
        logger.exception("Failed reading JSON %s: %s", path, exc)
        return {}


def write_json(path: Path, payload: Dict[str, Any]) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2)
    except Exception as exc:
        logger.exception("Failed writing JSON %s: %s", path, exc)


def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        if not rows:
            logger.warning("No rows to write for CSV %s", path)
            return
        fieldnames = list(rows[0].keys())
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    except Exception as exc:
        logger.exception("Failed writing CSV %s: %s", path, exc)
