from __future__ import annotations

import json
from collections import defaultdict
from datetime import UTC, datetime
from decimal import Decimal
from html import escape
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "prices.json"
AGENT_PATH = ROOT / "data" / "coding_agents.json"
AGENT_RATE_PATH = ROOT / "data" / "agent_model_rates.json"
DISCOVERY_PATH = ROOT / "data" / "model-discovery.json"
MTOK = Decimal("1000000")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_catalogue() -> dict[str, Any]:
    return load_json(DATA_PATH)


def load_agents() -> dict[str, Any]:
    return load_json(AGENT_PATH)


def load_agent_rates() -> dict[str, Any]:
    return load_json(AGENT_RATE_PATH)


def usd(value: Decimal | str | float | int | None) -> str:
    if value is None:
        return "—"
    rendered = Decimal(str(value)).quantize(Decimal("0.0001")).normalize()
    return f"${rendered:f}"


def number(value: Decimal | str | float | int | None) -> str:
    if value is None:
        return "—"
    return f"{Decimal(str(value)).quantize(Decimal('0.0001')).normalize():f}"


def native_price(item: dict[str, Any], key: str) -> str:
    price = item.get("native_prices_per_mtok", {}).get(key)
    if price is None:
        return "—"
    return f"{item.get('native_currency', 'USD')} {Decimal(str(price)).normalize():f}"


def source_index(*collections: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        source["id"]: source
        for collection in collections
        for source in collection.get("sources", [])
    }


