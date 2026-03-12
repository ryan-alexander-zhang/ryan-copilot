# Melon Build Feasibility And Cost

- 产品名称：Melon
- 产品官网：<https://www.getmelon.io/>
- 分析日期：2026-03-12

## 1. If Building a Similar Product

- Suggested MVP scope：
  - 先只服务一个垂直场景中的单一角色，比如 agency 财务负责人
  - 先只做 revenue split，不同时做 invoice、affiliate、多参与方
- Suggested modules：
  - 账户/KYC
  - bank linking
  - split management
  - transaction detection
  - payout reporting
- Main build risks：
  - 资金链路准确率
  - 合规/KYC
  - 人工客服兜底成本
  - 上游平台依赖
- Cost considerations：
  - 工程实现成本：账户体系、状态机、报表、任务调度
  - 第三方基础设施成本：银行连接、支付、短信、数据平台
  - 运营成本：异常处理、人工支持、支付失败追踪
  - 合规成本：KYC、法务、税务资料收集、风控
  - 获客成本：若依赖关系链/行业社群，早期增长并不一定便宜
- Early validation or success criteria：
  - 是否能稳定识别 cashout 并正确生成 split
  - 是否能显著减少人工催款/对账时间
  - agency 是否愿意让真实 creator roster 进入系统

## 2. Build Cost Research

本节按新规则分为三层：

- `Confirmed current-product cost clues`
- `Confirmed vendor pricing`
- `Scenario-based build-cost estimates`

### 2.1 Confirmed current-product cost clues

| Cost item | Vendor or cost type | Confirmed or candidate | Official source | Official URL | Public pricing/billing rule | Billing unit | Evidence level | Key uncertainty or assumption |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Melon 平台收费 | Melon 自身定价 | Confirmed | Melon homepage pricing | <https://www.getmelon.io/> | 官网页面写明 fees start at `5%` of the agency's cut，并给出 `4.85%`、`4.6%` 的体量示例 | 占 agency cut 的百分比 | High | 这是 Melon 对客户收费，不等于其底层 vendor 成本 |
| 自动 invoicing 依赖外部数据平台 | FansMetric data dependency | Confirmed dependency | Melon help center | <https://help.getmelon.io/en/articles/12005317-automated-invoicing-with-melon> | 启用 automated invoicing 前必须先连接 FansMetric | 功能前置依赖 | High | 依赖关系明确，但 Melon 与 FansMetric 的商务采购条款未公开 |
| 国际 agency 账户前提 | Wise USD bank account | Confirmed dependency | Melon help center | <https://help.getmelon.io/en/articles/9020125-melon-for-non-us-canada-agencies> | 非美国/加拿大 agency 需有 Wise USD bank account | 使用前置条件 | High | 这是用户侧接入条件，不一定是 Melon 平台采购成本 |

### 2.2 Confirmed vendor pricing

