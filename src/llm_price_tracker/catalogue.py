from __future__ import annotations

import json
from collections import defaultdict
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "prices.json"
AGENT_PATH = ROOT / "data" / "coding_agents.json"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_catalogue() -> dict[str, Any]:
    return load_json(DATA_PATH)


def load_agents() -> dict[str, Any]:
    return load_json(AGENT_PATH)


def usd(value: Decimal | str | float | int | None) -> str:
    if value is None:
        return "—"
    return f"${Decimal(str(value)).quantize(Decimal('0.0001')).normalize():f}"


def native_price(item: dict[str, Any], key: str) -> str:
    price = item.get("native_prices_per_mtok", {}).get(key)
    if price is None:
        return "—"
    return f"{item.get('native_currency', 'USD')} {Decimal(str(price)).normalize():f}"


def validate_catalogue(catalogue: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {"id", "provider", "model", "segment", "availability", "source_id"}
    sources = {source["id"] for source in catalogue["sources"]}
    seen: set[str] = set()
    for item in catalogue["models"]:
        missing = required - item.keys()
        if missing:
            errors.append(f"{item.get('id', '<unknown>')}: missing {sorted(missing)}")
        if item.get("id") in seen:
            errors.append(f"duplicate model id: {item['id']}")
        seen.add(item.get("id"))
        if item.get("source_id") not in sources:
            errors.append(f"{item.get('id')}: unknown source_id")
        if item.get("availability") == "api" and not item.get("prices"):
            errors.append(f"{item.get('id')}: API model must have prices")
        for key, price in item.get("prices", {}).items():
            if not isinstance(price, (int, float)) or price < 0:
                errors.append(f"{item.get('id')}: {key} must be a non-negative number")
    return errors


def estimate_native_cost(model: dict[str, Any], input_mtok: Decimal, output_mtok: Decimal,
                         cached_input_mtok: Decimal = Decimal("0")) -> Decimal:
    prices = model["prices"]
    standard_input = max(input_mtok - cached_input_mtok, Decimal("0"))
    return (
        standard_input * Decimal(str(prices["input_usd_per_mtok"]))
        + output_mtok * Decimal(str(prices["output_usd_per_mtok"]))
        + cached_input_mtok * Decimal(str(prices.get("cache_read_usd_per_mtok", prices["input_usd_per_mtok"])))
    )


def build_markdown(catalogue: dict[str, Any], agents: dict[str, Any]) -> str:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for model in catalogue["models"]:
        grouped[model["provider"]].append(model)
    lines = [
        "# LLM Price Catalogue",
        "",
        f"> Snapshot: `{catalogue['snapshot_date']}`. Prices are list prices unless a row says otherwise. "
        "Check the linked official source before purchase.",
        "",
        "## Native model APIs",
        "",
        "| Provider | Model | Positioning | Native input / MTok | Native output / MTok | USD input / output | Source |",
        "|---|---|---|---:|---:|---:|---|",
    ]
    for provider in sorted(grouped):
        for item in grouped[provider]:
            prices = item.get("prices", {})
            source = next(s for s in catalogue["sources"] if s["id"] == item["source_id"])
            if item["availability"] != "api":
                lines.append(f"| {provider} | {item['model']} | {item['segment']} ({item['availability']}) | — | — | — | [official]({source['url']}) |")
                continue
            lines.append(
                f"| {provider} | {item['model']} | {item['segment']} | "
                f"{native_price(item, 'input')} | {native_price(item, 'output')} | "
                f"{usd(prices.get('input_usd_per_mtok'))} / {usd(prices.get('output_usd_per_mtok'))} | [official]({source['url']}) |"
            )
    lines.extend([
        "",
        "## Coding agents / indirect access",
        "",
        "These are product plans or credit systems, not native token list prices. An effective per-token price is only shown where the vendor explicitly publishes a fixed overage rate.",
        "",
        "| Product | Plan | Monthly list price | Usage unit | Model access | Source |",
        "|---|---|---:|---|---|---|",
    ])
    for product in agents["products"]:
        for plan in product["plans"]:
            lines.append(
                f"| {product['name']} | {plan['name']} | {usd(plan.get('monthly_usd'))} | "
                f"{plan['usage_unit']} | {plan['model_access']} | [official]({product['source_url']}) |"
            )
    lines.extend([
        "",
        "## Interpretation",
        "",
        "- `MTok` means one million tokens. Input and output are charged separately; reasoning tokens are commonly billed as output tokens.",
        "- USD is the native list currency for global suppliers. CNY rows retain their source price and add a comparison-only USD conversion using the recorded `fx_usd_per_cny` snapshot; it is not a billing quote.",
        "- Cached-input prices apply only when the provider confirms a cache hit. Cache writes, image, audio, tool, batch, regional, and long-context pricing may be separate.",
        "- Hosted open-weight models are marked `partner/self-hosted`: there is no single Meta-native API list price to compare.",
        "- Coding-agent usage can include hidden context, retries, tool calls, and provider routing. Do not divide a subscription fee by visible chat tokens and label it an API price.",
    ])
    return "\n".join(lines) + "\n"


def status_payload(results: list[dict[str, Any]]) -> dict[str, Any]:
    return {"checked_at": datetime.now(UTC).replace(microsecond=0).isoformat(), "sources": results}
