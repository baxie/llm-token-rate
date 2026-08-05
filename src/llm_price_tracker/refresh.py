from __future__ import annotations

import hashlib
import json
from pathlib import Path
from http.client import IncompleteRead
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .catalogue import ROOT, load_catalogue, status_payload

STATUS_PATH = ROOT / "data" / "source-status.json"


def check_sources(timeout: int = 30) -> tuple[dict, bool]:
    catalogue = load_catalogue()
    previous = {}
    if STATUS_PATH.exists():
        previous = {item["id"]: item for item in json.loads(STATUS_PATH.read_text())["sources"]}
    results = []
    changed = False
    for source in catalogue["sources"]:
        result = {"id": source["id"], "url": source["url"]}
        try:
            request = Request(source["url"], headers={"User-Agent": "llm-price-tracker/0.1 (+https://github.com)"})
            with urlopen(request, timeout=timeout) as response:  # noqa: S310 - URLs are repository-controlled official sources
                # A bounded sample prevents a slow or malformed chunked response from
                # aborting the whole daily audit. It is a change signal, not a claim
                # that the complete document was parsed.
                body = response.read(512 * 1024)
                result.update({"http_status": response.status, "content_sha256": hashlib.sha256(body).hexdigest()})
        except HTTPError as exc:
            result.update({"http_status": exc.code, "error": str(exc)})
        except (URLError, IncompleteRead) as exc:
            result.update({"http_status": None, "error": str(getattr(exc, "reason", exc))})
        old = previous.get(source["id"], {})
        result["changed"] = bool(old and old.get("content_sha256") != result.get("content_sha256"))
        changed = changed or result["changed"]
        results.append(result)
    return status_payload(results), changed


def write_status(payload: dict) -> None:
    STATUS_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