| Cost item | Vendor or cost type | Confirmed or candidate | Official source | Official URL | Public pricing/billing rule | Billing unit | Evidence level | Key uncertainty or assumption |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 银行连接 / API 调用 | Plaid | Confirmed vendor for bank linking | Plaid pricing page | <https://plaid.com/pricing/> | 官方页写明 `Your first 200 API calls are free`，并说明后续为 pay-as-you-go 或 tailored volume pricing | API calls / custom volume pricing | Medium | 官方公开了免费额度，但公开页未稳定展示本案所需具体产品的单价，故不做精确量化 |
| 银行转账能力 | Dwolla | Confirmed vendor in Melon terms | Dwolla pricing page | <https://www.dwolla.com/pricing/> | 官方页写明 pricing is tailored to transaction volume, rails, and integration needs；无公开统一价格 | Custom / contact sales | High | 供应商确认，但官方不公开标准价，故 `Do not quantify` |
| 卡支付 | Stripe | Confirmed vendor signal | Stripe pricing | <https://stripe.com/pricing> | 标准在线卡支付 `2.9% + 30¢` | per successful card charge | High | 适用于标准在线支付；Melon 是否在所有支付场景下都按该计费未公开 |
| ACH 直接借记 | Stripe | Candidate / partially confirmed signal | Stripe pricing | <https://stripe.com/pricing> | `0.8%` for ACH Direct Debit | per ACH payment | High | Melon 帮助中心提到 Stripe 资料要求，但未公开确认所有 ACH 流程都走 Stripe |
| 平台抽佣式支付基础设施 | Stripe Connect | Candidate build option | Stripe pricing | <https://stripe.com/pricing> | `0.25% starting fee for platforms that deploy their own payments pricing to earn revenue on each transaction` | per transaction starting fee | High | 这是候选 build option，不可直接当作 Melon 已确认实际成本 |
| 订阅/账单软件费 | Stripe Billing | Candidate build option | Stripe Billing pricing | <https://stripe.com/billing/pricing> | `0.7%` of billing volume，公开页同时写明超出指定体量部分为 `0.67%` | % of billing volume | High | 可作为做类似 invoice 产品的候选方案，但 Melon 未公开确认使用 Stripe Billing |
| OnlyFans 经营数据平台 | FansMetric | Confirmed dependency / candidate paid vendor | FansMetric pricing | <https://fansmetric.com/pricing> | 定价页写明 `from $39/month per OnlyFans account`，页面可见 `Standard $39 per month per linked OnlyFans account` | monthly per linked account | High | Melon 是否按此标准零售价采购或有 B2B 协议价未公开 |
| 短信通知 | Twilio SMS US | Candidate build option | Twilio SMS pricing (US) | <https://www.twilio.com/en-us/sms/pricing/us> | 公开页显示分段计费；在公开表中，`150,001 - 300,000 messages` tier 为 `$0.0081`，`300,001 - 500,000` tier 为 `$0.0079`；另有 `$0.001` failed message processing fee | per message / per segment | High | Melon 未公开确认使用 Twilio；仅作为构建类似产品的候选短信基础设施价格 |
| Wise 收款账户 | Wise | Candidate / user prerequisite vendor | Wise receive pricing | <https://wise.com/us/pricing/receive> | 官方页明确这是 `Wise Account Fees for Receiving & Adding Money`，但本次稳定抓取未提取到适用于 Melon 场景的单一固定费率 | varies by currency / receive method | Low | 有官方价格页，但当前公开页面前端渲染较重，未稳定抽取到可直接引用的具体费用；`Do not quantify` |

### 2.3 Scenario-based build-cost estimates

以下不是 Melon 的已确认实际成本，而是“若做类似产品”基于官方计费规则能成立的成本模型。

