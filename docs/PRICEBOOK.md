# LLM Price Catalogue

> Snapshot: `2026-08-05`. Official list prices and public agent billing rules only; check the linked source before purchase.

## 本次重点：OpenAI GPT‑5.6 系列

| 模型 | 定位 | 上下文 | 默认输入 / 输出（USD / MTok） | 长上下文规则 | 官方来源 |
|---|---|---:|---:|---|---|
| GPT-5.6 Sol | 旗舰 / 最强 Agent 与复杂工作流 | 1,050,000 | $5 / $30 | 超过 272K 输入 Token 的长上下文请求使用更高档位；cache write 单列。 | [官方](https://developers.openai.com/api/docs/models/gpt-5.6-sol) |
| GPT-5.6 Terra | 均衡 / 更低单价 | 1,050,000 | $2 / $12 | 超过 272K 输入 Token 的长上下文请求使用更高档位；cache write 单列。 | [官方](https://developers.openai.com/api/docs/models/gpt-5.6-terra) |
| GPT-5.6 Luna | 高吞吐 / 最低单价 | 1,050,000 | $0.2 / $1.2 | 超过 272K 输入 Token 的长上下文请求使用更高档位；cache write 单列。 | [官方](https://developers.openai.com/api/docs/models/gpt-5.6-luna) |

## 原生模型 API（全量）

| 厂商 | 模型 | 生命周期 | 定位 | 输入 / MTok | 输出 / MTok | 价格档位 | 来源 |
|---|---|---|---|---:|---:|---|---|
| Alibaba Cloud | Qwen Coder | active | 代码 | CNY 1.5 | CNY 6 | 标准 | [官方](https://help.aliyun.com/zh/model-studio/models) |
| Alibaba Cloud | Qwen-Max | active | 旗舰 / 通用 | CNY 2.4 | CNY 9.6 | 标准 | [官方](https://help.aliyun.com/zh/model-studio/models) |
| Alibaba Cloud | Qwen-Plus | active | 均衡 / 通用 | CNY 0.8 | CNY 2 | 标准 | [官方](https://help.aliyun.com/zh/model-studio/models) |
| Alibaba Cloud | Qwen-Turbo | active | 轻量 / 高吞吐 | CNY 0.3 | CNY 0.6 | 标准 | [官方](https://help.aliyun.com/zh/model-studio/models) |
| Anthropic | Claude Haiku 3.5 | active | 轻量 / 高吞吐 | USD 0.8 | USD 4 | 标准 | [官方](https://docs.anthropic.com/en/docs/about-claude/pricing) |
| Anthropic | Claude Opus 4.1 | active | 旗舰 / 高难推理 | USD 15 | USD 75 | 标准 | [官方](https://docs.anthropic.com/en/docs/about-claude/pricing) |
| Anthropic | Claude Sonnet 4 | active | 均衡 / 编码 | USD 3 | USD 15 | 标准 | [官方](https://docs.anthropic.com/en/docs/about-claude/pricing) |
| Baidu | ERNIE 4.5 | active | 旗舰 / 通用 | CNY 4 | CNY 16 | 标准 | [官方](https://cloud.baidu.com/doc/WENXINWORKSHOP/s/6ltgkz7is) |
| Baidu | ERNIE X1 | active | 推理 | CNY 2 | CNY 8 | 标准 | [官方](https://cloud.baidu.com/doc/WENXINWORKSHOP/s/6ltgkz7is) |
| ByteDance | Doubao Lite | active | 轻量 / 高吞吐 | CNY 0.3 | CNY 0.6 | 标准 | [官方](https://www.volcengine.com/docs/82379/1099320) |
| ByteDance | Doubao Pro | active | 均衡 / 通用 | CNY 0.8 | CNY 2 | 标准 | [官方](https://www.volcengine.com/docs/82379/1099320) |
| ByteDance | Doubao-Seed-1.6 | active | 旗舰 / 多模态与推理 | CNY 0.8 | CNY 8 | 标准 | [官方](https://www.volcengine.com/docs/82379/1099320) |
| Cohere | Command A | active | 旗舰 / 企业 RAG | USD 2.5 | USD 10 | 标准 | [官方](https://docs.cohere.com/docs/how-does-cohere-pricing-work) |
| Cohere | Command R | active | 轻量 RAG | USD 0.15 | USD 0.6 | 标准 | [官方](https://docs.cohere.com/docs/how-does-cohere-pricing-work) |
| Cohere | Command R+ | active | 高质量 RAG | USD 2.5 | USD 10 | 标准 | [官方](https://docs.cohere.com/docs/how-does-cohere-pricing-work) |
| DeepSeek | DeepSeek-R1 | active | 推理 | CNY 4 | CNY 16 | 标准 | [官方](https://api-docs.deepseek.com/quick_start/pricing) |
| DeepSeek | DeepSeek-V3 | active | 通用 / 代码 | CNY 2 | CNY 8 | 标准 | [官方](https://api-docs.deepseek.com/quick_start/pricing) |
| Google | Gemini 2.5 Flash | active | 均衡 / Agent | USD 0.3 | USD 2.5 | 标准 | [官方](https://ai.google.dev/gemini-api/docs/pricing) |
| Google | Gemini 2.5 Flash-Lite | active | 轻量 / 高吞吐 | USD 0.1 | USD 0.4 | 标准 | [官方](https://ai.google.dev/gemini-api/docs/pricing) |
| Google | Gemini 2.5 Pro | active | 旗舰 / 推理与多模态 | USD 1.25 | USD 10 | 标准 | [官方](https://ai.google.dev/gemini-api/docs/pricing) |
| Meta | Llama 4 Maverick | — | 旗舰开源 / 多模态 (partner/self-hosted) | — | — | — | [官方](https://www.llama.com/llama-downloads/) |
| Meta | Llama 4 Scout | — | 长上下文开源 / 多模态 (partner/self-hosted) | — | — | — | [官方](https://www.llama.com/llama-downloads/) |
| MiniMax | MiniMax-M2.5 | active | 均衡 / 代码与 Agent | CNY 2.1 | CNY 8.4 | 标准 | [官方](https://platform.minimaxi.com/docs/guides/pricing-paygo) |
| MiniMax | MiniMax-M2.7 | active | 代码 / Agent | CNY 2.1 | CNY 8.4 | 标准 | [官方](https://platform.minimaxi.com/docs/guides/pricing-paygo) |
| MiniMax | MiniMax-M2.7-highspeed | active | 低延迟 / 代码与 Agent | CNY 4.2 | CNY 16.8 | 标准 | [官方](https://platform.minimaxi.com/docs/guides/pricing-paygo) |
| Mistral AI | Codestral | active | 代码 | USD 0.3 | USD 0.9 | 标准 | [官方](https://mistral.ai/pricing/api/) |
| Mistral AI | Mistral Large 3 | active | 旗舰 / 通用 | USD 0.5 | USD 1.5 | 标准 | [官方](https://mistral.ai/pricing/api/) |
| Mistral AI | Mistral Medium 3 | active | 均衡 / 企业 | USD 0.4 | USD 2 | 标准 | [官方](https://mistral.ai/pricing/api/) |
| Mistral AI | Mistral Small 3 | active | 轻量 / 高吞吐 | USD 0.1 | USD 0.3 | 标准 | [官方](https://mistral.ai/pricing/api/) |
| Moonshot AI | Kimi K2 | active | 旗舰 / Agent 与代码 | CNY 4 | CNY 16 | 标准 | [官方](https://platform.moonshot.cn/docs/pricing) |
| Moonshot AI | Kimi K2 Turbo | active | 低延迟 / Agent 与代码 | CNY 8 | CNY 32 | 标准 | [官方](https://platform.moonshot.cn/docs/pricing) |
| OpenAI | GPT-4.1 | active | 通用 / 长上下文 | USD 2 | USD 8 | 标准 | [官方](https://openai.com/api/pricing/) |
| OpenAI | GPT-5 | active | 旗舰 / 推理与通用 | USD 1.25 | USD 10 | 标准 | [官方](https://openai.com/api/pricing/) |
| OpenAI | GPT-5 mini | active | 均衡 / 高性价比 | USD 0.25 | USD 2 | 标准 | [官方](https://openai.com/api/pricing/) |
| OpenAI | GPT-5 nano | active | 轻量 / 高吞吐 | USD 0.05 | USD 0.4 | 标准 | [官方](https://openai.com/api/pricing/) |
| OpenAI | GPT-5.6 Luna | active | 高吞吐 / 最低单价 | USD 0.2 | USD 1.2 | ≤272K input；>272K input | [官方](https://developers.openai.com/api/docs/models/gpt-5.6-luna) |
| OpenAI | GPT-5.6 Sol | active | 旗舰 / 最强 Agent 与复杂工作流 | USD 5 | USD 30 | ≤272K input；>272K input | [官方](https://developers.openai.com/api/docs/models/gpt-5.6-sol) |
| OpenAI | GPT-5.6 Terra | active | 均衡 / 更低单价 | USD 2 | USD 12 | ≤272K input；>272K input | [官方](https://developers.openai.com/api/docs/models/gpt-5.6-terra) |
| OpenAI | o3 | active | 复杂推理 | USD 2 | USD 8 | 标准 | [官方](https://openai.com/api/pricing/) |
| OpenAI | o4-mini | active | 经济型推理 | USD 1.1 | USD 4.4 | 标准 | [官方](https://openai.com/api/pricing/) |
| StepFun | Step-3.5-Flash | active | 轻量 / 多模态 | CNY 0.5 | CNY 2 | 标准 | [官方](https://platform.stepfun.com/docs/zh/guides/pricing/intro) |
| Tencent Cloud | Hunyuan T1 | active | 深度推理 | CNY 4 | CNY 16 | 标准 | [官方](https://cloud.tencent.com/document/product/1729/97732) |
| Tencent Cloud | Hunyuan TurboS | active | 高速 / 通用 | CNY 0.8 | CNY 2 | 标准 | [官方](https://cloud.tencent.com/document/product/1729/97732) |
| Zhipu AI | GLM-4.5 | active | 旗舰 / 推理与代码 | CNY 4 | CNY 16 | 标准 | [官方](https://docs.bigmodel.cn/cn/guide/models/text/glm-4.5) |
| Zhipu AI | GLM-4.5 Air | active | 经济型 / 推理与代码 | CNY 0.8 | CNY 2 | 标准 | [官方](https://docs.bigmodel.cn/cn/guide/models/text/glm-4.5) |
| xAI | Grok 3 Mini | active | 经济型推理 | USD 0.3 | USD 0.5 | 标准 | [官方](https://docs.x.ai/docs/models) |
| xAI | Grok 4 | active | 旗舰 / 推理 | USD 3 | USD 15 | 标准 | [官方](https://docs.x.ai/docs/models) |

## Coding Agent 套餐与可用额度

| 产品 | 套餐 | 月度标价 | 含量 | 超额标价 | 计费口径 | 官方来源 |
|---|---|---:|---|---:|---|---|
| Cursor | Hobby | $0 | 有限用量 | — | 官方未公布固定 Token 或 Credit 配额 | [官方](https://docs.cursor.com/account/pricing) |
| Cursor | Pro | $20 | 20 USD Agent API usage | — | 另有 bonus usage；超额按用量计费 | [官方](https://docs.cursor.com/account/pricing) |
| Cursor | Pro+ | $60 | 70 USD Agent API usage | — | 另有 bonus usage；超额按用量计费 | [官方](https://docs.cursor.com/account/pricing) |
| Cursor | Ultra | $200 | 400 USD Agent API usage | — | 另有 bonus usage；超额按用量计费 | [官方](https://docs.cursor.com/account/pricing) |
| Kiro | Free | $0 | 50 credits | $0.04 | 可购买额外 Credits | [官方](https://kiro.dev/pricing/) |
| Kiro | Pro | $20 | 1000 credits | $0.04 | 可购买额外 Credits | [官方](https://kiro.dev/pricing/) |
| Kiro | Pro+ | $40 | 2000 credits | $0.04 | 可购买额外 Credits | [官方](https://kiro.dev/pricing/) |
| Kiro | Pro Max | $100 | 5000 credits | $0.04 | 可购买额外 Credits | [官方](https://kiro.dev/pricing/) |
| Kiro | Power | $200 | 10000 credits | $0.04 | 可购买额外 Credits | [官方](https://kiro.dev/pricing/) |
| GitHub Copilot | Free | $0 | 有限免费用量 | $0.01 | 无统一可比的公开 AI Credit 配额 | [官方](https://docs.github.com/en/copilot/concepts/billing/usage-based-billing-for-individuals) |
| GitHub Copilot | Pro | $10 | 1500 AI credits | $0.01 | 1,000 base + 500 flex AI credits | [官方](https://docs.github.com/en/copilot/concepts/billing/usage-based-billing-for-individuals) |
| GitHub Copilot | Pro+ | $39 | 7000 AI credits | $0.01 | 3,900 base + 3,100 flex AI credits | [官方](https://docs.github.com/en/copilot/concepts/billing/usage-based-billing-for-individuals) |
| GitHub Copilot | Max | $100 | 20000 AI credits | $0.01 | 10,000 base + 10,000 flex AI credits | [官方](https://docs.github.com/en/copilot/concepts/billing/usage-based-billing-for-individuals) |
| Windsurf | Free | $0 | 25 prompt credits | — | 免费额度 | [官方](https://docs.windsurf.com/windsurf/accounts/usage) |
| Windsurf | Pro | $15 | 500 prompt credits | $0.04 | Top-up：$10 / 250 credits | [官方](https://docs.windsurf.com/windsurf/accounts/usage) |
| Windsurf | Teams | $30 | 500 prompt credits / seat | $0.04 | Top-up：$40 / 1,000 credits | [官方](https://docs.windsurf.com/windsurf/accounts/usage) |
| Windsurf | Enterprise | — | 1000 prompt credits / seat | — | 企业报价；额度以合同为准 | [官方](https://docs.windsurf.com/windsurf/accounts/usage) |
| Cline | Bring your own API key | $0 | provider-billed | — | 无固定 Cline Credit 倍率 | [官方](https://docs.cline.bot/getting-started/authorizing-with-cline) |
| Roo Code（已停止） | Bring your own API key（历史） | $0 | provider-billed | — | 产品已停止；无固定 Roo Code Credit 倍率 | [官方](https://roocodeinc.github.io/Roo-Code/) |

## Agent × 模型消耗对比

情景：**一次中等编码任务**（输入 0.15 MTok、缓存命中 0.05 MTok、输出 0.015 MTok；Credit 产品以 1 个基础任务为基准）。订阅内额度不在此扣除，估算仅用于比较单次消耗或超额成本。

| Agent | 模型 | 计费方式 | 模型级消耗 / 该情景 | 可用性 | 来源 |
|---|---|---|---|---|---|
| Cline | 所选提供商模型（BYOK / Provider） | provider_token_price | 不可量化（无固定倍率） | selected-model-dependent | [官方](https://docs.cline.bot/getting-started/authorizing-with-cline) |
| Cursor | Cursor Auto | agent_token_price | USD Agent API usage ≈ $0.2275 | active | [官方](https://docs.cursor.com/account/pricing) |
| Cursor | GPT-5.6 Luna（如当前模型选择器可用） | native_api_price | 0.039 USD Agent API usage ≈ $0.039 | model-selection-dependent | [官方](https://docs.cursor.com/account/pricing) |
| Cursor | GPT-5.6 Sol（如当前模型选择器可用） | native_api_price | 0.975 USD Agent API usage ≈ $0.975 | model-selection-dependent | [官方](https://docs.cursor.com/account/pricing) |
| Cursor | GPT-5.6 Terra（如当前模型选择器可用） | native_api_price | 0.39 USD Agent API usage ≈ $0.39 | model-selection-dependent | [官方](https://docs.cursor.com/account/pricing) |
| GitHub Copilot | GPT-5.6 Luna | agent_token_price | 3.9 GitHub AI credits ≈ $0.039 | active | [官方](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing) |
| GitHub Copilot | GPT-5.6 Sol | agent_token_price | 97.5 GitHub AI credits ≈ $0.975 | active | [官方](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing) |
| GitHub Copilot | GPT-5.6 Terra | agent_token_price | 39 GitHub AI credits ≈ $0.39 | active | [官方](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing) |
| Kiro | Claude Haiku 4.5 | credit_multiplier | 0.4 Kiro credits ≈ $0.016 | active | [官方](https://kiro.dev/docs/models) |
| Kiro | Claude Opus 5 | credit_multiplier | 2.2 Kiro credits ≈ $0.088 | active | [官方](https://kiro.dev/docs/models) |
| Kiro | Claude Sonnet 5 | credit_multiplier | 1.3 Kiro credits ≈ $0.052 | active | [官方](https://kiro.dev/docs/models) |
| Kiro | DeepSeek V3.2 | credit_multiplier | 0.25 Kiro credits ≈ $0.01 | active | [官方](https://kiro.dev/docs/models) |
| Kiro | GLM-5 | credit_multiplier | 0.5 Kiro credits ≈ $0.02 | active | [官方](https://kiro.dev/docs/models) |
| Kiro | GPT-5.6 Luna | credit_multiplier | 0.6 Kiro credits ≈ $0.024 | active | [官方](https://kiro.dev/docs/models) |
| Kiro | GPT-5.6 Sol | credit_multiplier | 2.4 Kiro credits ≈ $0.096 | active | [官方](https://kiro.dev/docs/models) |
| Kiro | GPT-5.6 Terra | credit_multiplier | 1.2 Kiro credits ≈ $0.048 | active | [官方](https://kiro.dev/docs/models) |
| Kiro | MiniMax M2.5 | credit_multiplier | 0.25 Kiro credits ≈ $0.01 | active | [官方](https://kiro.dev/docs/models) |
| Kiro | Qwen3 Coder Next | credit_multiplier | 0.05 Kiro credits ≈ $0.002 | active | [官方](https://kiro.dev/docs/models) |
| Roo Code（已停止） | 所选提供商模型（BYOK，历史） | provider_token_price | 不可量化（无固定倍率） | discontinued | [官方](https://roocodeinc.github.io/Roo-Code/) |
| Windsurf | Claude Opus 4.6 | fixed_prompt_credit | 6 prompt credits ≈ $0.24 | active | [官方](https://docs.windsurf.com/windsurf/models) |
| Windsurf | Claude Opus 4.7（low thinking） | fixed_prompt_credit | 20 prompt credits ≈ $0.8 | active | [官方](https://docs.windsurf.com/windsurf/models) |
| Windsurf | Claude Opus 4.7（medium thinking） | fixed_prompt_credit | 40 prompt credits ≈ $1.6 | active | [官方](https://docs.windsurf.com/windsurf/models) |
| Windsurf | SWE-1.6 | fixed_prompt_credit | 0 prompt credits ≈ $0 | active | [官方](https://docs.windsurf.com/windsurf/models) |

## 解释与边界

- `MTok` = 100 万 Token。原生 API 的输入、输出、缓存读取与缓存写入可分别计费；当前工作量情景不包含 cache write。
- Cursor 的 selected-model 行是官方声明的 API list-price pass-through，不表示 GPT‑5.6 一定已出现在 Cursor 当日选择器中。
- Kiro 的倍率作用于随任务复杂度变化的基础 Credits，因此不能诚实地换算成固定 Token 单价。
- Copilot 当前以 `$0.01 / AI credit` 按 Token 价格折算。Copilot 旧 premium-request 口径不用于本表的模型级对比。
- Windsurf 以每条用户 Prompt 的模型倍率计费，模型矩阵会动态变化；Cline 和 Roo Code 不发布固定平台 Credit 倍率，使用所选模型的提供商价格。
- CNY 模型的 USD 列仅用于横向比较，不是结算报价。自托管/合作方托管模型没有唯一的原厂 API 价格。
