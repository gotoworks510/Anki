# 🎓 Anki LLM Learning System

**LLMとの対話からAnkiカードを自動生成するPythonシステム**

ユーザーがLLMに質問し、その回答から複数タイプのAnkiカードを自動生成してAnkiConnect APIを使用してAnkiに追加するシステムです。

## ✨ 特徴

- 🤖 **LLM回答からのスマートカード生成** - 定義、比較、手順、逆方向カードを自動生成
- 📊 **構造化データの直接インポート** - 表形式やJSON形式のデータを直接Ankiに登録
- 🔄 **AnkiConnect API統合** - Ankiとの直接連携で即座にカード追加
- 🏷️ **自動タグ付け** - トピックやカードタイプを自動で分類
- 📚 **複数の学習モード** - インタラクティブ、バッチ、直接インポート対応

## 🚀 クイックスタート

### 前提条件

1. **Ankiをインストール**
2. **AnkiConnectアドオンをインストール** ([ダウンロード](https://ankiweb.net/shared/info/2055492159))
3. **Ankiを起動** (http://localhost:8765でAPIが利用可能)

### インストール

```bash
git clone https://github.com/[username]/anki-llm-learning-system.git
cd anki-llm-learning-system
```

### 基本的な使用方法

#### 🎯 方法1: 構造化データの直接インポート

```python
from simple_import import import_to_anki

# LLMが生成したデータをそのまま貼り付け
data = """
A person seeking protection... (). asylum (政治的亡命)... immigration legal humanitarian
The petition was denied... (). inadmissibility (入国不許可)... immigration legal screening
"""

result = import_to_anki(data, "移民英語")
print(f"追加成功: {result['successful']}枚")
```

#### 🎯 方法2: シンプルな質問・回答ペア

```python
from simple_import import quick_import

pairs = [
    ("What is asylum?", "Protection for people fleeing persecution"),
    ("Define inadmissibility", "Legal grounds for denying entry"),
    ("What is naturalization?", "Process of becoming a citizen")
]

result = quick_import(pairs, "移民法用語", ["法律", "英語"])
```

#### 🎯 方法3: インタラクティブ学習

```python
from llm_interface import LearningSession

session = LearningSession("プログラミング学習")
session.interactive_mode()
```

### クイックスタートスクリプト

```bash
python3 quick_start.py
```

## 📁 プロジェクト構成

```
anki-llm-learning-system/
├── README.md                    # このファイル
├── CLAUDE.md                    # Claude Code用ガイド
├── DIRECT_IMPORT_GUIDE.md       # 直接インポートガイド
├── LEARNING_FLOW_GUIDE.md       # 学習フローガイド
├── anki_schema.py              # Ankiカードのデータ構造
├── anki_client.py              # AnkiConnect APIクライアント
├── card_generator.py           # LLM回答からのカード生成ロジック
├── llm_interface.py            # メインアプリケーション
├── direct_card_importer.py     # 構造化データインポーター
├── simple_import.py            # シンプルインポート関数
├── llm_integration_template.py # LLM API統合テンプレート
├── quick_start.py              # クイックスタートスクリプト
└── auto_delete_decks.py        # デッキ削除ユーティリティ
```

## 🎨 カード生成の特徴

### 自動生成されるカードタイプ

1. **📋 メイン回答カード** - 質問と回答をそのままカード化
2. **📖 定義カード** - 重要概念の定義を抽出
3. **⚖️ 比較カード** - 比較・対比の内容を抽出
4. **📝 手順カード** - プロセスや手順を段階的にカード化
5. **🔄 逆方向カード** - 回答から質問を推測するカード

### 対応データ形式

- **表形式** (タブ区切り、空白区切り、パイプ区切り)
- **JSON形式**
- **自然言語形式**

## 📊 使用例

### 移民法英語学習の例

```python
# 移民法用語データを直接インポート
immigration_data = """
A person seeking protection from persecution in their home country may apply for (). asylum (政治的亡命)<br>意味: (特に政治的理由による)亡命、庇護。 immigration legal humanitarian
The petitioner's application was denied due to a finding of (). inadmissibility (入国不許可)<br>意味: 入国不適格性、入国不許可事由。 immigration legal screening
"""

result = import_to_anki(immigration_data, "移民英語")
# → 10枚のカードが「移民英語」デッキに追加
```

### プログラミング学習の例

```python
# Python学習セッション
session = LearningSession("Python学習")

# 質問: [Python] オブジェクト指向プログラミングとは？
# → 自動的に複数のカード生成（定義、特徴、例など）
```

## 🔧 高度な使い方

### LLM APIとの統合

```python
from llm_integration_template import LLMIntegratedSession

# OpenAI APIまたはClaude APIと統合
session = LLMIntegratedSession("AI学習", llm_provider="openai")
session.smart_learning_session()
```

### バッチ処理

```python
qa_pairs = [
    {"question": "質問1", "answer": "回答1", "topic": "トピック1"},
    {"question": "質問2", "answer": "回答2", "topic": "トピック2"}
]

session = LearningSession("バッチ学習")
session.batch_mode(qa_pairs)
```

## 🛠️ 開発・カスタマイズ

### テスト実行

```bash
# AnkiConnect接続テスト
python3 anki_client.py

# カード生成テスト
python3 card_generator.py

# 統合テスト
python3 llm_interface.py --demo
```

### カスタマイズポイント

- **カード生成ロジック**: `card_generator.py`の`SmartCardGenerator`クラス
- **LLM統合**: `llm_integration_template.py`を参考に実際のAPI統合
- **データ解析**: `direct_card_importer.py`のパース機能

## 🤝 貢献

プルリクエストやイシューの報告を歓迎します！

1. このリポジトリをフォーク
2. 機能ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを開く

## 📄 ライセンス

MIT License

## 🆘 サポート

- [Issues](https://github.com/[username]/anki-llm-learning-system/issues) - バグ報告や機能要望
- [Discussions](https://github.com/[username]/anki-llm-learning-system/discussions) - 質問や議論

## 🔗 関連リンク

- [Anki](https://apps.ankiweb.net/) - 公式サイト
- [AnkiConnect](https://ankiweb.net/shared/info/2055492159) - アドオンページ
- [Claude Code](https://claude.ai/code) - 開発支援ツール

---

⭐ このプロジェクトが役に立ったら、ぜひスターをお願いします！