| Cost item | Vendor or cost type | Confirmed or candidate | Official source | Official URL | Public pricing/billing rule | Billing unit | Evidence level | Key uncertainty or assumption |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 银行连接层 | Plaid | Candidate build option | Plaid pricing page | <https://plaid.com/pricing/> | 前 200 API calls free；后续 pay-as-you-go / volume pricing | API calls | Medium | 若产品早期只做小规模验证，可先落在免费额度或低量级；但正式成本需销售报价或更细产品线定价 |
| 银行转账层 | Dwolla | Candidate build option | Dwolla pricing page | <https://www.dwolla.com/pricing/> | custom pricing only | custom | Do not quantify | 适合说明“成本项存在且可能显著”，但没有公开价格不能给精确预算 |
| 卡支付/ACH 收款层 | Stripe | Candidate build option | Stripe pricing | <https://stripe.com/pricing> | card `2.9% + 30¢`；ACH Direct Debit `0.8%` | per transaction | High | 若产品用卡支付收 invoice，交易抽成会成为主要变动成本；不同付款方式成本结构差异很大 |
| 平台化分账层 | Stripe Connect | Candidate build option | Stripe pricing | <https://stripe.com/pricing> | starting fee `0.25%` for platforms earning revenue on each transaction | per transaction | High | 只有当你的产品采用 Stripe Connect 类平台化收费模型时才成立 |
| 账单与订阅层 | Stripe Billing | Candidate build option | Stripe Billing pricing | <https://stripe.com/billing/pricing> | `0.7%` of billing volume，部分区间 additional volume `0.67%` | % of billing volume | High | 如果产品的 invoice/billing 量不大，这可能是可接受软件税；若 volume 很大，则需单独核算 |
| 创作者数据层 | FansMetric | Candidate build option / confirmed dependency analog | FansMetric pricing | <https://fansmetric.com/pricing> | `Standard $39/month per linked OnlyFans account` | monthly per linked account | High | 若你的类似产品依赖第三方 creator data 平台，单账号月费会迅速累积；但是否一定要买 FansMetric 取决于产品路线 |
| 短信提醒层 | Twilio SMS US | Candidate build option | Twilio SMS pricing | <https://www.twilio.com/en-us/sms/pricing/us> | 公开页显示 15万-30万条为 `$0.0081`，30万-50万条为 `$0.0079`；failed fee `$0.001` | per message segment | High | 真正成本还受 carrier fee、A2P onboarding fee、消息分段数影响 |
| 邮件通知层 | Email provider | Candidate capability | N/A | N/A | 当前未确认 Melon 或建议方案使用哪家邮件服务商 | N/A | Do not quantify | 没有确认 vendor，不应该硬套 SendGrid/Mailgun 等价格 |
| 合规/KYC | KYC vendor or internal ops | Capability category | N/A | N/A | Melon 公开确认需要文档与验证，但未公开具体 KYC vendor 计费 | N/A | Do not quantify | 这是关键成本，但当前证据不足，不能给精确数字 |

### 2.4 Cost Conclusion

- `可以精确引用的成本` 主要来自官方公开 pricing 页面，例如 Stripe、FansMetric、Twilio 某些公开 tier。
- `可以确认存在但不能精确量化的成本` 包括 Dwolla custom pricing、Plaid 的超出免费额度部分、KYC vendor 成本、邮件 vendor 成本。
- 对“类似 Melon 的产品”而言，真正的大头通常不是单一 SaaS 订阅费，而是：
  - 交易抽成类成本
  - KYC/支付风控与异常处理
  - 外部数据依赖
  - 人工客服与失败交易兜底
- 如果要进一步做可执行预算，下一步必须先锁定：
  - 是否一定采用 Stripe / Dwolla / Plaid 这组栈
  - 预计月交易额
  - 月消息量
  - 月活 creator/account 数
  - KYC 审核量

## 3. Final Summary

如果只从公开信息推断，做一个“类似 Melon”的产品在功能层面并非不可行，但真正的难度不在 UI 或基础账单逻辑，而在银行连接、支付链路、KYC、异常处理和持续运营成本。成本上，能够精确定价的主要是部分外部基础设施；真正决定成败的高风险成本项，反而有不少只能确认存在、不能公开精算。因此，最现实的切入方式仍然是先缩小场景，再逐步验证支付与运营闭环。

## Sources

- 官网：<https://www.getmelon.io/>
- 条款：<https://www.getmelon.io/terms-of-service>
- How does Melon work：<https://help.getmelon.io/en/articles/8358228-how-does-melon-work>
- Automated invoicing：<https://help.getmelon.io/en/articles/12005317-automated-invoicing-with-melon>
- Non-US/Canada agencies：<https://help.getmelon.io/en/articles/9020125-melon-for-non-us-canada-agencies>
- Plaid pricing：<https://plaid.com/pricing/>
- Dwolla pricing：<https://www.dwolla.com/pricing/>
- Stripe pricing：<https://stripe.com/pricing>
- Stripe Billing pricing：<https://stripe.com/billing/pricing>
- FansMetric pricing：<https://fansmetric.com/pricing>
- Twilio SMS US pricing：<https://www.twilio.com/en-us/sms/pricing/us>
- Wise receive pricing：<https://wise.com/us/pricing/receive>
