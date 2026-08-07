# LLM Token Price Tracker

An auditable catalogue for comparing native LLM API list prices with the very different pricing systems used by coding agents.

## What it covers

- Native APIs: current flagship, balanced, lightweight, reasoning, code, RAG, long-context, and open-weight/partner-hosted model categories across global and Chinese providers. The current snapshot includes OpenAI GPT-5.6, Anthropic Claude Opus 4.8 / Sonnet 5 / Fable 5, Gemini 3, DeepSeek V4, Kimi K3, GLM-5.2, Doubao 2.0, and other active families.
- Coding agents: Cursor, Kiro, GitHub Copilot, Windsurf, and Cline. Subscription, credit, and BYOK pricing is intentionally kept separate from native token rates.
- Agent × model usage: `data/agent_model_rates.json` records public model-specific rules — pass-through API price, Token-to-Credit conversion, or a vendor Credit multiplier — plus items that cannot honestly be converted to a fixed amount.
- Traceability: every row has an official pricing-page URL and the workflow records a SHA-256 fingerprint of each source page.

`data/prices.json`, `data/coding_agents.json`, and `data/agent_model_rates.json` are the machine-readable source of truth. The catalogue is an **active-only whitelist**: retired, sunset, or historical models and products must be removed rather than shown with a legacy label. They preserve the original billing currency and an USD comparison field. CNY-to-USD figures are indicative snapshot conversions only; invoices are charged in the source currency.

## Quick start

Requires only Python 3.11+.

```bash
PYTHONPATH=src python3 -m llm_price_tracker.cli validate
PYTHONPATH=src python3 -m llm_price_tracker.cli build
PYTHONPATH=src python3 -m llm_price_tracker.cli estimate \
  --model anthropic-claude-sonnet-5 --input-mtok 2 --output-mtok 0.5
```

The rendered comparison is in [docs/PRICEBOOK.html](docs/PRICEBOOK.html); [docs/PRICEBOOK.md](docs/PRICEBOOK.md) remains as a GitHub-friendly text version.

## Pricing semantics

- Native model rows are public on-demand list prices per one million tokens (MTok), not discounts, enterprise contracts, batch rates, or regional offers unless stated. A model may declare `pricing_tiers` when long-context calls use a different rate.
- A coding agent can add hidden context, retries, tool calls, model multipliers, and policy-based routing. Its subscription or credit cost must not be presented as a token API price. The report's model-level scenario is an overage/usage comparison; it does not deduct included monthly quotas.
- For Cline in BYOK mode, the agent layer is $0 and the selected provider bill is the applicable native API cost.
- Open-weight Llama models are available through partner APIs or self-hosting, so Meta has no single native API price to normalize.

## Scheduled verification

The GitHub Actions workflow runs daily at 10:17 China Standard Time and can be triggered manually. It validates the dataset, checks all official pricing and agent-model URLs, rebuilds the HTML and Markdown catalogues, and emails the generated `PRICEBOOK.html`. When a source fingerprint or a configured new-model pattern changes, it opens a **review pull request** instead of pushing to `main`. A content change is a review signal: pricing pages can change for reasons unrelated to prices, so update the corresponding data row after reviewing the official source before merging.

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
2. Update the original `native_currency` / `native_prices_per_mtok` first. Add `pricing_tiers` whenever a provider specifies a distinct long-context rate.
3. Update `prices` in USD for cross-provider comparison; if using CNY, use the recorded FX snapshot and update `fx_usd_per_cny` when appropriate.
4. For a coding-agent rule, update both the plan in `data/coding_agents.json` and its model rule in `data/agent_model_rates.json`; do not invent a Token conversion when the vendor publishes only a task multiplier.
5. Run `validate`, `build`, and `python3 -m unittest discover -s tests` before committing.

This project deliberately avoids scraping undocumented APIs or treating an agent's UI credit as a token. That keeps the comparison reproducible and honest when vendors alter routing or subscription rules.
