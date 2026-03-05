# Obsidian -> Feishu 群组发送流程

本仓库包含一个 Skill：`obsidian-feishu-group-sender`，用于把 Obsidian Markdown 笔记转换为飞书群消息并通过 Bot Webhook 发送。

- Skill 路径: `skills/obsidian-feishu-group-sender`
- 生成脚本: `skills/obsidian-feishu-group-sender/scripts/build_feishu_send_script.py`

## 1. 前置准备（飞书侧）

1. 在目标飞书群添加“自定义机器人”。
2. 获取机器人 Webhook 地址。
3. 按需开启安全设置：
- 关键词
- IP 白名单
- 签名校验（Secret）

官方文档：
- 自定义机器人使用指南: <https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot>
- 使用自定义机器人发送卡片消息: <https://open.feishu.cn/document/common-capabilities/message-card/getting-started/send-message-cards-with-a-custom-bot>

## 2. 环境变量

敏感信息不要写入文件，全部通过环境变量注入。

```bash
export FEISHU_BOT_WEBHOOK='https://open.feishu.cn/open-apis/bot/v2/hook/xxxx'
# 仅当群机器人开启签名校验时需要
export FEISHU_BOT_SECRET='your_signing_secret'
```

## 3. 从 Markdown 生成发送文件

```bash
python3 skills/obsidian-feishu-group-sender/scripts/build_feishu_send_script.py \
  --markdown /absolute/path/to/note.md \
  --msg-type text \
  --output-dir /tmp \
  --name-prefix note-to-feishu
```

默认输出（防竞态，文件名带时间戳+随机串）：
- `/tmp/note-to-feishu.<unique>.payload.json`
- `/tmp/note-to-feishu.<unique>.send.sh`

## 4. 发送消息

```bash
/tmp/note-to-feishu.<unique>.send.sh
```

脚本会：
1. 从 `FEISHU_BOT_WEBHOOK` 读取 webhook。
2. 若存在 `FEISHU_BOT_SECRET`，自动计算 `timestamp/sign` 并注入 payload。
3. 使用 `curl` 调用 webhook 发送消息。

## 5. Dry Run（只看请求体，不发消息）

```bash
DRY_RUN=1 /tmp/note-to-feishu.<unique>.send.sh
```

## 6. Markdown 转换规则

- 解析 front matter，仅保留 `tags`。
- 对 tags 执行归一化：去掉前缀 `output/`。
- 标签转为 `#tag` 行，拼在正文顶部。
- `--msg-type text`：转为纯文本结构（更稳）。
- `--msg-type post`：转为飞书 `post` 结构。

## 7. 常见问题

1. 返回鉴权错误
- 检查 `FEISHU_BOT_WEBHOOK` 是否正确。

2. 返回签名相关错误
- 说明群机器人开启了签名校验，但本地 `FEISHU_BOT_SECRET` 缺失或错误。

3. 返回关键词校验失败
- 机器人开启了关键词过滤，请确保消息文本包含约定关键词。

4. 没发到目标群
- 确认该 webhook 就是目标群对应机器人，不是其他群。

## 8. 已知说明

飞书文档页面为前端动态渲染；本仓库实现基于官方文档页面说明与标准 webhook 协议实践，适配自定义机器人常见配置（Webhook/关键词/IP 白名单/签名）。
