# TikTok PDCA 自動運用スキル

Claude Code用のTikTokアカウント自動運用ツールです。
AIがTikTokアカウントの分析・戦略立案・コンテンツ企画・画像生成・投稿下書き作成までを自動で行います。

あなたの作業は **「TikTokアプリで下書きを公開する」だけ** です。

---

## このツールでできること

- TikTokアカウントのパフォーマンス分析（フォロワー推移、エンゲージメント等）
- 分析データに基づく投稿戦略の自動更新
- 投稿テーマの企画とキャプション（概要欄）の自動作成
- カルーセル用画像の自動生成（AI画像生成）
- Postiz経由でTikTokに下書きを自動保存

---

## セットアップ手順（初回のみ）

### ステップ 0: 事前に用意するもの

始める前に、以下の3つを準備してください。

| 必要なもの | 説明 | 取得方法 |
|---|---|---|
| **Claude Code** | AIがコードを実行するためのツール | 下のステップ1で説明します |
| **OpenAI APIキー** | 投稿画像を自動生成するために必要 | 下のステップ3で説明します |
| **Postiz APIキー** | TikTokへの投稿管理に必要 | 下のステップ4で説明します |

---

### ステップ 1: Claude Code をインストールする

Claude Codeは、AIとチャットしながら作業を進められるツールです。

#### Mac の場合

1. **ターミナルを開く**
   - `Command + Space` を押して「ターミナル」と入力 → Enter

2. **以下のコマンドをコピーして貼り付け、Enter を押す**

   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

   > `npm: command not found` とエラーが出た場合は、先にNode.jsをインストールしてください:
   >
   > ```bash
   > curl -fsSL https://fnm.vercel.app/install | bash && source ~/.zshrc && fnm install --lts
   > ```
   >
   > 完了したら、もう一度 `npm install -g @anthropic-ai/claude-code` を実行してください。

3. **Claude Code を起動してログインする**

   ```bash
   claude
   ```

   ブラウザが開くので、Anthropicアカウントでログインしてください。
   （アカウントがなければその場で作成できます）

#### Windows の場合

1. **PowerShell を管理者として開く**
   - スタートメニューで「PowerShell」と検索 → 右クリック → 「管理者として実行」

2. **以下のコマンドを実行**

   ```powershell
   npm install -g @anthropic-ai/claude-code
   ```

   > `npm` が見つからない場合は https://nodejs.org/ からNode.jsをインストールしてください。

3. **Claude Codeを起動**

   ```powershell
   claude
   ```

---

### ステップ 2: このツールをダウンロード＆インストールする

1. **ターミナル（またはPowerShell）で以下を順番に実行する**

   ```bash
   git clone https://github.com/matsukawa-yaaha/tiktok-pdca.git
   ```

   ```bash
   cd tiktok-pdca
   ```

   ```bash
   chmod +x install.sh
   ```

   ```bash
   ./install.sh
   ```

   > `git: command not found` とエラーが出た場合:
   >
   > **Mac:**
   > ```bash
   > xcode-select --install
   > ```
   > ダイアログが出たら「インストール」をクリック。完了したら `git clone ...` からやり直してください。
   >
   > **Windows:**
   > https://git-scm.com/ からGitをインストールしてください。

2. **インストールが完了すると以下のメッセージが表示されます**

   ```
   === インストール完了 ===

   使い方:
     1. config.json にAPIキーを設定
     2. Claude Code で /tiktok-pdca を実行
   ```

---

### ステップ 3: OpenAI APIキーを取得する

このツールは投稿用の画像を自動生成するためにOpenAIのAPIを使います。

1. https://platform.openai.com/ にアクセスしてアカウントを作成（またはログイン）
2. 画面左のメニューから **「API keys」** をクリック
3. **「Create new secret key」** をクリック
4. キーが表示されるので **コピーして控えておく**（`sk-proj-...` で始まる文字列）

