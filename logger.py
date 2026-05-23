import logging
import json
import os
import datetime
import urllib.request

class ELKHandler(logging.Handler):
    """Sends log records to Logstash over HTTP."""

    def __init__(self, url, extra_fields=None):
        super().__init__()
        self.url = url
        self.extra = extra_fields or {}

    def emit(self, record):
        payload = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "level":     record.levelname,
            "message":   self.format(record),
            "logger":    record.name,
            "file":      record.filename,
            "line":      record.lineno,
        }
        payload.update(self.extra)

        try:
            data = json.dumps(payload).encode("utf-8")
            req  = urllib.request.Request(
                self.url,
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            urllib.request.urlopen(req, timeout=3)
        except Exception:
            pass  # never crash the app because of logging


def get_logger(name="app"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Always print to console
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter("%(levelname)s | %(message)s"))
    logger.addHandler(console)

    # Send to ELK if LOGSTASH_URL is set
    url = os.getenv("LOGSTASH_URL")
    if url:
        elk = ELKHandler(url, extra_fields={
            "app":        os.getenv("APP_NAME", "my-python-app"),
            "environment": os.getenv("APP_ENV", "ci"),
            "run_number": os.getenv("GITHUB_RUN_NUMBER", "0"),
            "branch":     os.getenv("GITHUB_REF_NAME", "local"),
            "actor":      os.getenv("GITHUB_ACTOR", "local"),
            "repository": os.getenv("GITHUB_REPOSITORY", "local"),
        })
        logger.addHandler(elk)

    return logger
