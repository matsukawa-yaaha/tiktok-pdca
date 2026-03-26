#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
TIKTOK_DIR="$CLAUDE_DIR/tiktok-pdca"

echo "=== TikTok PDCA インストーラー ==="
echo ""

# 1. スキル定義をコピー
echo "[1/4] スキル定義をインストール中..."
mkdir -p "$CLAUDE_DIR/commands"
cp "$SCRIPT_DIR/commands/tiktok-pdca.md" "$CLAUDE_DIR/commands/tiktok-pdca.md"
echo "  -> ~/.claude/commands/tiktok-pdca.md"

# 2. スクリプトをコピー
echo "[2/4] スクリプトをインストール中..."
mkdir -p "$TIKTOK_DIR/scripts"
cp "$SCRIPT_DIR/scripts/postiz_api.py" "$TIKTOK_DIR/scripts/postiz_api.py"
cp "$SCRIPT_DIR/scripts/openai_api.py" "$TIKTOK_DIR/scripts/openai_api.py"
chmod +x "$TIKTOK_DIR/scripts/postiz_api.py"
chmod +x "$TIKTOK_DIR/scripts/openai_api.py"
echo "  -> ~/.claude/tiktok-pdca/scripts/"

# 3. 設定ファイル
echo "[3/4] 設定ファイルを準備中..."
if [ -f "$TIKTOK_DIR/config.json" ]; then
    echo "  -> config.json は既に存在します（スキップ）"
else
    cp "$SCRIPT_DIR/config.template.json" "$TIKTOK_DIR/config.json"
    echo "  -> ~/.claude/tiktok-pdca/config.json を作成しました"
    echo ""
    echo "  ⚠️  config.json にAPIキーを設定してください:"
    echo "     $TIKTOK_DIR/config.json"
    echo ""
    echo "  必要なキー:"
    echo "    - openai_api_key: OpenAI APIキー（画像生成用）"
    echo "    - postiz_api_key: Postiz APIキー（投稿管理用）"
fi

# 4. Python依存パッケージ
echo "[4/4] Python依存パッケージを確認中..."
if python3 -c "import openai, requests" 2>/dev/null; then
    echo "  -> openai, requests インストール済み"
else
    echo "  -> パッケージをインストール中..."
    pip install openai requests
fi

echo ""
echo "=== インストール完了 ==="
echo ""
echo "使い方:"
echo "  1. config.json にAPIキーを設定"
echo "  2. Claude Code で /tiktok-pdca を実行"
