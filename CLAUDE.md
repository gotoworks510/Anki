# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

LLMとの対話からAnkiカードを自動生成するPythonシステム。ユーザーがLLMに質問し、その回答から複数タイプのAnkiカードを生成してAnkiConnect APIを使用してAnkiに追加する。

## 主要コンポーネント

### 1. anki_schema.py
- AnkiCard: Ankiカードのデータ構造
- LearningContent: 学習内容の構造
- AnkiConnect API用のフォーマット変換機能

### 2. anki_client.py
- AnkiConnectClient: AnkiConnect APIとの通信クライアント
- 標準ライブラリ（urllib）を使用してHTTP通信
- カードの追加、デッキ作成、接続テスト機能

### 3. card_generator.py
- SmartCardGenerator: LLM回答からの高度なカード生成
- 複数のカードタイプ生成（定義、比較、手順、逆方向）
- 重要概念の自動抽出機能

### 4. llm_interface.py
- LearningSession: メインアプリケーションクラス
- インタラクティブモードとバッチモード対応
- セッション管理と統計機能

## 開発・テストコマンド

### テスト実行
```bash
# AnkiConnect接続テスト
python3 anki_client.py

# カード生成テスト
python3 card_generator.py

# デモモードでの統合テスト
python3 llm_interface.py --demo

# インタラクティブモード
python3 llm_interface.py
```

### 前提条件
- Ankiがインストールされ起動している
- AnkiConnectアドオンがインストールされている
- http://localhost:8765でAnkiConnect APIが利用可能

## アーキテクチャ特徴

### データフロー
1. ユーザー入力（質問）
2. LLM回答生成（現在はシミュレーション）
3. SmartCardGeneratorでカード生成
4. AnkiConnectClientでAnki追加
5. 結果レポート

### カード生成ロジック
- 正規表現による重要概念抽出
- 文構造解析による定義抽出
- 手順・プロセスの段階的分解
- 比較・対比の自動検出

### エラーハンドリング
- AnkiConnect接続エラーの適切な処理
- カード追加失敗時のフォールバック
- ユーザーフレンドリーなエラーメッセージ

## 拡張ポイント

### LLM統合
- OpenAI API, Claude API, ローカルLLMとの統合
- llm_interface.py の _generate_simulated_answer を実際のAPI呼び出しに置換

### カード生成改善
- 画像生成機能の追加
- 音声ファイルの埋め込み
- より高度な自然言語処理

### UI改善
- Web インターフェース
- デスクトップGUIアプリ
- 音声入力対応