> APIキーは一度しか表示されません。必ずコピーしてどこかにメモしてください。
>
> OpenAI APIの利用には料金がかかります（画像1枚あたり数円〜数十円程度）。
> 事前にクレジットを追加しておいてください: https://platform.openai.com/settings/organization/billing/overview

---

### ステップ 4: Postiz APIキーを取得する

PostizはTikTokへの投稿を管理するサービスです。

1. https://postiz.com/ にアクセスしてアカウントを作成（またはログイン）
2. PostizにTikTokアカウントを連携する（Postizの画面の案内に従ってください）
3. 画面左下の **Settings（設定）** → **「API」** を開く
4. APIキーをコピーする

---

### ステップ 5: 設定ファイルにAPIキーを入力する

ステップ3・4で取得した2つのAPIキーを設定ファイルに書き込みます。

1. **ターミナルで以下を実行して設定ファイルを開く**

   **Mac:**
   ```bash
   open ~/.claude/tiktok-pdca/config.json
   ```

   > テキストエディタで開かない場合は:
   > ```bash
   > nano ~/.claude/tiktok-pdca/config.json
   > ```

   **Windows:**
   ```powershell
   notepad $env:USERPROFILE\.claude\tiktok-pdca\config.json
   ```

2. **以下のように書き換える（2箇所）**

   ```json
   {
     "openai_api_key": "ここにOpenAIのAPIキーを貼り付け",
     "postiz_api_key": "ここにPostizのAPIキーを貼り付け",
     "image_model": "gpt-image-1",
     "image_size": "1024x1536",
     "postiz_base_url": "https://api.postiz.com/public/v1"
   }
   ```

   - `openai_api_key`: ステップ3でコピーした `sk-proj-...` で始まるキー
   - `postiz_api_key`: ステップ4でコピーしたキー
   - それ以外の項目は変更不要です

3. **保存して閉じる**
   - nanoの場合: `Ctrl + O` → Enter → `Ctrl + X`
   - それ以外のエディタ: `Command + S`（Mac）/ `Ctrl + S`（Windows）で保存

---

## 使い方

### 基本的な使い方

1. **ターミナルでClaude Codeを起動する**

   ```bash
   claude
   ```

2. **チャット欄に以下を入力してEnter**

   ```
   /tiktok-pdca
   ```

3. **AIの質問に答えていく**

   初回はTikTokアカウントの情報をヒアリングされます（テーマ、ターゲット層、目標など）。
   質問に答えるだけでアカウント設定が完了します。

4. **自動でPDCAサイクルが実行される**

   設定完了後、AIが自動的に以下を実行します:
   - アカウントのパフォーマンス分析
   - 投稿戦略の立案
   - コンテンツ企画・キャプション作成
   - 画像の自動生成
   - Postizへの下書き保存

5. **TikTokアプリで下書きを確認して公開する**

   Postiz経由でTikTokに下書きが保存されるので、内容を確認して公開してください。

### 2回目以降

`/tiktok-pdca` を実行すると、登録済みアカウントの一覧が表示されます。
アカウントを選ぶだけで、自動的にPDCAサイクルが回ります。

---

## よくあるトラブル

### 「pip: command not found」と表示される

Pythonのパッケージ管理ツールが入っていません。以下を実行してください:

```bash
python3 -m ensurepip --upgrade
```

### 「openai パッケージが見つからない」と表示される

以下を実行してください:

```bash
pip install openai requests
```

または:

```bash
python3 -m pip install openai requests
```

### 「config.json が見つからない」と表示される

install.sh をもう一度実行してください:

```bash
cd tiktok-pdca
./install.sh
```

### 画像生成でエラーが出る

- OpenAI APIキーが正しいか確認してください
- OpenAIアカウントにクレジット（残高）があるか確認してください
  - https://platform.openai.com/settings/organization/billing/overview

### Postiz関連のエラーが出る

- Postiz APIキーが正しいか確認してください
- PostizにTikTokアカウントが連携されているか確認してください