def model_index(catalogue: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {model["id"]: model for model in catalogue["models"]}


def active_models(catalogue: dict[str, Any]) -> list[dict[str, Any]]:
    """Return the reportable model set; retired records never reach a report."""
    return [model for model in catalogue["models"] if model.get("status") == "active"]


def product_index(agents: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {product["id"]: product for product in agents["products"]}


def tier_for_input(pricing: dict[str, Any], input_mtok: Decimal) -> dict[str, Any]:
    """Select a declared input-size tier, falling back to the legacy flat price."""
    tiers = pricing.get("pricing_tiers")
    if not tiers:
        return pricing.get("prices", pricing)
    input_tokens = input_mtok * MTOK
    for tier in tiers:
        maximum = tier.get("max_input_tokens")
        minimum = tier.get("min_input_tokens")
        if maximum is not None and input_tokens <= Decimal(str(maximum)):
            return tier
        if minimum is not None and input_tokens >= Decimal(str(minimum)):
            return tier
    return tiers[-1]


def estimate_priced_usage(
    pricing: dict[str, Any],
    input_mtok: Decimal,
    output_mtok: Decimal,
    cached_input_mtok: Decimal = Decimal("0"),
    cache_write_mtok: Decimal = Decimal("0"),
) -> Decimal:
    tier = tier_for_input(pricing, input_mtok)
    input_price = Decimal(str(tier["input_usd_per_mtok"]))
    standard_input = max(input_mtok - cached_input_mtok - cache_write_mtok, Decimal("0"))
    cache_read_price = Decimal(str(tier.get("cache_read_usd_per_mtok", input_price)))
    cache_write_price = Decimal(str(tier.get("cache_write_usd_per_mtok", input_price)))
    return (
        standard_input * input_price
        + output_mtok * Decimal(str(tier["output_usd_per_mtok"]))
        + cached_input_mtok * cache_read_price
        + cache_write_mtok * cache_write_price
    )


def estimate_native_cost(
    model: dict[str, Any],
    input_mtok: Decimal,
    output_mtok: Decimal,
    cached_input_mtok: Decimal = Decimal("0"),
    cache_write_mtok: Decimal = Decimal("0"),
) -> Decimal:
    return estimate_priced_usage(model, input_mtok, output_mtok, cached_input_mtok, cache_write_mtok)


def default_overage_usd(product: dict[str, Any]) -> Decimal | None:
    for plan in product["plans"]:
        if plan.get("overage_usd_per_unit") is not None:
            return Decimal(str(plan["overage_usd_per_unit"]))
    return None


def estimate_agent_rate(
    rate: dict[str, Any],
    catalogue: dict[str, Any],
    agents: dict[str, Any],
    scenario: dict[str, Any],
) -> dict[str, Decimal | str | None]:
    """Return only what the vendor pricing makes quantitatively defensible."""
    input_mtok = Decimal(str(scenario["input_mtok"]))
    cached_input_mtok = Decimal(str(scenario.get("cached_input_mtok", 0)))
    output_mtok = Decimal(str(scenario["output_mtok"]))
    mode = rate["billing_mode"]
    if mode == "agent_token_price":
        cost = estimate_priced_usage(rate, input_mtok, output_mtok, cached_input_mtok)
        credit_usd = rate.get("credit_usd")
        credits = cost / Decimal(str(credit_usd)) if credit_usd else None
        return {"usage": credits, "usd": cost, "unit": rate["unit"], "basis": "published token price"}
    if mode == "native_api_price":
        model = model_index(catalogue)[rate["model_id"]]
        cost = estimate_native_cost(model, input_mtok, output_mtok, cached_input_mtok)
        return {"usage": cost, "usd": cost, "unit": rate["unit"], "basis": "selected model list price"}
    if mode in {"credit_multiplier", "fixed_prompt_credit"}:
        credits = Decimal(str(scenario["base_prompt_credits"])) * Decimal(str(rate["credit_multiplier"]))
        overage = default_overage_usd(product_index(agents)[rate["agent_id"]])
        return {
            "usage": credits,
            "usd": credits * overage if overage is not None else None,
            "unit": rate["unit"],
            "basis": "published model credit multiplier",
        }
    return {"usage": None, "usd": None, "unit": rate["unit"], "basis": "no fixed agent multiplier published"}


def validate_catalogue(catalogue: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {"id", "provider", "model", "segment", "availability", "status", "last_verified_at", "source_id"}
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
        if item.get("status") != "active":
            errors.append(f"{item.get('id')}: catalogue only accepts active models")
        if item.get("availability") == "api" and not item.get("prices"):
            errors.append(f"{item.get('id')}: API model must have prices")
        for key, price in item.get("prices", {}).items():
            if not isinstance(price, (int, float)) or price < 0:
                errors.append(f"{item.get('id')}: {key} must be a non-negative number")
        previous_maximum = None
        for tier in item.get("pricing_tiers", []):
            for price_key in ("input_usd_per_mtok", "output_usd_per_mtok"):
                if price_key not in tier or not isinstance(tier[price_key], (int, float)) or tier[price_key] < 0:
                    errors.append(f"{item.get('id')}: tier {tier.get('label', '?')} has invalid {price_key}")
            maximum = tier.get("max_input_tokens")
            if maximum is not None:
                if not isinstance(maximum, int) or maximum <= 0:
                    errors.append(f"{item.get('id')}: tier max_input_tokens must be a positive integer")
                if previous_maximum is not None and maximum <= previous_maximum:
                    errors.append(f"{item.get('id')}: pricing tiers must be ascending")
                previous_maximum = maximum
    for model_id in catalogue.get("featured_model_ids", []):
        model = model_index(catalogue).get(model_id)
        if model is None:
            errors.append(f"featured model does not exist: {model_id}")
        elif model.get("status") != "active":
            errors.append(f"featured model is not active: {model_id}")
    return errors


def validate_agent_data(catalogue: dict[str, Any], agents: dict[str, Any], rates: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    product_ids: set[str] = set()
    for product in agents.get("products", []):
        if {"id", "name", "source_url", "billing_model", "status", "plans"} - product.keys():
            errors.append(f"agent product {product.get('name', '<unknown>')}: missing required fields")
        if product.get("id") in product_ids:
            errors.append(f"duplicate agent product id: {product['id']}")
        product_ids.add(product.get("id"))
        if product.get("status") != "active":
            errors.append(f"agent product {product.get('id')}: catalogue only accepts active products")
        for plan in product.get("plans", []):
            for key in ("name", "monthly_usd", "included_amount", "included_unit", "model_access", "billing_note"):
                if key not in plan:
                    errors.append(f"{product.get('id')}: plan missing {key}")
            for key in ("monthly_usd", "included_amount", "overage_usd_per_unit"):
                value = plan.get(key)
                if value is not None and (not isinstance(value, (int, float)) or value < 0):
                    errors.append(f"{product.get('id')}: plan {plan.get('name')} invalid {key}")
    rate_sources = {source["id"] for source in rates.get("sources", [])}
    known_models = set(model_index(catalogue))
    rate_ids: set[str] = set()
    permitted_modes = {"agent_token_price", "native_api_price", "credit_multiplier", "fixed_prompt_credit", "provider_token_price"}
    for rate in rates.get("rates", []):
        for key in ("id", "agent_id", "model", "billing_mode", "unit", "availability", "source_id", "note"):
            if key not in rate:
                errors.append(f"agent model rate {rate.get('id', '<unknown>')}: missing {key}")
        if rate.get("id") in rate_ids:
            errors.append(f"duplicate agent model rate id: {rate['id']}")
        rate_ids.add(rate.get("id"))
        if rate.get("agent_id") not in product_ids:
            errors.append(f"{rate.get('id')}: unknown agent_id")
        if rate.get("source_id") not in rate_sources:
            errors.append(f"{rate.get('id')}: unknown source_id")
        if rate.get("billing_mode") not in permitted_modes:
            errors.append(f"{rate.get('id')}: unsupported billing_mode")
        if rate.get("availability") == "discontinued":
            errors.append(f"{rate.get('id')}: discontinued model rates are not permitted")
        if rate.get("model_id") and rate["model_id"] not in known_models:
            errors.append(f"{rate.get('id')}: unknown model_id")
        if rate.get("billing_mode") == "native_api_price" and not rate.get("model_id"):
            errors.append(f"{rate.get('id')}: native_api_price requires model_id")
        if rate.get("billing_mode") in {"credit_multiplier", "fixed_prompt_credit"}:
            if not isinstance(rate.get("credit_multiplier"), (int, float)) or rate["credit_multiplier"] < 0:
                errors.append(f"{rate.get('id')}: missing or invalid credit_multiplier")
        if rate.get("billing_mode") == "agent_token_price" and not (rate.get("prices") or rate.get("pricing_tiers")):
            errors.append(f"{rate.get('id')}: agent_token_price needs prices or pricing_tiers")
    return errors


def pricing_label(item: dict[str, Any]) -> str:
    if item.get("billing_status") == "limited-free":
        return "限额免费"
    if not item.get("pricing_tiers"):
        return "标准"
    return "；".join(tier["label"] for tier in item["pricing_tiers"])


def price_pair(item: dict[str, Any]) -> str:
    prices = item.get("prices")
    if not prices:
        return "—"
    return f"{usd(prices['input_usd_per_mtok'])} / {usd(prices['output_usd_per_mtok'])}"


def context_window_label(item: dict[str, Any]) -> str:
    context_window = item.get("context_window_tokens")
    return f"{context_window:,}" if isinstance(context_window, int) else "—"


def lifecycle_label(item: dict[str, Any]) -> str:
    stage = item.get("release_stage")
    return f"{item['status']} / {stage}" if stage else item["status"]


def source_markdown(source: dict[str, Any]) -> str:
    return f"[官方]({source['url']})"


def estimate_label(estimate: dict[str, Decimal | str | None]) -> str:
    if estimate["usage"] is None and estimate["usd"] is None:
        return "不可量化（无固定倍率）"
    usage = f"{number(estimate['usage'])} {estimate['unit']}" if estimate["usage"] is not None else str(estimate["unit"])
    if estimate["usd"] is not None:
        usage += f" ≈ {usd(estimate['usd'])}"
    return usage


def build_markdown(catalogue: dict[str, Any], agents: dict[str, Any], rates: dict[str, Any] | None = None) -> str:
    rates = rates or load_agent_rates()
    sources = source_index(catalogue, rates)
    products = product_index(agents)
    medium = next(s for s in rates["scenarios"] if s["id"] == "coding-task")
    lines = [
        "# LLM Price Catalogue",
        "",
        f"> Snapshot: `{catalogue['snapshot_date']}`. Official list prices and public agent billing rules only; check the linked source before purchase.",
        "",
        "## 当前活跃模型速览",
        "",
        "| 厂商 · 模型 | 定位 | 上下文 | 默认输入 / 输出（USD / MTok） | 长上下文规则 | 官方来源 |",
        "|---|---|---:|---:|---|---|",
    ]
    featured = set(catalogue.get("featured_model_ids", []))
    for item in active_models(catalogue):
        if item["id"] not in featured:
            continue
        lines.append(
            f"| {item['provider']} · {item['model']} | {item['segment']} | {context_window_label(item)} | "
            f"{price_pair(item)} | "
            f"{item.get('pricing_note', '—')} | {source_markdown(sources[item['source_id']])} |"
        )
    lines.extend([
        "",
        "## 原生模型 API（全量）",
        "",
        "| 厂商 | 模型 | 生命周期 | 定位 | 输入 / MTok | 输出 / MTok | 价格档位 | 来源 |",
        "|---|---|---|---|---:|---:|---|---|",
    ])
    for item in sorted(active_models(catalogue), key=lambda row: (row["provider"], row["model"])):
        source = sources[item["source_id"]]
        if item["availability"] != "api":
            lines.append(f"| {item['provider']} | {item['model']} | {lifecycle_label(item)} | {item['segment']} ({item['availability']}) | — | — | — | {source_markdown(source)} |")
            continue
        lines.append(
            f"| {item['provider']} | {item['model']} | {lifecycle_label(item)} | {item['segment']} | "
            f"{native_price(item, 'input')} | {native_price(item, 'output')} | {pricing_label(item)} | {source_markdown(source)} |"
        )
    lines.extend([
        "",
        "## Coding Agent 套餐与可用额度",
        "",
        "| 产品 | 套餐 | 月度标价 | 含量 | 超额标价 | 计费口径 | 官方来源 |",
        "|---|---|---:|---|---:|---|---|",
    ])
    for product in agents["products"]:
        for plan in product["plans"]:
            included = f"{number(plan['included_amount'])} {plan['included_unit']}" if plan["included_amount"] is not None else plan["included_unit"]
            lines.append(
                f"| {product['name']} | {plan['name']} | {usd(plan['monthly_usd'])} | {included} | "
                f"{usd(plan.get('overage_usd_per_unit'))} | {plan['billing_note']} | [官方]({product['source_url']}) |"
            )
    lines.extend([
        "",
        "## Agent × 模型消耗对比",
        "",
        f"情景：**{medium['label']}**（输入 {medium['input_mtok']} MTok、缓存命中 {medium['cached_input_mtok']} MTok、输出 {medium['output_mtok']} MTok；Credit 产品以 1 个基础任务为基准）。订阅内额度不在此扣除，估算仅用于比较单次消耗或超额成本。",
        "",
        "| Agent | 模型 | 计费方式 | 模型级消耗 / 该情景 | 可用性 | 来源 |",
        "|---|---|---|---|---|---|",
    ])
    for rate in sorted(rates["rates"], key=lambda row: (products[row["agent_id"]]["name"], row["model"])):
        estimate = estimate_agent_rate(rate, catalogue, agents, medium)
        lines.append(
            f"| {products[rate['agent_id']]['name']} | {rate['model']} | {rate['billing_mode']} | "
            f"{estimate_label(estimate)} | {rate['availability']} | {source_markdown(sources[rate['source_id']])} |"
        )
    lines.extend([
        "",
        "## 解释与边界",
        "",
        "- `MTok` = 100 万 Token。原生 API 的输入、输出、缓存读取与缓存写入可分别计费；当前工作量情景不包含 cache write。",
        "- Cursor 的 selected-model 行是官方声明的 API list-price pass-through，不表示 GPT‑5.6 一定已出现在 Cursor 当日选择器中。",
        "- Kiro 的倍率作用于随任务复杂度变化的基础 Credits，因此不能诚实地换算成固定 Token 单价。",
        "- Copilot 当前以 `$0.01 / AI credit` 按 Token 价格折算。Copilot 旧 premium-request 口径不用于本表的模型级对比。",
        "- Windsurf 以每条用户 Prompt 的模型倍率计费，模型矩阵会动态变化；Cline 不发布固定平台 Credit 倍率，使用所选模型的提供商价格。",
        "- 本报告实行活跃白名单：已下线、迁移或仅历史可用的模型与 Agent 产品不保留为报告条目。Preview 仍在官方 API 中可用，因此会标注为 Preview 而不与下线混淆。",
        "- CNY 模型的 USD 列仅用于横向比较，不是结算报价。自托管/合作方托管模型没有唯一的原厂 API 价格。",
    ])
    return "\n".join(lines) + "\n"


def build_html(catalogue: dict[str, Any], agents: dict[str, Any], rates: dict[str, Any] | None = None) -> str:
    rates = rates or load_agent_rates()
    sources = source_index(catalogue, rates)
    products = product_index(agents)
    medium = next(s for s in rates["scenarios"] if s["id"] == "coding-task")

    def link(source: dict[str, Any]) -> str:
        return f'<a href="{escape(source["url"], quote=True)}">官方来源</a>'

    def cells(values: list[Any]) -> str:
        return "".join(f"<td>{escape(str(value))}</td>" for value in values)

    latest_rows = []
    for item in active_models(catalogue):
        if item["id"] in set(catalogue.get("featured_model_ids", [])):
            latest_rows.append("<tr>" + cells([
                f"{item['provider']} · {item['model']}", item["segment"], context_window_label(item),
                price_pair(item), item.get("pricing_note", "—"),
            ]) + f"<td>{link(sources[item['source_id']])}</td></tr>")

    native_rows = []
    for item in sorted(active_models(catalogue), key=lambda row: (row["provider"], row["model"])):
        if item["availability"] != "api":
            row = [item["provider"], item["model"], lifecycle_label(item), f"{item['segment']} ({item['availability']})", "—", "—", "—"]
        else:
            row = [item["provider"], item["model"], lifecycle_label(item), item["segment"], native_price(item, "input"), native_price(item, "output"), pricing_label(item)]
        native_rows.append("<tr>" + cells(row) + f"<td>{link(sources[item['source_id']])}</td></tr>")

    plan_rows = []
    for product in agents["products"]:
        for plan in product["plans"]:
            included = f"{number(plan['included_amount'])} {plan['included_unit']}" if plan["included_amount"] is not None else plan["included_unit"]
            plan_rows.append("<tr>" + cells([
                product["name"], plan["name"], usd(plan["monthly_usd"]), included, usd(plan.get("overage_usd_per_unit")), plan["billing_note"],
            ]) + f'<td><a href="{escape(product["source_url"], quote=True)}">官方来源</a></td></tr>')

    rate_rows = []
    for rate in sorted(rates["rates"], key=lambda row: (products[row["agent_id"]]["name"], row["model"])):
        estimate = estimate_agent_rate(rate, catalogue, agents, medium)
        rate_rows.append("<tr>" + cells([
            products[rate["agent_id"]]["name"], rate["model"], rate["billing_mode"], estimate_label(estimate), rate["availability"], rate["note"],
        ]) + f"<td>{link(sources[rate['source_id']])}</td></tr>")

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>LLM Price Catalogue · {escape(catalogue['snapshot_date'])}</title>
  <style>
    :root {{ color-scheme:light; --ink:#172033; --muted:#5b6474; --line:#dfe5ee; --surface:#f6f8fb; --accent:#2563eb; --panel:#ffffff; }}
    * {{ box-sizing:border-box; }} body {{ margin:0; color:var(--ink); background:var(--surface); font:14px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }}
    main {{ max-width:1500px; margin:auto; padding:32px 20px 52px; }} header {{ padding:28px; background:linear-gradient(135deg,#172554,#2563eb); color:white; border-radius:16px; }}
    h1 {{ margin:0 0 6px; font-size:29px; }} h2 {{ margin:36px 0 12px; font-size:21px; }} p {{ color:var(--muted); }} header p {{ color:#dbeafe; margin:0; }}
    .summary {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:12px; margin:18px 0 4px; }} .card {{ padding:15px; background:var(--panel); border:1px solid var(--line); border-radius:12px; }} .card strong {{ display:block; color:#1e3a8a; font-size:18px; }}
    .table-wrap {{ overflow-x:auto; background:var(--panel); border:1px solid var(--line); border-radius:12px; box-shadow:0 1px 2px #1720330d; }} table {{ width:100%; border-collapse:collapse; white-space:nowrap; }} th,td {{ padding:11px 14px; text-align:left; border-bottom:1px solid var(--line); vertical-align:top; }} th {{ position:sticky; top:0; background:#eef4ff; font-weight:650; color:#1e3a8a; }} tr:last-child td {{ border-bottom:0; }} tr:hover td {{ background:#fafcff; }}
    td:nth-child(3),td:nth-child(5),td:nth-child(6) {{ font-variant-numeric:tabular-nums; }} a {{ color:var(--accent); text-decoration:none; }} a:hover {{ text-decoration:underline; }} .note {{ background:#fff7ed; border-left:4px solid #f97316; padding:14px 16px; border-radius:6px; color:#7c2d12; }} .muted {{ color:var(--muted); }}
  </style>
</head>
<body><main>
  <header><h1>LLM Price Catalogue</h1><p>快照日期：{escape(catalogue['snapshot_date'])} · 原生模型价格、Agent 套餐与模型级 Credit / 用量对比</p></header>
  <section class="summary"><div class="card"><strong>{len(active_models(catalogue))}</strong>活跃模型</div><div class="card"><strong>{len(agents['products'])}</strong>编程 Agent</div><div class="card"><strong>{len(rates['rates'])}</strong>模型级 Agent 规则</div><div class="card"><strong>官方页面</strong>每日变更检测</div></section>
  <h2>当前活跃模型速览</h2><p>每家厂商的当前主力模型均纳入速览；完整表同时涵盖旗舰、均衡、轻量、代码、推理和多模态定位。Preview 会明确标注，已下线型号不会出现。</p>
  <div class="table-wrap"><table><thead><tr><th>厂商 · 模型</th><th>定位</th><th>上下文 Tokens</th><th>默认输入 / 输出（USD / MTok）</th><th>长上下文规则</th><th>来源</th></tr></thead><tbody>{''.join(latest_rows)}</tbody></table></div>
  <h2>原生模型 API（全量）</h2><div class="table-wrap"><table><thead><tr><th>厂商</th><th>模型</th><th>生命周期</th><th>定位</th><th>原币输入 / MTok</th><th>原币输出 / MTok</th><th>价格档位</th><th>来源</th></tr></thead><tbody>{''.join(native_rows)}</tbody></table></div>
  <h2>Coding Agent 套餐与可用额度</h2><p>订阅费与模型级消耗分开呈现；含量可抵扣的单位由产品自行定义，不能直接当作 Token。</p><div class="table-wrap"><table><thead><tr><th>产品</th><th>套餐</th><th>月度标价</th><th>含量</th><th>超额标价</th><th>计费口径</th><th>来源</th></tr></thead><tbody>{''.join(plan_rows)}</tbody></table></div>
  <h2>Agent × 模型消耗对比</h2><p>情景：{escape(medium['label'])}（输入 {medium['input_mtok']} MTok、缓存命中 {medium['cached_input_mtok']} MTok、输出 {medium['output_mtok']} MTok；Credit 产品以 1 个基础任务为基准）。估算不包含订阅内额度。</p><div class="table-wrap"><table><thead><tr><th>Agent</th><th>模型</th><th>计费方式</th><th>模型级消耗 / 该情景</th><th>可用性</th><th>口径</th><th>来源</th></tr></thead><tbody>{''.join(rate_rows)}</tbody></table></div>
  <h2>解释与边界</h2><div class="note">MTok = 100 万 Token。Cursor 的 selected-model 口径是 API list-price pass-through，是否可选须以其当日模型选择器为准。Kiro 的 Credit 倍率作用于随任务复杂度变化的基础 Credits；Windsurf 以每条用户 Prompt 的模型倍率计费；Cline 没有公开的固定平台倍率。Copilot 的模型级用量为 $0.01 / AI Credit 的 Token 价折算。已停止的模型与产品不在本报告保留。</div>
</main></body></html>\n"""


def status_payload(results: list[dict[str, Any]]) -> dict[str, Any]:
    return {"checked_at": datetime.now(UTC).replace(microsecond=0).isoformat(), "sources": results}
