# LLM Price Catalogue

> Snapshot: `2026-08-07`. Official list prices and public agent billing rules only; check the linked source before purchase.

## 当前活跃模型速览

| 厂商 · 模型 | 定位 | 上下文 | 默认输入 / 输出（USD / MTok） | 长上下文规则 | 官方来源 |
|---|---|---:|---:|---|---|
| OpenAI · GPT-5.6 Sol | 旗舰 / 最强 Agent 与复杂工作流 | 1,050,000 | $5 / $30 | 超过 272K 输入 Token 的长上下文请求使用更高档位；cache write 单列。 | [官方](https://developers.openai.com/api/docs/models/gpt-5.6-sol) |
| Anthropic · Claude Opus 4.8 | 旗舰 / 复杂推理与 Agent | 1,000,000 | $5 / $25 | — | [官方](https://www.anthropic.com/claude/opus?app=claude-code) |
| Anthropic · Claude Fable 5 | 前沿 / 创作、代码与长程 Agent | — | $10 / $50 | API 已面向用户开放；仅收录 Fable 5，受限访问的 Mythos 5 不纳入。 | [官方](https://www.anthropic.com/news/claude-fable-5-mythos-5?type=company) |
| Google · Gemini 3.1 Pro | 旗舰 / 推理与多模态 | 1,000,000 | $2 / $12 | 当前为 Preview；超过 200K 输入使用高档位。 | [官方](https://ai.google.dev/gemini-api/docs/gemini-3) |
| xAI · Grok 4.3 | 旗舰 / 推理与通用 | 1,000,000 | $1.25 / $2.5 | 长上下文阈值为 200K 输入 Token。 | [官方](https://docs.x.ai/developers/pricing) |
| Mistral AI · Mistral Large 3 | 旗舰 / 通用 | — | $0.5 / $1.5 | — | [官方](https://mistral.ai/pricing/api/) |
| Cohere · Command A+ | 旗舰 / 企业 Agent、多语种与视觉 | 128,000 | $0 / $0 | 官方说明在达到速率限制前免费；生产规模使用需经 Model Vault / 商务路径确认。 | [官方](https://docs.cohere.com/docs/command-a-plus) |
| Meta · Llama 4 Maverick | 旗舰开源 / 多模态 | — | — | 开放权重；合作方 API 与自托管成本并非 Meta 的统一原生 API 刊例价。 | [官方](https://www.llama.com/llama-downloads/) |
| DeepSeek · DeepSeek-V4-Pro | 旗舰 / 推理与通用 | 1,000,000 | $0.435 / $0.87 | 价格页提示近期可能调整，工作流会持续检测。 | [官方](https://api-docs.deepseek.com/quick_start/pricing) |
| Alibaba Cloud · Qwen 3.7 Max | 旗舰 / 通用与复杂任务 | 1,000,000 | $1.668 / $5.004 | 价格为 1M 上下文以内的公开按量价。 | [官方](https://help.aliyun.com/en/model-studio/model-pricing) |
| Moonshot AI · Kimi K3 | 旗舰 / 长程编程与端到端知识工作 | 1,048,576 | $2.78 / $13.9 | — | [官方](https://platform.kimi.com/docs/pricing/chat-k3) |
| Zhipu AI · GLM-5.2 | 旗舰 / 1M 长程 Coding Agent | 1,000,000 | $1.112 / $3.892 | — | [官方](https://bigmodel.cn/pricing) |
| Baidu · ERNIE 5.1 | 旗舰 / 通用与企业 Agent | — | $0.556 / $2.502 | — | [官方](https://cloud.baidu.com/doc/qianfan-docs/s/Jm8r1826a) |
| ByteDance · Doubao-Seed-2.0 Pro | 旗舰 / 复杂指令与多模态 | — | $0.4448 / $2.224 | — | [官方](https://www.volcengine.com/docs/84458/1585097?lang=zh) |
| Tencent Cloud · Hunyuan Hy3 | 旗舰 / 通用与 Agent | — | $0.139 / $0.556 | — | [官方](https://cloud.tencent.com/document/product/1759/127342) |
| MiniMax · MiniMax-M2.7 | 代码 / Agent | — | $0.2919 / $1.1676 | — | [官方](https://platform.minimaxi.com/docs/guides/pricing-paygo) |
| StepFun · Step-3.5-Flash-2603 | 轻量 / 多模态与高吞吐 | — | $0.1 / $0.3 | — | [官方](https://platform.stepfun.ai/docs/en/guides/pricing/details) |

## 原生模型 API（全量）

| 厂商 | 模型 | 生命周期 | 定位 | 输入 / MTok | 输出 / MTok | 价格档位 | 来源 |
|---|---|---|---|---:|---:|---|---|
| Alibaba Cloud | Qwen 3.7 Max | active | 旗舰 / 通用与复杂任务 | CNY 12 | CNY 36 | 标准 | [官方](https://help.aliyun.com/en/model-studio/model-pricing) |
| Alibaba Cloud | Qwen 3.7 Plus | active | 均衡 / 通用 | CNY 2 | CNY 8 | ≤256K input；>256K input | [官方](https://help.aliyun.com/en/model-studio/model-pricing) |
| Anthropic | Claude Fable 5 | active | 前沿 / 创作、代码与长程 Agent | USD 10 | USD 50 | 标准 | [官方](https://www.anthropic.com/news/claude-fable-5-mythos-5?type=company) |
| Anthropic | Claude Haiku 4.5 | active | 轻量 / 高吞吐 | USD 1 | USD 5 | 标准 | [官方](https://docs.anthropic.com/en/docs/about-claude/pricing) |
| Anthropic | Claude Opus 4.8 | active | 旗舰 / 复杂推理与 Agent | USD 5 | USD 25 | 标准 | [官方](https://www.anthropic.com/claude/opus?app=claude-code) |
| Anthropic | Claude Sonnet 5 | active | 均衡 / 编码与生产 | USD 2 | USD 10 | 标准 | [官方](https://www.anthropic.com/claude/sonnet?hsLang=en-us) |
| Baidu | ERNIE 5.0 Thinking | active | 推理 / 复杂任务 | CNY 6 | CNY 24 | ≤32K input；32K–128K input | [官方](https://cloud.baidu.com/doc/qianfan-docs/s/Jm8r1826a) |
| Baidu | ERNIE 5.1 | active | 旗舰 / 通用与企业 Agent | CNY 4 | CNY 18 | ≤32K input；32K–128K input | [官方](https://cloud.baidu.com/doc/qianfan-docs/s/Jm8r1826a) |
| ByteDance | Doubao-Seed-2.0 Code | active | 代码 / Agentic Coding | CNY 3.2 | CNY 16 | ≤32K input；32K–128K input；128K–256K input | [官方](https://www.volcengine.com/docs/84458/1585097?lang=zh) |
| ByteDance | Doubao-Seed-2.0 Lite | active | 均衡 / 高性价比 | CNY 0.6 | CNY 3.6 | ≤32K input；32K–128K input；128K–256K input | [官方](https://www.volcengine.com/docs/84458/1585097?lang=zh) |
| ByteDance | Doubao-Seed-2.0 Mini | active | 轻量 / 最低单价 | CNY 0.2 | CNY 2 | ≤32K input；32K–128K input；128K–256K input | [官方](https://www.volcengine.com/docs/84458/1585097?lang=zh) |
| ByteDance | Doubao-Seed-2.0 Pro | active | 旗舰 / 复杂指令与多模态 | CNY 3.2 | CNY 16 | ≤32K input；32K–128K input；128K–256K input | [官方](https://www.volcengine.com/docs/84458/1585097?lang=zh) |
| Cohere | Command A | active | 企业 / RAG、工具调用与多语种 | USD 2.5 | USD 10 | 标准 | [官方](https://docs.cohere.com/docs/command-a) |
| Cohere | Command A+ | active | 旗舰 / 企业 Agent、多语种与视觉 | USD 0 | USD 0 | 限额免费 | [官方](https://docs.cohere.com/docs/command-a-plus) |
| DeepSeek | DeepSeek-V4-Flash | active | 轻量 / 推理、工具调用与代码 | USD 0.14 | USD 0.28 | 标准 | [官方](https://api-docs.deepseek.com/quick_start/pricing) |
| DeepSeek | DeepSeek-V4-Pro | active | 旗舰 / 推理与通用 | USD 0.435 | USD 0.87 | 标准 | [官方](https://api-docs.deepseek.com/quick_start/pricing) |
| Google | Gemini 3 Flash | active / preview | 均衡 / Agent 与多模态 | USD 0.5 | USD 3 | 标准 | [官方](https://ai.google.dev/gemini-api/docs/gemini-3) |
| Google | Gemini 3.1 Flash-Lite | active / preview | 轻量 / 高吞吐 | USD 0.25 | USD 1.5 | 标准 | [官方](https://ai.google.dev/gemini-api/docs/gemini-3) |
| Google | Gemini 3.1 Pro | active / preview | 旗舰 / 推理与多模态 | USD 2 | USD 12 | ≤200K input；>200K input | [官方](https://ai.google.dev/gemini-api/docs/gemini-3) |
| Meta | Llama 4 Maverick | active | 旗舰开源 / 多模态 (partner/self-hosted) | — | — | — | [官方](https://www.llama.com/llama-downloads/) |
| Meta | Llama 4 Scout | active | 长上下文开源 / 多模态 (partner/self-hosted) | — | — | — | [官方](https://www.llama.com/llama-downloads/) |
| MiniMax | MiniMax-M2-her | active | 专业 / 角色与交互 | CNY 2.1 | CNY 8.4 | 标准 | [官方](https://platform.minimaxi.com/docs/guides/pricing-paygo) |
| MiniMax | MiniMax-M2.5 | active | 均衡 / 代码与 Agent | CNY 2.1 | CNY 8.4 | 标准 | [官方](https://platform.minimaxi.com/docs/guides/pricing-paygo) |
| MiniMax | MiniMax-M2.5 Highspeed | active | 低延迟 / 均衡代码与 Agent | CNY 4.2 | CNY 16.8 | 标准 | [官方](https://platform.minimaxi.com/docs/guides/pricing-paygo) |
| MiniMax | MiniMax-M2.7 | active | 代码 / Agent | CNY 2.1 | CNY 8.4 | 标准 | [官方](https://platform.minimaxi.com/docs/guides/pricing-paygo) |
| MiniMax | MiniMax-M2.7 Highspeed | active | 低延迟 / 代码与 Agent | CNY 4.2 | CNY 16.8 | 标准 | [官方](https://platform.minimaxi.com/docs/guides/pricing-paygo) |
| Mistral AI | Devstral 2 | active | 代码 / Agent | USD 0.4 | USD 2 | 标准 | [官方](https://mistral.ai/pricing/api/) |
| Mistral AI | Mistral Large 3 | active | 旗舰 / 通用 | USD 0.5 | USD 1.5 | 标准 | [官方](https://mistral.ai/pricing/api/) |
| Mistral AI | Mistral Medium 3.5 | active | 均衡 / 企业 | USD 1.5 | USD 7.5 | 标准 | [官方](https://mistral.ai/pricing/api/) |
| Mistral AI | Mistral Small 4 | active | 轻量 / 高吞吐 | USD 0.15 | USD 0.6 | 标准 | [官方](https://mistral.ai/pricing/api/) |
| Moonshot AI | Kimi K2.6 | active | 均衡 / 多模态与 Agent | CNY 6.5 | CNY 27 | 标准 | [官方](https://platform.kimi.com/docs/pricing/chat-k26) |
| Moonshot AI | Kimi K2.7 Code | active | 代码 / Agent | CNY 6.5 | CNY 27 | 标准 | [官方](https://platform.kimi.com/docs/pricing/chat-k27-code) |
| Moonshot AI | Kimi K2.7 Code Highspeed | active | 低延迟 / 代码与 Agent | CNY 13 | CNY 54 | 标准 | [官方](https://platform.kimi.com/docs/pricing/chat-k27-code) |
| Moonshot AI | Kimi K3 | active | 旗舰 / 长程编程与端到端知识工作 | CNY 20 | CNY 100 | 标准 | [官方](https://platform.kimi.com/docs/pricing/chat-k3) |
| OpenAI | GPT-5.6 Luna | active | 高吞吐 / 最低单价 | USD 0.2 | USD 1.2 | ≤272K input；>272K input | [官方](https://developers.openai.com/api/docs/models/gpt-5.6-luna) |
| OpenAI | GPT-5.6 Sol | active | 旗舰 / 最强 Agent 与复杂工作流 | USD 5 | USD 30 | ≤272K input；>272K input | [官方](https://developers.openai.com/api/docs/models/gpt-5.6-sol) |
| OpenAI | GPT-5.6 Terra | active | 均衡 / 更低单价 | USD 2 | USD 12 | ≤272K input；>272K input | [官方](https://developers.openai.com/api/docs/models/gpt-5.6-terra) |
| StepFun | Step-3.5-Flash-2603 | active | 轻量 / 多模态与高吞吐 | USD 0.1 | USD 0.3 | 标准 | [官方](https://platform.stepfun.ai/docs/en/guides/pricing/details) |
| Tencent Cloud | Hunyuan Hy3 | active | 旗舰 / 通用与 Agent | CNY 1 | CNY 4 | 标准 | [官方](https://cloud.tencent.com/document/product/1759/127342) |
| Tencent Cloud | Hunyuan Hy3 Preview | active / preview | 预览 / 高规格通用 | CNY 2 | CNY 8 | 标准 | [官方](https://cloud.tencent.com/document/product/1759/127342) |
| Zhipu AI | GLM-5.2 | active | 旗舰 / 1M 长程 Coding Agent | CNY 8 | CNY 28 | 标准 | [官方](https://bigmodel.cn/pricing) |
| Zhipu AI | GLM-5V-Turbo | active | 多模态 / 视觉 Agent | CNY 5 | CNY 22 | <32K input；≥32K input | [官方](https://bigmodel.cn/pricing) |
| xAI | Grok 4.3 | active | 旗舰 / 推理与通用 | USD 1.25 | USD 2.5 | <200K input；≥200K input | [官方](https://docs.x.ai/developers/pricing) |
| xAI | Grok Build 0.1 | active | 代码 / 构建 Agent | USD 1 | USD 2 | <200K input；≥200K input | [官方](https://docs.x.ai/developers/pricing) |

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
| Kiro | Claude Opus 4.8 | credit_multiplier | 2.2 Kiro credits ≈ $0.088 | active | [官方](https://kiro.dev/docs/models) |
| Kiro | Claude Sonnet 5 | credit_multiplier | 1.3 Kiro credits ≈ $0.052 | active | [官方](https://kiro.dev/docs/models) |
| Kiro | GLM-5.2 | credit_multiplier | 0.5 Kiro credits ≈ $0.02 | active | [官方](https://kiro.dev/docs/models) |
| Kiro | GPT-5.6 Luna | credit_multiplier | 0.6 Kiro credits ≈ $0.024 | active | [官方](https://kiro.dev/docs/models) |
| Kiro | GPT-5.6 Sol | credit_multiplier | 2.4 Kiro credits ≈ $0.096 | active | [官方](https://kiro.dev/docs/models) |
| Kiro | GPT-5.6 Terra | credit_multiplier | 1.2 Kiro credits ≈ $0.048 | active | [官方](https://kiro.dev/docs/models) |
| Kiro | MiniMax M2.5 | credit_multiplier | 0.25 Kiro credits ≈ $0.01 | active | [官方](https://kiro.dev/docs/models) |
| Kiro | Qwen3 Coder Next | credit_multiplier | 0.05 Kiro credits ≈ $0.002 | active | [官方](https://kiro.dev/docs/models) |
| Windsurf | SWE-1.6 | fixed_prompt_credit | 0 prompt credits ≈ $0 | active | [官方](https://docs.windsurf.com/windsurf/models) |

## 解释与边界

- `MTok` = 100 万 Token。原生 API 的输入、输出、缓存读取与缓存写入可分别计费；当前工作量情景不包含 cache write。
- Cursor 的 selected-model 行是官方声明的 API list-price pass-through，不表示 GPT‑5.6 一定已出现在 Cursor 当日选择器中。
- Kiro 的倍率作用于随任务复杂度变化的基础 Credits，因此不能诚实地换算成固定 Token 单价。
- Copilot 当前以 `$0.01 / AI credit` 按 Token 价格折算。Copilot 旧 premium-request 口径不用于本表的模型级对比。
- Windsurf 以每条用户 Prompt 的模型倍率计费，模型矩阵会动态变化；Cline 不发布固定平台 Credit 倍率，使用所选模型的提供商价格。
- 本报告实行活跃白名单：已下线、迁移或仅历史可用的模型与 Agent 产品不保留为报告条目。Preview 仍在官方 API 中可用，因此会标注为 Preview 而不与下线混淆。
- CNY 模型的 USD 列仅用于横向比较，不是结算报价。自托管/合作方托管模型没有唯一的原厂 API 价格。
