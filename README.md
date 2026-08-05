# LLM Token Price Tracker

An auditable catalogue for comparing native LLM API list prices with the very different pricing systems used by coding agents.

## What it covers

- Native APIs: flagship, balanced, lightweight, reasoning, code, RAG, long-context, and open-weight/partner-hosted model categories across global and Chinese providers.
- Coding agents: Cursor, Kiro, GitHub Copilot, Windsurf, Cline, and Roo Code. Subscription, credit, and BYOK pricing is intentionally kept separate from native token rates.
- Traceability: every row has an official pricing-page URL and the workflow records a SHA-256 fingerprint of each source page.

`data/prices.json` is the machine-readable source of truth. It preserves the original billing currency and an USD comparison field. CNY-to-USD figures are indicative snapshot conversions only; invoices are charged in the source currency.

## Quick start

Requires only Python 3.11+.

```bash
PYTHONPATH=src python3 -m llm_price_tracker.cli validate
PYTHONPATH=src python3 -m llm_price_tracker.cli build
PYTHONPATH=src python3 -m llm_price_tracker.cli estimate \
  --model anthropic-claude-sonnet-4 --input-mtok 2 --output-mtok 0.5
```

The rendered comparison is in [docs/PRICEBOOK.html](docs/PRICEBOOK.html); [docs/PRICEBOOK.md](docs/PRICEBOOK.md) remains as a GitHub-friendly text version.

## Pricing semantics

- Native model rows are public on-demand list prices per one million tokens (MTok), not discounts, enterprise contracts, batch rates, or regional offers unless stated.
- A coding agent can add hidden context, retries, tool calls, model multipliers, and policy-based routing. Its subscription or credit cost must not be presented as a token API price.
- For Cline and Roo Code in BYOK mode, the agent layer is $0 and the selected provider bill is the applicable native API cost.
- Open-weight Llama models are available through partner APIs or self-hosting, so Meta has no single native API price to normalize.

## Scheduled verification

The GitHub Actions workflow runs daily at 10:17 China Standard Time and can be triggered manually. It validates the dataset, checks all official pricing URLs, rebuilds the HTML and Markdown catalogues, emails the generated `PRICEBOOK.html`, and commits only when source content changes. A content change is a review signal: pricing pages can change for reasons unrelated to prices, so update the corresponding data row after reviewing the official source.

### Gmail delivery setup

Create these repository Action secrets under `Settings` → `Secrets and variables` → `Actions`; never put their values in a file or commit.

| Secret | Value |
|---|---|
| `SMTP_SERVER` | `smtp.gmail.com` |
| `SMTP_PORT` | `465` |
| `SMTP_USERNAME` | Gmail sender address |
| `SMTP_PASSWORD` | Gmail 16-character App Password |
| `REPORT_RECIPIENT` | Destination email address |

The sender must have two-step verification and an App Password. The report is sent only after validation and rendering succeed.

## Updating a price

1. Verify the official page linked by the model's `source_id`.
2. Update the original `native_currency` / `native_prices_per_mtok` first.
3. Update `prices` in USD for cross-provider comparison; if using CNY, use the recorded FX snapshot and update `fx_usd_per_cny` when appropriate.
4. Run `validate`, `build`, and `python3 -m unittest discover -s tests` before committing.

This project deliberately avoids scraping undocumented APIs or treating an agent's UI credit as a token. That keeps the comparison reproducible and honest when vendors alter routing or subscription rules.
