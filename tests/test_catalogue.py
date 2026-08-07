from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from llm_price_tracker.catalogue import (
    build_html,
    build_markdown,
    estimate_agent_rate,
    estimate_native_cost,
    load_agent_rates,
    load_agents,
    load_catalogue,
    validate_agent_data,
    validate_catalogue,
)
from llm_price_tracker.send_report import make_message
from llm_price_tracker.refresh import comparable_discovery, discovery_payload
from llm_price_tracker import refresh


class CatalogueTest(unittest.TestCase):
    def setUp(self) -> None:
        self.catalogue = load_catalogue()
        self.agents = load_agents()
        self.rates = load_agent_rates()

    def test_all_source_data_is_valid(self) -> None:
        self.assertEqual(validate_catalogue(self.catalogue), [])
        self.assertEqual(validate_agent_data(self.catalogue, self.agents, self.rates), [])

    def test_native_estimate_uses_cache_rate(self) -> None:
        model = {"prices": {"input_usd_per_mtok": 3, "output_usd_per_mtok": 15, "cache_read_usd_per_mtok": 0.3}}
        self.assertEqual(estimate_native_cost(model, Decimal("2"), Decimal("1"), Decimal("0.5")), Decimal("19.65"))

    def test_gpt_56_sol_uses_the_long_context_tier(self) -> None:
        model = next(item for item in self.catalogue["models"] if item["id"] == "openai-gpt-5.6-sol")
        self.assertEqual(estimate_native_cost(model, Decimal("0.4"), Decimal("0")), Decimal("4.0"))

    def test_kiro_model_multiplier_is_estimated_in_credits(self) -> None:
        rate = next(item for item in self.rates["rates"] if item["id"] == "kiro-gpt-5.6-sol")
        scenario = next(item for item in self.rates["scenarios"] if item["id"] == "coding-task")
        estimate = estimate_agent_rate(rate, self.catalogue, self.agents, scenario)
        self.assertEqual(estimate["usage"], Decimal("2.4"))
        self.assertEqual(estimate["usd"], Decimal("0.096"))

    def test_model_discovery_flags_untracked_candidate_without_auto_adding_it(self) -> None:
        payload = discovery_payload(
            [{"id": "openai", "model_candidates": ["GPT-5.6 Sol", "GPT-5.7 Sol"]}], self.catalogue
        )
        self.assertEqual(payload["untracked_candidates"], ["GPT-5.7 Sol"])
        self.assertNotIn("checked_at", comparable_discovery(payload))

    def test_refresh_marks_a_changed_successful_fingerprint(self) -> None:
        with TemporaryDirectory() as directory:
            status_path = Path(directory) / "source-status.json"
            discovery_path = Path(directory) / "model-discovery.json"
            status_path.write_text('{"sources":[{"id":"openai","content_sha256":"old"}]}', encoding="utf-8")
            source = {"id": "openai", "url": "https://example.com/pricing"}
            result = {"id": "openai", "url": source["url"], "content_sha256": "new", "http_status": 200}
            with (
                patch.object(refresh, "STATUS_PATH", status_path),
                patch.object(refresh, "DISCOVERY_PATH", discovery_path),
                patch.object(refresh, "tracked_sources", return_value=[source]),
                patch.object(refresh, "fetch_source", return_value=result),
            ):
                payload, _, changed = refresh.check_sources(timeout=1)
        self.assertTrue(changed)
        self.assertTrue(payload["sources"][0]["changed"])

    def test_render_includes_model_and_agent_comparisons(self) -> None:
        output = build_markdown(self.catalogue, self.agents, self.rates)
        self.assertIn("## 原生模型 API（全量）", output)
        self.assertIn("## Agent × 模型消耗对比", output)
        self.assertIn("Claude Fable 5", output)
        self.assertIn("Kiro", output)
        self.assertNotIn("Roo Code", output)

    def test_only_active_models_and_products_are_reported(self) -> None:
        self.assertTrue(all(model["status"] == "active" for model in self.catalogue["models"]))
        self.assertTrue(all(product["status"] == "active" for product in self.agents["products"]))
        self.assertNotIn("deepseek-v3", {model["id"] for model in self.catalogue["models"]})

    def test_html_render_includes_tables_and_sources(self) -> None:
        output = build_html(self.catalogue, self.agents, self.rates)
        self.assertIn("<table>", output)
        self.assertIn("官方来源", output)
        self.assertIn("Agent × 模型消耗对比", output)

    def test_email_attaches_the_report(self) -> None:
        with TemporaryDirectory() as directory:
            report = Path(directory) / "PRICEBOOK.html"
            report.write_text("<h1>test report</h1>\n", encoding="utf-8")
            message = make_message("sender@gmail.com", "recipient@gmail.com", report)
        self.assertEqual(message["To"], "recipient@gmail.com")
        self.assertEqual(message.get_content_type(), "multipart/mixed")
        self.assertIn("PRICEBOOK.html", message.as_string())
        self.assertIn("text/html", message.as_string())

    def test_app_password_whitespace_is_removed(self) -> None:
        self.assertEqual("".join("abcd\u00a0efgh ijkl\tmnop".split()), "abcdefghijklmnop")
