# 个人结论仅供参考

我的初步判断是：这类产品不是不能做，但现阶段更适合定义为“`可做，但要谨慎评估，不建议低估难度`”。表面上看是分账、打款、KYC 这些功能组合，真正难的是支付链路稳定性、异常处理、合规约束和持续运营，这部分门槛通常高于功能开发本身。

核心原因有三点。
* 显性成本不低，`KYC / tax / bank linking / payout / notification` 都会持续产生第三方成本。
* 隐性成本更高，包括准备金占压和兜底、退票（可能引发后续一系列动作比如账户冻结等）、争议追偿、KYC 补件、人工审核和客服 support
* 这类业务对行业经验依赖很强，如果团队缺少支付、金融合规或相关垂直场景经验，遇到资金异常、账户风控或合作方政策变化时，处理不当容易带来直接亏损，甚至放大法务风险。

风险上，当前至少有三个需要重点关注。
* 获客层面，如果没有行业资历、案例或支付稳定性背书，前期不容易说服 `agency` 迁移。
* 合作方层面，底层支付能力受第三方约束明显，例如 `Dwolla` 条款对 `adult entertainment` 有明确限制，这意味着目标客群和支付合作方政策之间存在天然张力。
* 运营层面，实际会持续遇到退票、KYC 补件、风控冻结、payout 延迟等问题，很多都需要人工介入，不是上线后就能自动跑顺的业务。

所以更稳妥的结论不是“能不能复刻 Melon”，而是“在没有相关行业经验沉淀之前，是否值得承担这类业务复杂度和风险成本”。如果后续要推进，前提最好是先补齐有支付/金融合规经验的产品、研发或运营角色，否则即使产品能上线，后续也可能被异常处理和合作方约束拖入高成本区。

# Melon 产品概述

- Melon 是一个面向创作者经纪公司（Agency）的收入分账与回款自动化产品，核心不是内容运营，而是把“创作者收款后如何按协议分钱、催款、对账、周结”做成标准化工作流。
- 官方公开定位是 `Automatic payouts for agencies`；截至 `2026-03-13`，官网披露规模信号为 `900+ creators / 125+ agencies / $25m+ revenue shared`。
- 产品当前覆盖两类主流程：
  - `Creator Split`：创作者在 OnlyFans、Chaturbate 等平台收款后，Melon 自动向创作者扣回 agency 分成，并按周打款给 agency。
  - `Invoice Split`：基于 FansMetric 数据生成账单链接，通过短信或邮件向 creator 收款。
- 商业模式是交易抽成而不是席位费：对 agency 的收费从其 `agency cut` 的 `5%` 起(`50K$/Mo` `4.85%`， `100K$/Mo` `4.6%`， `500K$` contact sales)；referral recipient 额外支付 `2%` 转账费。
- 本质上，Melon 是 creator agency 生态中的 `payment layer`，不是全栈 agency OS。

# 参与角色

- `Agency`：创建 split、设定分成比例、查看回款、管理 referral/chat team 分账。
- `Creator`：接受邀请、连接银行账户、接收平台收入、被自动扣款或通过账单链接付款。
- `Referral / Chat Team / Additional Participant`：接收 agency 二次分账。
- `上游平台`：OnlyFans、Chaturbate 等，为 creator 提供原始收入来源。
- `支付合作方`：Stripe 负责 agency 侧 KYC、税务信息与 1099 交付；Plaid 负责 creator 银行连接；Dwolla 负责 ACH / funding source；Wise 支持部分跨境 USD 银行路径。
- `Melon`：负责规则、检测、编排、通知、账本与 payout。

# 应用场景

- Agency 管理多个 creator，需要稳定、透明地回收 agency 分成。
- Agency 需要给 referral、chat team 等第三方继续分账。
- 创作者与 agency 不希望继续依赖 Excel、截图、人工催款和手工转账。
- Agency 已有运营系统，但缺少金融工作流层，希望把“收钱、分钱、催钱、周结”独立出来。
- 国际 agency 或加拿大 creator 需要 USD 银行路径，但又不想自建跨境支付流程。

# 上下游依赖

- `上游依赖`
  - Creator 平台收入：OnlyFans、Chaturbate 等。
  - Creator 银行账户：Melon 依赖银行入账事件触发分账。
  - Invoice 数据源：Automated Invoicing 依赖 FansMetric。
- `中游关键依赖`
  - Stripe：agency 侧 KYC、tax reporting、tax form delivery。
  - Plaid：银行连接与账户验证。
  - Dwolla：支付账户、funding source、ACH 转账。
  - Wise：国际 agency / 加拿大 creator 的 USD 银行账户路径。
