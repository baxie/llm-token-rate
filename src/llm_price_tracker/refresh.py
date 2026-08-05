from __future__ import annotations

import hashlib
import json
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
from http.client import IncompleteRead, RemoteDisconnected
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from .catalogue import DISCOVERY_PATH, ROOT, load_agent_rates, load_agents, load_catalogue, status_payload

STATUS_PATH = ROOT / "data" / "source-status.json"


def tracked_sources() -> list[dict]:
    """Return all source pages behind the rendered report, deduplicated by URL."""
    catalogue, agents, rates = load_catalogue(), load_agents(), load_agent_rates()
    sources = list(catalogue["sources"]) + list(rates["sources"])
    sources.extend(
        {"id": f"agent-plan-{product['id']}", "url": product["source_url"]}
        for product in agents["products"]
    )
    unique: list[dict] = []
    seen_urls: set[str] = set()
    for source in sources:
        if source["url"] not in seen_urls:
            unique.append(source)
            seen_urls.add(source["url"])
    return unique


def normalise_name(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip().lower()


def discovery_payload(results: list[dict], catalogue: dict) -> dict:
    known_names = {
        normalise_name(name)
        for model in catalogue["models"]
        for name in [model["model"], *model.get("aliases", [])]
    }
    candidates = []
    for result in results:
        for candidate in result.get("model_candidates", []):
            candidates.append({"source_id": result["id"], "model": candidate, "known": normalise_name(candidate) in known_names})
    untracked = sorted({item["model"] for item in candidates if not item["known"]})
    return {
        "checked_at": status_payload([])["checked_at"],
        "candidates": candidates,
        "untracked_candidates": untracked,
        "note": "Pattern matches are review candidates only. They do not automatically change the audited price catalogue.",
    }


def comparable_discovery(payload: dict) -> dict:
    return {key: value for key, value in payload.items() if key != "checked_at"}


def curl_fallback(source: dict, timeout: int) -> tuple[int | None, bytes, str | None]:
    """Fetch a bounded page sample for sites that reject Python's HTTP client.

    GitHub-hosted runners and macOS include curl. Arguments are passed as a list
    and URLs come solely from the repository's reviewed source registry.
    """
    command = [
        "curl", "--location", "--silent", "--show-error", "--max-time", str(timeout),
        "--range", "0-524287", "--user-agent", "Mozilla/5.0 (compatible; LLMPriceTracker/0.2)",
        "--header", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "--write-out", "\n%{http_code}", source["url"],
    ]
    try:
        completed = subprocess.run(command, capture_output=True, check=False, timeout=timeout + 2)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, b"", str(exc)
    body, separator, status_bytes = completed.stdout.rpartition(b"\n")
    if not separator or not status_bytes.isdigit():
        return None, b"", completed.stderr.decode("utf-8", errors="replace") or "curl returned no HTTP status"
    status = int(status_bytes)
    if completed.returncode != 0 or not 200 <= status < 300:
        error = completed.stderr.decode("utf-8", errors="replace").strip() or f"HTTP {status}"
        return status, b"", error
    return status, body, None


def fetch_source(source: dict, timeout: int) -> dict:
    result = {"id": source["id"], "url": source["url"]}
    body = b""
    try:
        request = Request(
            source["url"],
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; LLMPriceTracker/0.2; +https://github.com/baxie/llm-token-rate)",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            },
        )
        with urlopen(request, timeout=timeout) as response:  # noqa: S310 - URLs are repository-controlled official sources
            # A bounded sample is a review signal, not a claim that the page was
            # fully parsed. It keeps the scheduled job reliable for large pages.
            body = response.read(512 * 1024)
            result.update({"http_status": response.status, "content_sha256": hashlib.sha256(body).hexdigest()})
    except HTTPError as exc:
        result.update({"http_status": exc.code, "error": str(exc)})
    except (URLError, IncompleteRead, RemoteDisconnected, TimeoutError, OSError) as exc:
        result.update({"http_status": None, "error": str(getattr(exc, "reason", exc))})
    if not body:
        status, body, fallback_error = curl_fallback(source, timeout)
        if body:
            result.update({"http_status": status, "content_sha256": hashlib.sha256(body).hexdigest(), "fetch_method": "curl-fallback"})
            result.pop("error", None)
        elif fallback_error:
            result["error"] = f"{result.get('error', 'urllib request failed')}; curl fallback: {fallback_error}"
    pattern = source.get("discovery_pattern")
    if body and pattern:
        text = body.decode("utf-8", errors="replace")
        result["model_candidates"] = sorted({match.group(0) for match in re.finditer(pattern, text, flags=re.IGNORECASE)})
    return result


def check_sources(timeout: int = 30) -> tuple[dict, dict, bool]:
    catalogue = load_catalogue()
    previous = {}
    if STATUS_PATH.exists():
        previous = {item["id"]: item for item in json.loads(STATUS_PATH.read_text(encoding="utf-8"))["sources"]}
    sources = tracked_sources()
    # Pricing pages are independent. Bounded parallel checks avoid one slow
    # vendor extending the Action for every other source.
    with ThreadPoolExecutor(max_workers=min(8, len(sources))) as executor:
        results = list(executor.map(lambda source: fetch_source(source, timeout), sources))
    source_changed = False
    for result in results:
        old = previous.get(result["id"], {})
        # A network or HTTP error must not masquerade as a pricing-page change.
        # Only compare two successful bounded-content fingerprints.
        old_hash, current_hash = old.get("content_sha256"), result.get("content_sha256")
        # The first successful check of a newly configured page establishes a
        # reviewable baseline. A transport failure never does.
        result["changed"] = bool(current_hash and (not old_hash or old_hash != current_hash))
        if current_hash and not old_hash:
            result["change_kind"] = "new_source_baseline"
        source_changed = source_changed or result["changed"]
    discovery = discovery_payload(results, catalogue)
    previous_discovery = {}
    if DISCOVERY_PATH.exists():
        previous_discovery = json.loads(DISCOVERY_PATH.read_text(encoding="utf-8"))
    discovery_changed = comparable_discovery(discovery) != comparable_discovery(previous_discovery)
    return status_payload(results), discovery, source_changed or discovery_changed


def write_status(payload: dict) -> None:
    STATUS_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_discovery(payload: dict) -> None:
    DISCOVERY_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
