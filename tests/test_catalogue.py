from decimal import Decimal
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from llm_price_tracker.catalogue import build_markdown, estimate_native_cost, load_agents, load_catalogue, validate_catalogue
from llm_price_tracker.send_report import make_message


class CatalogueTest(unittest.TestCase):
    def test_catalogue_is_valid(self) -> None:
        self.assertEqual(validate_catalogue(load_catalogue()), [])

    def test_native_estimate_uses_cache_rate(self) -> None:
        model = {"prices": {"input_usd_per_mtok": 3, "output_usd_per_mtok": 15, "cache_read_usd_per_mtok": 0.3}}
        self.assertEqual(estimate_native_cost(model, Decimal("2"), Decimal("1"), Decimal("0.5")), Decimal("19.65"))

    def test_render_includes_native_and_agent_catalogues(self) -> None:
        output = build_markdown(load_catalogue(), load_agents())
        self.assertIn("## Native model APIs", output)
        self.assertIn("## Coding agents / indirect access", output)
        self.assertIn("Cursor", output)

    def test_email_attaches_the_report(self) -> None:
        with TemporaryDirectory() as directory:
            report = Path(directory) / "PRICEBOOK.md"
            report.write_text("# test report\n", encoding="utf-8")
            message = make_message("sender@gmail.com", "recipient@gmail.com", report)
        self.assertEqual(message["To"], "recipient@gmail.com")
        self.assertEqual(message.get_content_type(), "multipart/mixed")
        self.assertIn("PRICEBOOK.md", message.as_string())
