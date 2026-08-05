from __future__ import annotations

import argparse
from decimal import Decimal
from .catalogue import (
    AGENT_PATH,
    AGENT_RATE_PATH,
    DATA_PATH,
    ROOT,
    build_html,
    build_markdown,
    estimate_native_cost,
    load_agent_rates,
    load_agents,
    load_catalogue,
    validate_agent_data,
    validate_catalogue,
)
from .refresh import check_sources, write_discovery, write_status


def command_validate(_: argparse.Namespace) -> int:
    catalogue, agents, rates = load_catalogue(), load_agents(), load_agent_rates()
    errors = validate_catalogue(catalogue) + validate_agent_data(catalogue, agents, rates)
    if errors:
        print("Catalogue validation failed:\n- " + "\n- ".join(errors))
        return 1
    print("Catalogue validation passed.")
    return 0


def command_build(_: argparse.Namespace) -> int:
    catalogue, agents, rates = load_catalogue(), load_agents(), load_agent_rates()
    errors = validate_catalogue(catalogue) + validate_agent_data(catalogue, agents, rates)
    if errors:
        print("Refusing to build invalid catalogue:\n- " + "\n- ".join(errors))
        return 1
    markdown_output = ROOT / "docs" / "PRICEBOOK.md"
    html_output = ROOT / "docs" / "PRICEBOOK.html"
    markdown_output.write_text(build_markdown(catalogue, agents, rates), encoding="utf-8")
    html_output.write_text(build_html(catalogue, agents, rates), encoding="utf-8")
    print(
        f"Built {markdown_output.relative_to(ROOT)} and {html_output.relative_to(ROOT)} from "
        f"{DATA_PATH.name}, {AGENT_PATH.name}, and {AGENT_RATE_PATH.name}."
    )
    return 0


def command_refresh(args: argparse.Namespace) -> int:
    payload, discovery, changed = check_sources(args.timeout)
    status_path = ROOT / "data" / "source-status.json"
    discovery_path = ROOT / "data" / "model-discovery.json"
    if changed or not status_path.exists():
        write_status(payload)
    if changed or not discovery_path.exists():
        write_discovery(discovery)
    if changed:
        print(
            f"Checked {len(payload['sources'])} official sources; persisted changed source or model-discovery evidence "
            f"({len(discovery['untracked_candidates'])} untracked candidate(s))."
        )
    else:
        print(f"Checked {len(payload['sources'])} official sources; no content change detected.")
    return 0


def command_estimate(args: argparse.Namespace) -> int:
    catalogue = load_catalogue()
    model = next((x for x in catalogue["models"] if x["id"] == args.model), None)
    if not model:
        print(f"Unknown model ID: {args.model}")
        return 2
    if model["availability"] != "api":
        print(f"{model['model']} has no provider-native API price.")
        return 2
    total = estimate_native_cost(model, Decimal(args.input_mtok), Decimal(args.output_mtok), Decimal(args.cached_input_mtok))
    print(f"{model['provider']} {model['model']}: ${total.quantize(Decimal('0.0001'))} list-price estimate")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Auditable LLM pricing catalogue")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate", help="validate source data").set_defaults(func=command_validate)
    commands.add_parser("build", help="render the Markdown catalogue").set_defaults(func=command_build)
    refresh = commands.add_parser("refresh", help="check official pricing pages for changes")
    refresh.add_argument("--timeout", type=int, default=30)
    refresh.set_defaults(func=command_refresh)
    estimate = commands.add_parser("estimate", help="estimate a native API request")
    estimate.add_argument("--model", required=True)
    estimate.add_argument("--input-mtok", default="0")
    estimate.add_argument("--output-mtok", default="0")
    estimate.add_argument("--cached-input-mtok", default="0")
    estimate.set_defaults(func=command_estimate)
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
