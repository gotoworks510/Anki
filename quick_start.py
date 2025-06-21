#!/usr/bin/env python3
"""
Anki学習システム クイックスタート
使い方に応じて最適なモードを自動選択
"""

import sys
import os
from llm_interface import LearningSession

def check_anki_connection():
    """Anki接続チェック"""
    try:
        from anki_client import AnkiConnectClient
        client = AnkiConnectClient()
        if client.test_connection():
            print("✅ AnkiConnect接続確認")
            return True
        else:
            print("❌ AnkiConnectに接続できません")
            print("💡 解決方法:")
            print("   1. Ankiを起動してください")
            print("   2. AnkiConnectアドオンが有効になっていることを確認")
            print("   3. http://localhost:8765 にアクセスできることを確認")
            return False
    except Exception as e:
        print(f"❌ 接続エラー: {e}")
        return False

def show_menu():
    """メインメニュー表示"""
    print("\n" + "="*50)
    print("🎓 Anki学習システム - クイックスタート")
    print("="*50)
    print("1. 📚 今すぐ学習開始（おすすめ）")
    print("2. 🎮 デモモード（システム確認）") 
    print("3. 📝 学習ガイド表示")
    print("4. 🔧 システム診断")
    print("5. 🚪 終了")
    print("="*50)

def quick_learning():
    """クイック学習モード"""
    print("\n🚀 学習セッションを開始します")
    
    # デッキ名の選択
    deck_options = [
        "今日の学習",
        "プログラミング", 
        "語学学習",
        "資格試験",
        "一般教養",
        "カスタム"
    ]
    
    print("\n📂 デッキを選択してください:")
    for i, deck in enumerate(deck_options, 1):
        print(f"   {i}. {deck}")
    
    try:
        choice = int(input("\n番号を選択 (1-6): ")) - 1
        if 0 <= choice < len(deck_options) - 1:
            deck_name = deck_options[choice]
        elif choice == len(deck_options) - 1:
            deck_name = input("カスタムデッキ名を入力: ").strip()
        else:
            deck_name = "今日の学習"
    except:
        deck_name = "今日の学習"
    
    print(f"\n📚 デッキ '{deck_name}' で学習を開始します")
    
    # 学習セッション開始
    session = LearningSession(deck_name)
    
    print("\n💡 使い方のコツ:")
    print("   • トピック指定: [Python] Pythonの特徴は？")
    print("   • 詳細度指定: [初心者向け] または [詳しく]")
    print("   • 終了: 'quit' または 'exit'")
    print("-" * 40)
    
    session.interactive_mode()

def demo_mode():
    """デモモード"""
    print("\n🎮 デモモードを実行します")
    
    demo_scenarios = [
        {
            "topic": "Python",
            "question": "Pythonの特徴について教えてください",
            "description": "プログラミング学習の例"
        },
        {
            "topic": "機械学習", 
            "question": "機械学習の基本的なアルゴリズムの種類は？",
            "description": "技術学習の例"
        },
        {
            "topic": "英語",
            "question": "現在完了形の使い方を説明してください",
            "description": "語学学習の例"
        }
    ]
    
    print("\nデモシナリオを選択:")
    for i, scenario in enumerate(demo_scenarios, 1):
        print(f"   {i}. {scenario['description']}")
    
    try:
        choice = int(input("番号を選択 (1-3): ")) - 1
        if 0 <= choice < len(demo_scenarios):
            scenario = demo_scenarios[choice]
        else:
            scenario = demo_scenarios[0]
    except:
        scenario = demo_scenarios[0]
    
    # デモ実行
    session = LearningSession("デモ学習")
    print(f"\n📚 質問: {scenario['question']}")
    
    # シミュレーション回答を生成
    answer = session._generate_simulated_answer(scenario['question'], scenario['topic'])
    print(f"🤖 回答: {answer}")
    
    # カード生成と追加
    result = session.process_qa_pair(
        scenario['question'], 
        answer, 
        scenario['topic']
    )
    
    print(f"\n📊 デモ結果:")
    print(f"   生成カード: {result['cards_generated']}枚")
    print(f"   追加成功: {result['cards_added']}枚")

