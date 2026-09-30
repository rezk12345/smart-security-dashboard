"""Flask dashboard for Smart Security Dashboard."""

import sys
from pathlib import Path

from flask import Flask, redirect, render_template, request, send_from_directory, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

# Ensure project root imports work when running this file directly.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from main import run_pipeline  # noqa: E402
from utils.config import CHART_DIR, DEFAULT_PASSWORD, DEFAULT_USERNAME, REPORT_DIR  # noqa: E402
from utils.file_utils import read_json  # noqa: E402

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "replace-this-secret-in-production"

USERS = {
    DEFAULT_USERNAME: generate_password_hash(DEFAULT_PASSWORD),
}


def is_authenticated() -> bool:
    return bool(session.get("authenticated"))


@app.route("/", methods=["GET"])
def index():
    if not is_authenticated():
        return redirect(url_for("login"))
    return redirect(url_for("dashboard"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        stored_hash = USERS.get(username)
        if stored_hash and check_password_hash(stored_hash, password):
            session["authenticated"] = True
            session["username"] = username
            return redirect(url_for("dashboard"))
        error = "Invalid username or password"
    return render_template("login.html", error=error)


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if not is_authenticated():
        return redirect(url_for("login"))

    if request.method == "POST":
        run_pipeline()

    report = read_json(REPORT_DIR / "security_report_daily.json")
    return render_template(
        "dashboard.html",
        report=report,
        username=session.get("username", DEFAULT_USERNAME),
        has_report=bool(report),
    )


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/charts/<path:filename>", methods=["GET"])
def chart_file(filename: str):
    return send_from_directory(CHART_DIR, filename)


if __name__ == "__main__":
    app.run(debug=True)