- `下游依赖`
  - Agency 银行账户：周度 payout 的最终落点。
  - Referral / Chat Team 收款账户：二次分账的最终落点。
  - Email / SMS 渠道：邀请、提醒、催收与异常通知。

# 核心流程图

```mermaid
flowchart LR
  A[Agency 注册] --> B[通过 Stripe 完成 KYC / Tax Onboarding]
  B --> C[Agency 创建 Split]
  C --> D[Creator 接受邀请并通过 Plaid 绑定银行]
  D --> E[OnlyFans / Chaturbate 向 Creator 打款]
  E --> F[Melon 检测入账并计算 Agency 应收]
  F --> G[通过 Dwolla / 支付合作方发起 ACH 扣款]
  G --> H[ACH 清算约 4 个工作日]
  H --> I[Melon 按周向 Agency payout]
  I --> J[可选: 向 Referral / Chat Team 二次分账]
  C --> K[可选: 启用 Invoice Split]
  K --> L[基于 FansMetric 生成账单]
  L --> M[通过短信 / 邮件发送支付链接]
  M --> N[Creator 直接付款]
```

# 用户旅程

## Agency Onboard

- Agency 注册 Melon，提交实体资料并完成基础 KYC / KYB。
- 公开文档显示，agency 端的 KYC / tax reporting 与 Stripe 有明确关联；共享页面中的补充截图也显示会跳转到 `connect.stripe.com/setup/`，说明这一环节大概率采用 Stripe-hosted onboarding。
- 配置自己的收款账户与 payout 路径。
- 如果是国际 agency，则需要额外准备 Wise USD 账户。
- Onboard 完成后进入 dashboard，可创建 split、查看 cashout / payout 历史并导出数据。

## Creator Onboard

- Creator 通过 agency 邀请链接进入 Melon。
- Creator 接受 split 条款，并通过 Plaid 连接银行账户。
- 如果是加拿大 creator，则需要准备 Wise 的美国银行信息。
- Creator 完成连接后，Melon 才能在检测到平台打款后发起自动扣款。

## Agency Create Split

- Agency 创建 `Creator Split`，设定分成比例、生效关系和收款方。
- 如果存在 referral/chat team，可创建 `Referral Split` 或 `Multi-participant split`。
- Split 创建后，Melon 开始持续监听创作者账户中的平台收入变化。
- 对于账单模式，agency 可启用 `Invoice Split`，由 Melon 发送付款链接并跟踪支付状态。

## Creator Get the Money From OnlyFans

- OnlyFans 等平台先把收入打到 creator 银行账户。
- Melon 检测到入账后，按 split 规则从 creator 账户扣回 agency 应收部分。
- ACH 清算通常需要约 `4` 个工作日。

## Agency Weekly Payout

- Melon 将当周已完成清算的 agency 应收款汇总，并按周发起 payout。
- 官方公开口径显示 payout 处理通常围绕美国周四 cutoff 运行，agency 实际收款通常体现在周五。
- 如果配置了 referral/chat team，二次分账通常在 agency 收款后的下一个 payout 周期处理。
- Agency 可在 dashboard 中查看 payout / cashout 历史，并导出 Excel 用于对账。

## Exception / Retry

- 如果 creator 银行连接失效，Melon 会要求 creator 重新连接银行账户，split 可能暂时进入 pending。
- 如果账户余额不足、ACH 失败或发生退票，相关交易不会进入正常 payout，而会转入异常处理与重试流程。
- 如果 agency 或 creator 的 KYC / KYB 资料不完整，支付能力可能被暂停，需补件后恢复。
- Stripe、Plaid、Dwolla 分别承接不同环节，任何一家供应商的审核、断连或策略变更都会放大 support 压力。
- 这说明 Melon 的真实能力不只是自动扣款，还包括异常识别、通知、人工 review 和运营兜底。

## Invoice Split

- 在 invoice 模式下，Melon 不再完全依赖平台入账后扣款，而是基于 FansMetric 数据生成应收账单。
- 系统通过邮件或短信向 creator 发送支付链接，creator 不必注册 Melon 账号也可完成付款。
- 该模式支持银行卡或银行账户支付，其中刷卡手续费由 creator 承担。

# 核心时序图

