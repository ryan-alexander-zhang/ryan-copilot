# Feishu Custom Bot Notes

## Official docs

- Custom bot guide: https://open.feishu.cn/document/client-docs/bot-v3/add-custom-bot
- Message cards with custom bot: https://open.feishu.cn/document/common-capabilities/message-card/getting-started/send-message-cards-with-a-custom-bot

## Confirmed from official page metadata

- Custom bots use webhook push and support security options: keyword, IP allowlist, signature check.
- Message cards can be sent through custom bots.

## Webhook endpoint pattern

Feishu custom bot webhook endpoint pattern is:

- `https://open.feishu.cn/open-apis/bot/v2/hook/{token}`

This pattern is verified by direct endpoint probing (invalid token returns code `19001`).

## Implementation assumptions

The docs pages are JS-rendered and not fully retrievable as static HTML in this environment.
The script follows standard Feishu custom-bot payload conventions:

- `text` payload: `{"msg_type":"text","content":{"text":"..."}}`
- `post` payload: `{"msg_type":"post",...}`
- Optional signature fields: `timestamp`, `sign`

If the tenant enforces signature verification, provide `FEISHU_BOT_SECRET` at send time.
