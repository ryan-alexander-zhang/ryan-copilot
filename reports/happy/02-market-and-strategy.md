# Happy 仓库流程分析 02: Market And Strategy

## 本报告边界

这不是常规市场竞品分析，而是围绕这次代码拆解，解释 Happy 在产品策略上为什么要采用“本地 agent 远程操控”模式，以及这种模式对多 agent / skills 的影响。

## 产品定位复原

### 已确认事实

- README 明确把 Happy 定义为 `Mobile and Web Client for Claude Code & Codex`，强调“用手机控制 Claude Code 或 Codex”。
  - 证据: `repos/happy/README.md`

- README 明确写出使用方式是“用 `happy` 代替 `claude`，用 `happy codex` 代替 `codex`”。
  - 证据: `repos/happy/README.md`

### 推测

- Happy 的真正产品定位不是新的 coding agent，而是“agent remote companion”。
  - 置信度: High

## 为什么它没有选择服务端代跑 Codex

### 已确认事实

- 本地 `happy codex` 会直接连本机 `codex mcp`/`mcp-server`。
  - 证据: `repos/happy/packages/happy-cli/src/codex/codexMcpClient.ts:94-170`

- Happy Server 主要承担 session/machine/update 的同步和 RPC 转发，不是 provider 执行层。
  - 证据: `repos/happy/packages/happy-cli/src/api/apiSession.ts:131-160`
  - 证据: `repos/happy/docs/session-protocol.md:7-28`

### 这样设计的战略收益

1. 复用现成 agent 能力。
Happy 不需要复刻 Codex/Claude 的推理、tool calling、resume、subagent、skills。

2. 避免把代码仓库上传到 Happy 云端执行。
这对开发者心理安全和隐私都更友好。

3. 兼容多个 agent 后端。
仓库结构已经显示 Happy 同时支持 Claude、Codex、Gemini，说明它的护城河更像“控制层与体验层”，不是模型能力本身。

4. 跟随底层 agent 演进。
Codex 新增更强的 skills、多 agent、patch/workflow 能力时，Happy 理论上只需更新适配层和 UI 协议。

## 对多 agent 的产品策略含义

### 已确认事实

- Happy 自己的 session protocol 明确把 `subagent` 当作一等概念。
  - 证据: `repos/happy/docs/session-protocol.md:36-68`

- Codex mapper 会把 provider 产生的 subagent 标记成统一 envelope。
  - 证据: `repos/happy/packages/happy-cli/src/codex/utils/sessionProtocolMapper.ts:84-110`
  - 证据: `repos/happy/packages/happy-cli/src/codex/utils/sessionProtocolMapper.ts:179-220`

### 这意味着什么

- Happy 想支持的是“观察和交互多 agent”，而不是“自己成为多 agent orchestrator”。
- 它对上层 UI 暴露的是统一结构:
  - turn
  - tool call
  - permission
  - subagent start/stop
- 这样它就能用同一套移动端界面，承接 Claude Task、Codex subagent、未来 ACP agent。

## 对 skills 的产品策略含义

### 已确认事实

- 仓库内没有发现独立 skills 引擎、skill registry、`SKILL.md` 解析和匹配逻辑。
- daemon 只是负责拉起 agent，并为 agent 注入环境变量。
  - 证据: `repos/happy/packages/happy-cli/src/daemon/run.ts:268-330`

### 推测

- Happy 对 skills 的策略是“保持透明，不介入底层语义”。
  - 置信度: High

也就是说:

- skills 属于 agent runtime
- Happy 属于 control plane / presentation layer

这是非常合理的边界，因为如果 Happy 自己也做 skill 编排，就会和 Claude/Codex 的原生能力打架，适配成本会指数上升。

## 替代方案与真实差异

用户真实可替代方案不是另一个模型，而是:

1. 只在电脑终端里跑 Codex。
2. 用远程桌面/VNC/SSH 看终端。
3. 自己做一套 Telegram/Slack/网页层的 agent wrapper。

Happy 的差异化价值在于:

- 面向 agent 的专用协议，而不是屏幕流。
- 结构化工具事件和权限审批，而不是看原始终端输出。
- 支持 session 级加密同步和设备切换。
- 兼容多 provider，不绑死单一模型厂商。

## 风险与约束

### 技术风险

- Happy 高度依赖底层 CLI 的事件稳定性。
- Codex CLI 的 MCP 事件格式一旦变化，Happy 适配层就要跟。

### 产品风险

- 如果底层 agent 官方自己做出更成熟的移动端控制台，Happy 的差异化会被侵蚀。

### 体验风险

- 手机只适合审批、观察、发短指令，不适合长时间深度编码。
- 所以 Happy 更像“补全场景”，不是主战场。

### 生态依赖风险

- 多 agent / skills 越强，Happy 越要保持“不过度抽象”，否则会丢语义。

## 结论

从代码看，Happy 的核心战略不是“做更强的 agent”，而是“做 agent 的远程控制面板”。  
因此它对多 agent 与 skills 的最佳策略就是现在这种边界:

- 底层 agent 决定如何思考、何时开子代理、如何使用 skills
- Happy 负责启动、转发、加密、审批、展示和跨设备切换

这个边界是清晰且正确的。