```mermaid
sequenceDiagram
  participant Agency as Agency
  participant Creator as Creator
  participant Platform as OnlyFans / Chaturbate
  participant Melon as Melon
  participant Stripe as Stripe
  participant Plaid as Plaid
  participant Dwolla as Dwolla / ACH Partner
  participant Referral as Referral / Chat Team

  Agency->>Stripe: 提交 KYC / tax 信息
  Stripe-->>Melon: 返回 requirements / tax status
  Agency->>Melon: 创建 split
  Melon-->>Creator: 发送邀请
  Creator->>Plaid: 连接银行账户
  Creator->>Melon: 接受 split 条款
  Platform->>Creator: 平台收入入账
  Melon->>Dwolla: 发起 ACH 扣款 / 跟踪清算状态
  Dwolla-->>Melon: 返回成功 / 失败 / 待处理状态
  Agency->>Melon: 可选配置 referral / chat team split
  Melon-->>Agency: 周度 payout 与报表
  Melon->>Melon: 基于 agency payout 计算第三方应分金额
  Melon-->>Referral: 下一个 payout 周期发起二次 payout
  Melon-->>Creator: 异常提醒 / invoice 支付链接
```

# 核心功能

- Creator Split：基于平台入账的自动分账。
- Agency KYC / Tax Onboarding：通过第三方完成主体核验、税务信息收集与税表交付。
- Referral Split：agency 对 referral/chat team 的二次分账。
- Multi-participant split：多参与方分账。
- Weekly payout：周度汇总结算给 agency。
- Bank linking：通过 Plaid 完成 creator 银行连接与后续 relink。
- Dashboard / Reporting：查看 active、pending、cancelled split，导出 Excel，查看 payout / cashout 历史。
- Automated Invoicing：基于 FansMetric 数据生成账单链接，并通过短信/邮件催收。
- Support / exception handling：处理资金不足、断连、补件、争议等异常。

# 竞争壁垒与核心风险

- `垂直工作流理解`
  - 壁垒：Melon 不是泛支付工具，而是深度贴合 creator agency 的“关系型分账”场景。
  - 风险：高度依赖 OnlyFans、Chaturbate 等上游平台的打款规则与生态稳定性，平台政策变化会直接冲击主流程。
- `金融正确性与异常处理`
  - 壁垒：真正难点在账本、状态机、异常处理、周结和争议处理，不在前端界面。
  - 风险：ACH 不是“发起即成功”，后续仍可能出现 insufficient funds、closed account、unauthorized return、bank dispute 与 clawback。公开资料显示 Melon 已把余额不足追缴、dispute 后追偿等场景做成正式规则，这意味着状态回滚、追偿、人工复核和 payout 延迟会持续存在。
- `信任与合规链路`
  - 壁垒：对 Stripe、Plaid、Dwolla、Wise 等合作方的接入与运营经验会形成门槛。
  - 风险：成人/订阅内容相关生态对支付合作方的接受度变化较大。`Dwolla` 在 `2025-01-21` 更新的账户条款中把 `adult entertainment` 列为 `Prohibited Activities`，说明这类客群存在直接的支付合作方准入风险；同时，KYC 不完整会直接造成 payout delayed/blocked，部分合作方还可能通过 reserve / hold 机制占压可分配余额。
- `多供应商编排能力`
  - 壁垒：Stripe、Plaid、Dwolla、Wise 的职责拆分本身就是产品复杂度，谁能把这条链路稳定跑通，谁就更难被简单复制。
  - 风险：任一供应商的审核、断连、政策或 API 变化，都会放大产品文案、support、合规和技术实现压力。对 Melon 这类产品来说，异常通常不是单点失败，而是会跨 Plaid、Dwolla、Stripe 与内部账本同步扩散。
- `嵌入式替代成本`
  - 壁垒：一旦 agency 把分账、报表和 payout 都迁移到 Melon，切换回 Excel 或手工流程的成本会上升。
  - 风险：更大的 agency OS 一旦内建 payouts 与 ledger，Melon 的差异化可能被压缩。
- `运营经验沉淀`
  - 壁垒：对 relink、insufficient funds、KYC 缺资料、cutoff 等异常的处理方式会形成隐性壁垒。
  - 风险：国际 agency 与加拿大 creator 路径会继续放大 KYC、支付、support 和文档一致性复杂度。

# 附录

## 名词解释

- `Split`：创作者与 agency 的分账规则。
- `Referral Split`：agency 再把自己收入的一部分分给第三方的规则。
- `Invoice Split`：按账单向 creator 收款，而不是等平台入账后再扣款。
- `KYC / KYB`：个人/企业身份与主体核验。
- `ACH`：美国银行间电子清算网络，成本低但到账慢且可退回。

## 成本分析

