from __future__ import annotations

import json
from html import escape
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


def build_html(catalogue: dict[str, Any], agents: dict[str, Any]) -> str:
    def source_link(source_id: str) -> str:
        source = next(source for source in catalogue["sources"] if source["id"] == source_id)
        return f'<a href="{escape(source["url"], quote=True)}">官方来源</a>'

    native_rows = []
    for item in sorted(catalogue["models"], key=lambda row: (row["provider"], row["model"])):
        if item["availability"] != "api":
            cells = [item["provider"], item["model"], f'{item["segment"]} ({item["availability"]})', "—", "—", "—"]
        else:
            prices = item["prices"]
            cells = [
                item["provider"], item["model"], item["segment"], native_price(item, "input"), native_price(item, "output"),
                f'{usd(prices.get("input_usd_per_mtok"))} / {usd(prices.get("output_usd_per_mtok"))}',
            ]
        native_rows.append("<tr>" + "".join(f"<td>{escape(str(cell))}</td>" for cell in cells) + f"<td>{source_link(item['source_id'])}</td></tr>")

    agent_rows = []
    for product in agents["products"]:
        for plan in product["plans"]:
            cells = [product["name"], plan["name"], usd(plan.get("monthly_usd")), plan["usage_unit"], plan["model_access"]]
            agent_rows.append(
                "<tr>" + "".join(f"<td>{escape(str(cell))}</td>" for cell in cells)
                + f'<td><a href="{escape(product["source_url"], quote=True)}">官方来源</a></td></tr>'
            )

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>LLM Price Catalogue · {escape(catalogue['snapshot_date'])}</title>
  <style>
    :root {{ color-scheme: light; --ink:#172033; --muted:#5b6474; --line:#dfe5ee; --surface:#f6f8fb; --accent:#2563eb; }}
    body {{ margin:0; color:var(--ink); background:var(--surface); font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }}
    main {{ max-width:1440px; margin:auto; padding:32px 20px 48px; }}
    header {{ padding:26px 28px; background:linear-gradient(135deg,#172554,#2563eb); color:white; border-radius:16px; }}
    h1 {{ margin:0 0 6px; font-size:28px; }} h2 {{ margin:34px 0 12px; font-size:20px; }} p {{ color:var(--muted); }} header p {{ color:#dbeafe; margin:0; }}
    .table-wrap {{ overflow-x:auto; background:white; border:1px solid var(--line); border-radius:12px; box-shadow:0 1px 2px #1720330d; }}
    table {{ width:100%; border-collapse:collapse; white-space:nowrap; }} th,td {{ padding:11px 14px; text-align:left; border-bottom:1px solid var(--line); }}
    th {{ position:sticky; top:0; background:#eef4ff; font-weight:650; color:#1e3a8a; }} tr:last-child td {{ border-bottom:0; }} tr:hover td {{ background:#fafcff; }}
    td:nth-child(4),td:nth-child(5),td:nth-child(6) {{ text-align:right; font-variant-numeric:tabular-nums; }} a {{ color:var(--accent); text-decoration:none; }} a:hover {{ text-decoration:underline; }}
    .note {{ background:#fff7ed; border-left:4px solid #f97316; padding:14px 16px; border-radius:6px; }}
  </style>
</head>
<body><main>
  <header><h1>LLM Price Catalogue</h1><p>快照日期：{escape(catalogue['snapshot_date'])} · 所有价格以官方页面为准</p></header>
  <h2>原生模型 API</h2>
  <div class="table-wrap"><table><thead><tr><th>厂商</th><th>模型</th><th>定位</th><th>原币输入 / MTok</th><th>原币输出 / MTok</th><th>USD 输入 / 输出</th><th>来源</th></tr></thead><tbody>{''.join(native_rows)}</tbody></table></div>
  <h2>Coding Agent / 间接调用</h2>
  <div class="table-wrap"><table><thead><tr><th>产品</th><th>套餐</th><th>月度标价</th><th>计费单位</th><th>模型访问</th><th>来源</th></tr></thead><tbody>{''.join(agent_rows)}</tbody></table></div>
  <h2>口径说明</h2>
  <div class="note">MTok = 100 万 Token。Coding Agent 的套餐、积分、隐藏上下文与模型路由不等同于原生 API Token 单价；CNY 的 USD 数值仅用于横向比较，不是结算报价。</div>
</main></body></html>
"""


def status_payload(results: list[dict[str, Any]]) -> dict[str, Any]:
    return {"checked_at": datetime.now(UTC).replace(microsecond=0).isoformat(), "sources": results}
