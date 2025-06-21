# Anki学習フローシステム

LLMとの対話からAnkiカードを自動生成するシステム

## 機能

- LLMの回答から効果的なAnkiカードを自動生成
- AnkiConnect APIを使用してAnkiに直接カード追加
- 複数のカードタイプを生成（定義、比較、手順、逆方向）
- インタラクティブ学習セッション
- バッチ処理対応

## 必要な準備

1. Ankiをインストール
2. AnkiConnectアドオンをインストール
3. Ankiを起動（http://localhost:8765でAPIが利用可能）

## ファイル構成

- `anki_schema.py` - Ankiカードのデータ構造定義
- `anki_client.py` - AnkiConnect APIクライアント
- `card_generator.py` - LLM回答からのカード生成ロジック
- `llm_interface.py` - メインアプリケーション

## 使用方法

### デモモード
```bash
python3 llm_interface.py --demo
```

### インタラクティブモード
```bash
python3 llm_interface.py
```

トピック指定は `[トピック] 質問内容` の形式で入力

### プログラム統合
```python
from llm_interface import LearningSession

# セッション開始
session = LearningSession("学習デッキ")

# Q&Aペアを処理
result = session.process_qa_pair(
    question="質問内容",
    answer="LLMからの回答",
    topic="トピック"
)
```

## カード生成の特徴

1. **メイン回答カード** - 質問と回答をそのままカード化
2. **定義カード** - 重要概念の定義を抽出
3. **比較カード** - 比較・対比の内容を抽出
4. **手順カード** - プロセスや手順を段階的にカード化
5. **逆方向カード** - 回答から質問を推測するカード

## 生成例

質問: "Pythonの特徴について教えてください"
→ 12枚のカードを生成（定義、特徴、手順など）

## 拡張可能性

- 実際のLLM API統合（OpenAI、Claude APIなど）
- より高度なカード生成ロジック
- 音声入力/出力対応
- 画像・図表の自動生成