# TikTok PDCA 自動運用スキル

Claude Code用のTikTokアカウント自動運用ツール。PDCAサイクル（分析→戦略更新→企画→投稿下書き作成）を自律的に実行します。

## できること

- TikTokアカウントのパフォーマンス分析（Postiz経由）
- データに基づく戦略の自動更新
- 投稿コンテンツの企画・キャプション作成
- カルーセル用画像の自動生成（OpenAI gpt-image-1）
- Postizへの下書き自動保存

## 必要なもの

- [Claude Code](https://claude.ai/claude-code)
- Python 3.9+
- OpenAI APIキー（画像生成用）
- [Postiz](https://postiz.com/) アカウント + APIキー

## インストール

```bash
git clone https://github.com/matsukawa-yaaha/tiktok-pdca.git
cd tiktok-pdca
chmod +x install.sh
./install.sh
```

## セットアップ

インストール後、`~/.claude/tiktok-pdca/config.json` にAPIキーを設定:

```json
{
  "openai_api_key": "sk-proj-...",
  "postiz_api_key": "your-postiz-api-key",
  "image_model": "gpt-image-1",
  "image_size": "1024x1536",
  "postiz_base_url": "https://api.postiz.com/public/v1"
}
```

## 使い方

Claude Codeで以下を実行:

```
/tiktok-pdca
```

初回はアカウント作成のヒアリングが始まります。2回目以降は自動でPDCAサイクルが実行されます。