def show_guide():
    """学習ガイド表示"""
    guide_text = """
📖 Anki学習システム 使い方ガイド

🎯 基本的な使い方:
   1. システム起動: python3 quick_start.py
   2. デッキ選択: 学習分野に応じてデッキを選択
   3. 質問入力: [トピック] 質問内容 の形式で入力
   4. 確認: LLM回答を確認してカード化を承認
   5. 学習: Ankiで生成されたカードを復習

🏷️  トピック指定の例:
   • [Python] オブジェクト指向プログラミングとは？
   • [英語] 過去完了形の使い分けを教えて
   • [数学] 微分と積分の関係について
   • [歴史] 江戸時代の特徴を説明して

💡 効果的な質問の仕方:
   ✅ 具体的: "Pythonのリスト内包表記の書き方は？"
   ❌ 曖昧: "Pythonについて教えて"
   
   ✅ 適切な粒度: "[Web開発] HTMLとCSSの役割の違い"
   ❌ 大きすぎる: "Web開発について全部教えて"

🔄 学習フロー:
   質問入力 → LLM回答 → カード生成 → Anki追加 → 復習学習

📚 デッキ管理のコツ:
   • 科目ごとにデッキを分ける
   • プロジェクトごとにデッキを作成
   • 定期的にAnkiで復習を実施

🎛️  カスタマイズ:
   • デッキ名: 学習内容に応じて設定
   • トピック: より詳細な分類が可能
   • 質問の詳細度: 初心者向け/詳しく等を指定可能
"""
    print(guide_text)
    input("\nエンターキーで戻る...")

def system_diagnosis():
    """システム診断"""
    print("\n🔧 システム診断を実行します...\n")
    
    # Python環境チェック
    print(f"✅ Python バージョン: {sys.version}")
    
    # 必要なモジュールチェック
    modules = ['urllib.request', 'json', 're', 'dataclasses']
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module}: インストール済み")
        except ImportError:
            print(f"❌ {module}: 見つかりません")
    
    # ファイル存在チェック
    files = [
        'anki_schema.py',
        'anki_client.py', 
        'card_generator.py',
        'llm_interface.py'
    ]
    
    for file in files:
        if os.path.exists(file):
            print(f"✅ {file}: 存在")
        else:
            print(f"❌ {file}: 見つかりません")
    
    # AnkiConnect接続チェック
    print("\n🔍 AnkiConnect接続テスト...")
    if check_anki_connection():
        print("✅ 全システム正常動作")
    else:
        print("⚠️  AnkiConnect接続に問題があります")
    
    input("\nエンターキーで戻る...")

def main():
    """メイン関数"""
    print("🔍 システムチェック中...")
    
    # 基本的なシステムチェック
    required_files = ['anki_client.py', 'llm_interface.py']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ 必要なファイルが見つかりません: {missing_files}")
        print("💡 正しいディレクトリで実行していることを確認してください")
        return
    
    # メインループ
    while True:
        show_menu()
        
        try:
            choice = input("\n選択してください (1-5): ").strip()
            
            if choice == '1':
                if check_anki_connection():
                    quick_learning()
                
            elif choice == '2':
                if check_anki_connection():
                    demo_mode()
                
            elif choice == '3':
                show_guide()
                
            elif choice == '4':
                system_diagnosis()
                
            elif choice == '5':
                print("\n👋 学習システムを終了します")
                break
                
            else:
                print("❌ 無効な選択です")
                
        except KeyboardInterrupt:
            print("\n\n👋 学習システムを終了します")
            break
        except Exception as e:
            print(f"\n❌ エラーが発生しました: {e}")

if __name__ == "__main__":
    main()