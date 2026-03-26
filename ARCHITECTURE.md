# TikTok PDCA 自動運用システム — アーキテクチャドキュメント

最終更新: 2026-03-26

---

## 1. システム概要

TikTokアカウントの運用（分析・戦略更新・コンテンツ企画・画像生成・投稿下書き作成）を、Claude Codeが毎日自律的に実行するPDCA自動化システム。

ユーザーの作業は「TikTokアプリで下書きを公開する」だけ。

---

## 2. ディレクトリ構成

```
~/.claude/
├── commands/
│   └── tiktok-pdca.md              ← [A] スキル定義（Claudeへの指示書）
│
└── tiktok-pdca/
    ├── config.json                  ← [B] APIキー・グローバル設定
    ├── ARCHITECTURE.md              ← 本ドキュメント
    │
    ├── scripts/
    │   ├── postiz_api.py            ← [C] Postiz APIラッパー
    │   └── openai_api.py            ← [D] OpenAI画像生成ラッパー
    │
    └── accounts/
        └── {account_id}/            ← [E] アカウント別データ（複数可）
            ├── concept.md           ← [E-1] ブランド設計書（不変）
            ├── strategy.md          ← [E-2] 現行戦略（毎日更新）
            └── history.json         ← [E-3] 投稿履歴（毎日追記）
```

---

## 3. 各コンポーネントの詳細

### [A] スキル定義: `~/.claude/commands/tiktok-pdca.md`

| 項目 | 内容 |
|---|---|
| 役割 | Claude Codeが `/tiktok-pdca` コマンドで実行する全手順を定義 |
| 更新タイミング | システムの振る舞いを変えたいときに手動編集 |

**定義している内容:**
- 起動時の処理（アカウント一覧表示 → 選択 or 新規作成）
- 新規アカウント作成フロー（Q1〜Q10の対話型ヒアリング）
- PDCAサイクルの実行手順（CHECK → ACT → PLAN → DO）
- 各ステップで使うスクリプトのコマンド例
- キャプション・画像プロンプトの設計指針
- エラーハンドリング方針
- 依存パッケージの確認方法

---

### [B] グローバル設定: `~/.claude/tiktok-pdca/config.json`

| 項目 | 内容 |
|---|---|
| 役割 | 外部API接続情報と画像生成パラメータの一元管理 |
| 更新タイミング | APIキーのローテーション時、画像モデル変更時 |

**定義しているフィールド:**

```json
{
  "openai_api_key": "sk-proj-...",     // OpenAI APIキー（画像生成用）
  "postiz_api_key": "d6ff...",         // Postiz APIキー（投稿管理用）
  "image_model": "gpt-image-1",       // 使用する画像生成モデル
  "image_size": "1024x1536",          // 画像サイズ（TikTok縦長）
  "postiz_base_url": "https://api.postiz.com/public/v1"  // Postiz APIエンドポイント
}
```

---

### [C] Postiz APIラッパー: `~/.claude/tiktok-pdca/scripts/postiz_api.py`

| 項目 | 内容 |
|---|---|
| 役割 | Postiz REST APIへのCLIインターフェース |
| 依存 | `requests` パッケージ、`config.json` |
| 更新タイミング | Postiz APIの仕様変更時 |

**提供する4コマンド:**

| コマンド | 用途 | 入力 | 出力 |
|---|---|---|---|
| `integrations` | 接続済みチャンネル一覧取得 | なし | JSON配列 |
| `analytics <id> [days]` | 指定チャンネルのKPI取得 | integration_id, 日数 | Followers/Views/Likes等のJSON |
| `upload <file>` | 画像ファイルをPostizにアップロード | ローカルファイルパス | `{"id": "...", "path": "https://..."}` |
| `create_draft` | TikTok下書き投稿を作成 | stdin経由のJSON | `{"postId": "..."}` |

**`create_draft` のstdin JSON仕様:**
```json
{
  "integration_id": "cmmu...",
  "content": "キャプション本文",
  "date": "2026-03-27T10:00:00.000Z",  // 省略時: 当日19:00 JST
  "images": [
    {"id": "uuid", "path": "https://uploads.postiz.com/xxx.png"}
  ]
}
```

**`create_draft` が生成するPostiz APIペイロード:**
- `type`: `"schedule"`（スケジュール投稿）
- `settings.__type`: `"tiktok"`
- `privacy_level`: `"PUBLIC_TO_EVERYONE"`
- `content_posting_method`: `"UPLOAD"`（カルーセル画像投稿）
- コメント: 有効 / デュエット・スティッチ: 無効

---

### [D] OpenAI画像生成ラッパー: `~/.claude/tiktok-pdca/scripts/openai_api.py`

| 項目 | 内容 |
|---|---|
| 役割 | OpenAI Images APIで画像を生成しローカルに保存 |
| 依存 | `openai` パッケージ、`config.json` |
| 更新タイミング | OpenAI APIの仕様変更時 |

**提供する1コマンド:**

| コマンド | 用途 | 入力 | 出力 |
|---|---|---|---|
| `generate <prompt> [index]` | 画像生成 | 英語プロンプト, インデックス番号 | `{"file_path": "/tmp/tiktok_pdca_image_{index}.png"}` |

**画像生成パラメータ:**
- モデル: `gpt-image-1`（config.jsonで変更可）
- サイズ: `1024x1536`（TikTok縦長）
- 品質: `high`
- レスポンス形式: `b64_json` または `url`（自動判定して保存）

---

### [E] アカウント別データ: `~/.claude/tiktok-pdca/accounts/{account_id}/`

アカウントを追加するたびにディレクトリが増える。cron実行時は `ls accounts/` で全アカウントを動的に検出。