- `显性第三方成本`
  - `KYC / tax onboarding`：如采用 `Stripe Connect` 或同类方案，agency 端开户、KYC、tax forms 本身也是独立的第三方成本面。对 `generic Connect onboarding`，Stripe 官方仍是按方案和地区变化定价，不能用一个统一全球价格概括；但对 Melon 明确涉及且 Stripe US 已公开单价的模块，可以单独量化：
    - `Stripe Identity`：证件+自拍核验 ` $1.50 / verification `，`ID number lookup` 为 ` $0.50 / lookup `。
    - `Stripe Connect 1099`：向 IRS 电子申报 ` $2.99 / 1099 `，州电子申报 ` $1.49 / 1099 `，纸质邮寄 ` $2.99 / 1099 `，电子交付 `无额外费用`。
  - `银行连接与支付`：`Plaid` 未公开统一标准单价，`Dwolla` 也是 `custom pricing`，需以商务报价为准。
  - `通知与验证`：`Twilio SMS` 美国基础价从 ` $0.0083 / segment ` 起，另有 carrier fee；`Twilio Verify` 为 ` $0.05 / successful verification + $0.0083 / SMS `。以 `2,000` 条短信/月估算，基础短信费用约 ` $16.6/月 `。
  - `跨境能力`：如覆盖国际 agency 或加拿大 creator，`Wise` 一次性开通费 ` $31 `，接收 USD wire ` $6.11 / 笔 `。
  - `账单数据来源`：若不自建 invoice 数据能力，可接 `FansMetric`。其 Standard 为 ` $39/月/账号 `，Pro 为 ` $99/月/账号 `；按 `20` 个 creator 估算，月成本约 ` $780 - $1,980 `。
- `隐性但更关键的成本`
  - 长期成本大头通常来自支付合作方商务条款、KYC / 风控、准备金要求、退票与争议处理，以及人工审核和客服 support。
  - 如果是 `Plaid Link + Dwolla` 组合，公开文档没有说明平台运营方必须预先冻结固定金额的 reserve；但平台仍需承担负余额和退票兜底责任，这部分会以现金流占压和坏账风险的形式体现出来。

# 参考来源

- `Melon 官网`
  - URL：https://www.getmelon.io/
  - 用于支持：产品定位 `Automatic payouts for agencies`、官网规模数据 `900+ creators / 125+ agencies / $25m+ revenue shared`、周度 payout 叙述。
- `What is Melon?`
  - URL：https://help.getmelon.io/en/articles/8986654-what-is-melon
  - 用于支持：Melon 是 revenue-sharing platform；支持 OnlyFans、Chaturbate 等平台；核心是自动分账而非内容运营。
- `How does Melon work?`
  - URL：https://help.getmelon.io/en/articles/8358228-how-does-melon-work
  - 用于支持：creator 需接受邀请，并通过 Plaid 连接银行账户；agency 创建 split 后进入自动分账流程。
- `How the flow of funds works on Melon`
  - URL：https://help.getmelon.io/en/articles/8986666-how-the-flow-of-funds-works-on-melon
  - 用于支持：平台入账后同日触发 charge、ACH 约 `4` 个工作日清算、agency 每周五收款、第三方分账通常比 agency 晚一周。
- `How does payout timing work on Melon?`
  - URL：https://help.getmelon.io/en/articles/7879269-how-does-payout-timing-work-on-melon
  - 用于支持：Melon 多次扫描平台入账、charge 与 payout 的时间节奏、ACH `4` 个工作日窗口。
- `What is a Referral Split?`
  - URL：https://help.getmelon.io/en/articles/8136980-what-is-a-referral-split
  - 用于支持：Referral Split 的定义、weekly payouts、referral recipient `2%` fee。
- `Automated Invoicing with Melon`
  - URL：https://help.getmelon.io/en/articles/12005317-automated-invoicing-with-melon
  - 用于支持：Invoice Split 依赖 FansMetric、creator 可通过付款链接支付、刷卡手续费由 creator 承担、银行转账显示为 `0 fee`。
- `Melon for non-US/Canada agencies`
  - URL：https://help.getmelon.io/en/articles/9020125-melon-for-non-us-canada-agencies
  - 用于支持：Melon 支持部分国际 agency，但要求使用 Wise USD 银行账户；creator 仍主要限定在美国和加拿大。
- `Using Melon as a Canadian Creator – Wise US Bank Account Setup`
  - URL：https://help.getmelon.io/en/articles/11994736-using-melon-as-a-canadian-creator-wise-us-bank-account-setup
  - 用于支持：加拿大 creator 需要 Wise US bank account，OnlyFans 与 Melon 以 USD 路径运行。