#### [E-1] ブランド設計書: `concept.md`

| 項目 | 内容 |
|---|---|
| 役割 | アカウントの「憲法」。PDCAで参照するが原則として変更しない |
| 作成タイミング | 新規アカウント作成時（ヒアリング結果をAIが整理・深化） |
| 更新タイミング | アカウント方針の根本的な転換時のみ（手動） |

**定義しているセクション:**
- **基本情報**: TikTokユーザー名、Postiz Integration ID、投稿頻度・時間帯、参考アカウント
- **ポジショニング**: ターゲット x テーマ x 目的の一言コンセプト
- **ターゲットペルソナ**: 年齢・状況・心理状態・行動パターン
- **コンテンツピラー**: 3〜5本の柱（投稿テーマのカテゴリ）
- **トンマナ・世界観**: 語り口、雰囲気、テキストスタイル、画像スタイル、PR感の度合い
- **KPI目標**: フェーズ別の数値目標
- **禁止事項**: ブランドガイドライン上のNG

#### [E-2] 現行戦略: `strategy.md`

| 項目 | 内容 |
|---|---|
| 役割 | PDCAの[ACT]で毎回更新される、直近の運用方針 |
| 更新タイミング | 毎日のPDCAサイクル実行時に自動上書き |

**定義しているセクション:**
- **直近の方針**: 現フェーズの重点ポイント・改善方向
- **今週のコンテンツ方向性**: 攻めるテーマ・角度
- **改善メモ**: PDCAで蓄積された気づき（日付付き）

#### [E-3] 投稿履歴: `history.json`

| 項目 | 内容 |
|---|---|
| 役割 | テーマ重複防止、振り返り用の投稿ログ |
| 更新タイミング | 投稿下書き作成のたびに自動追記 |

**1レコードの構造:**
```json
{
  "date": "2026-03-27",
  "theme": "テーマの要約",
  "caption_preview": "キャプション先頭100文字",
  "image_count": 3,
  "postiz_id": "cmn6...",
  "status": "draft"
}
```

---

## 4. 自動実行（cron）

| 項目 | 内容 |
|---|---|
| 定義場所 | Claude Code セッション内 CronCreate |
| スケジュール | 毎日 17:03 JST |
| 有効期間 | セッション起動中のみ、7日で自動期限切れ |
| 対象 | `accounts/` 配下の全アカウント（動的検出） |

**実行フロー:**
```
cron (17:03 JST)
  └→ Claude Code が自律起動
       └→ ls accounts/ で全アカウントIDを取得
            └→ 各アカウントに対して:
                 ├→ concept.md / strategy.md / history.json を読み込み
                 ├→ concept.md から integration_id を抽出
                 ├→ [CHECK] postiz_api.py analytics で14日分KPI取得・分析
                 ├→ [ACT]   strategy.md を分析結果で更新
                 ├→ [PLAN]  翌日の投稿案を設計（テーマ重複チェック）
                 └→ [DO]    画像生成 → アップロード → 下書き作成 → 履歴追記
```

---

## 5. 外部サービス連携

```
┌──────────────┐        ┌──────────────┐        ┌──────────────┐
│  OpenAI API  │        │  Postiz API  │        │   TikTok     │
│              │        │              │        │              │
│ gpt-image-1  │        │ /analytics   │        │  下書き保存   │
│ 画像生成     │        │ /upload      │        │  ユーザーが   │
│              │        │ /posts       │        │  手動で公開   │
└──────┬───────┘        └──────┬───────┘        └──────┬───────┘
       │                       │                       │
       │ 画像バイナリ           │ 画像URL + 投稿データ    │ 下書き転送
       │                       │                       │
       └───────────┬───────────┘                       │
                   │                                   │
            ┌──────┴───────┐                           │
            │ Claude Code  │───────────────────────────┘
            │ (ローカル)    │        Postiz経由で自動転送
            │              │
            │ スキル定義    │
            │ Pythonスクリプト│
            │ アカウントデータ│
            └──────────────┘
```

---

## 6. 新規アカウント追加の流れ

1. ユーザーが `/tiktok-pdca` を実行し「新規」を選択
2. Q1〜Q10の対話ヒアリング（スキル定義に従い1問ずつ）
3. Q3でPostiz APIから `integrations` を取得し、対応するIDを選択
4. ヒアリング結果からAIが `concept.md` / `strategy.md` / `history.json` を生成
5. `accounts/{new_id}/` に保存
6. 次回のcron実行から自動的にPDCA対象に含まれる（動的検出のため設定変更不要）

---

## 7. 依存関係

| 依存 | バージョン | 用途 |
|---|---|---|
| Python 3.9+ | システム同梱 | スクリプト実行 |
| `openai` (PyPI) | latest | OpenAI Images API クライアント |
| `requests` (PyPI) | latest | Postiz REST API 通信 |
| Claude Code | CLI | オーケストレーター・AI判断エンジン |
| Postiz | SaaS | TikTok投稿スケジューリング・アナリティクス |
| OpenAI API | gpt-image-1 | カルーセル画像生成 |

---

## 8. 制約・既知の制限

- **cron はセッション依存**: Claude Code を閉じると停止、7日で自動期限切れ → 再設定が必要
- **TikTok公開は手動**: Postiz経由で下書きは自動作成されるが、TikTokアプリでの公開はユーザーが行う
- **アナリティクスの粒度**: Postiz APIが返すのは集計値のみ。個別投稿ごとのパフォーマンス比較はできない
- **画像にテキストオーバーレイなし**: 画像生成は背景のみ。テキストの重ね合わせはTikTokアプリ側で行う想定