- `Update your KYC info on Melon`
  - URL：https://help.getmelon.io/en/articles/8987119-update-your-kyc-info-on-melon
  - 用于支持：Melon 会因未满足 Stripe KYC 要求而延迟 payout，说明 Stripe 参与 agency 侧 KYC 环节。
- `Understanding Your 1099 Tax Forms with Melon [2024 Tax Season]`
  - URL：https://help.getmelon.io/en/articles/10543097-understanding-your-1099-tax-forms-with-melon-2024-tax-season
  - 用于支持：Melon 与 Stripe 合作处理 tax reporting，符合条件的用户可通过 Stripe Express 查看税表。
- `Stripe Connect Pricing`
  - URL：https://stripe.com/connect/pricing
  - 用于支持：Stripe Connect 的通用平台成本模型取决于平台方案与地区，不能用一个统一价格概括所有 onboarding / connected account 场景。
- `Stripe Pricing`
  - URL：https://stripe.com/pricing
  - 用于支持：Stripe US 公开列出了 `Identity` 单价，其中 `ID document and selfie verification = $1.50/verification`，`ID number lookup = $0.50/lookup`。
- `Stripe Connect: 1099`
  - URL：https://stripe.com/connect/1099
  - 用于支持：Stripe US 公开列出了 `1099` 单价，其中 `IRS e-file = $2.99/1099`、`state e-file = $1.49/1099`、`mail = $2.99/1099`、`e-delivery` 无额外费用。
- `Stripe Connect onboarding`
  - URL：https://docs.stripe.com/connect/custom/onboarding
  - 用于支持：平台可通过 hosted / API 方式完成 connected account onboarding，可映射 agency 侧 KYC 主流程。
- `Stripe tax form delivery`
  - URL：https://docs.stripe.com/connect/deliver-tax-forms
  - 用于支持：税表交付可由 Stripe Connect 承接，适用于 1099 交付这一合规环节。
- `Plaid Pricing`
  - URL：https://plaid.com/pricing/
  - 用于支持：Plaid 采用 one-time / subscription / per-request 三类计费模型；官方未在公开页披露统一单价。
- `Plaid Pricing and Billing`
  - URL：https://plaid.com/docs/account/billing/
  - 用于支持：Plaid 提供 `Pay as you go / Growth / Custom` 三类 plan；文档中的 `up to $6,000/month`、`over $2,000/month` 是适用规模提示而非公开报价；`Auth` 属一次性收费，`Transactions` 等属于按 Item 的持续订阅；partner 调用也会计入你的账单。
- `Plaid Link introduction`
  - URL：https://plaid.com/docs/link/#introduction-to-link
  - 用于支持：Plaid Link 是终端用户连接其金融账户的前端模块，可用于补充说明 creator 银行连接入口。
- `Dwolla Pricing`
  - URL：https://www.dwolla.com/pricing/
  - 用于支持：Dwolla 为 `custom pricing`，属于需商务确认的核心支付成本。
- `Dwolla Account Terms of Service`
  - URL：https://www.dwolla.com/legal/dwolla-account-terms-of-service
  - 用于支持：`2025-01-21` 更新版条款把 `adult entertainment` 列为 `Prohibited Activities`，说明成人内容相关客群存在明确的支付合作方政策风险。
- `Wise Business Pricing`
  - URL：https://wise.com/us/pricing/business/
  - 用于支持：Wise 一次性开通费 ` $31 `，接收 USD wire ` $6.11 / 笔 `。
- `Twilio SMS Pricing in United States`
  - URL：https://www.twilio.com/en-us/sms/pricing/us
  - 用于支持：美国短信基础价从 ` $0.0083 / segment ` 起，另有 carrier fee。
- `Twilio Verify Pricing`
  - URL：https://www.twilio.com/en-us/verify/pricing
  - 用于支持：美国短信验证价格为 ` $0.05 / successful verification + $0.0083 / SMS `。
- `FansMetric Pricing`
  - URL：https://fansmetric.com/pricing
  - 用于支持：FansMetric Standard ` $39/月/账号 `、Pro ` $99/月/账号 `，可作为 invoice 数据能力的第三方成本参考。
- `共享页面补充证据（非官方）`
  - URL：https://chatgpt.com/share/69b3d532-0b44-8000-8326-48a9bbcf9c8c
  - 用于支持：agency 端 KYC / Tax 页面跳转到 `connect.stripe.com/setup/` 的截图层面补充观察；只用于辅助判断，不单独支撑产品事实或数据。
