import json
import sys
from typing import Dict, List, Optional
from anki_client import AnkiConnectClient
from card_generator import SmartCardGenerator
from anki_schema import AnkiCard

class LearningSession:
    """LLMとの学習セッションを管理するクラス"""
    
    def __init__(self, deck_name: str = "LLM学習"):
        self.anki_client = AnkiConnectClient()
        self.card_generator = SmartCardGenerator()
        self.deck_name = deck_name
        self.session_history = []
        
        # AnkiConnect接続を確認
        if not self.anki_client.test_connection():
            raise Exception("AnkiConnectに接続できません。Ankiが起動していることを確認してください。")
        
        # デッキを作成（存在しない場合）
        if deck_name not in self.anki_client.get_deck_names():
            self.anki_client.create_deck(deck_name)
            print(f"新しいデッキ '{deck_name}' を作成しました。")
    
    def process_qa_pair(self, question: str, answer: str, topic: str = "") -> Dict:
        """質問と回答のペアを処理してAnkiカードを生成・追加"""
        
        print(f"\n📚 質問: {question}")
        print(f"💡 回答: {answer[:100]}...")
        
        # Ankiカードを生成
        cards = self.card_generator.generate_cards_from_llm_response(
            question, answer, topic
        )
        
        print(f"\n🎴 {len(cards)}枚のカードを生成しました")
        
        # カードをAnkiに追加
        successful_cards = []
        failed_cards = []
        
        for card in cards:
            card.deck_name = self.deck_name
            try:
                note_id = self.anki_client.add_note(card)
                if note_id:
                    successful_cards.append(card)
                    print(f"✅ カード追加成功: {card.front[:50]}...")
                else:
                    failed_cards.append(card)
                    print(f"❌ カード追加失敗: {card.front[:50]}...")
            except Exception as e:
                failed_cards.append(card)
                print(f"❌ エラー: {card.front[:50]}... - {str(e)}")
        
        # セッション履歴に記録
        session_record = {
            "question": question,
            "answer": answer,
            "topic": topic,
            "cards_generated": len(cards),
            "cards_added": len(successful_cards),
            "cards_failed": len(failed_cards)
        }
        self.session_history.append(session_record)
        
        return {
            "success": True,
            "cards_generated": len(cards),
            "cards_added": len(successful_cards),
            "cards_failed": len(failed_cards),
            "successful_cards": [card.front for card in successful_cards],
            "failed_cards": [card.front for card in failed_cards]
        }
    
    def interactive_mode(self):
        """インタラクティブモードでの学習セッション"""
        print("🎓 LLM学習セッションを開始します")
        print("📝 'quit'または'exit'で終了します")
        print("💭 トピックを指定する場合は '[トピック] 質問内容' の形式で入力してください")
        print("-" * 50)
        
        while True:
            try:
                # ユーザーからの入力を取得
                user_input = input("\n🤔 質問を入力してください: ").strip()
                
                if user_input.lower() in ['quit', 'exit', '終了', 'q']:
                    break
                
                if not user_input:
                    continue
                
                # トピックと質問を分離
                topic = ""
                question = user_input
                
                if user_input.startswith('[') and ']' in user_input:
                    parts = user_input.split(']', 1)
                    if len(parts) == 2:
                        topic = parts[0][1:].strip()
                        question = parts[1].strip()
                
                # ここではシミュレーションとして、簡単な回答を生成
                # 実際の使用では、LLM APIを呼び出す
                simulated_answer = self._generate_simulated_answer(question, topic)
                
                print(f"\n🤖 LLM回答:\n{simulated_answer}")
                
                # 確認を求める
                confirm = input("\n❓ この回答からAnkiカードを生成しますか？ (y/n): ").strip().lower()
                
                if confirm in ['y', 'yes', 'はい', 'h']:
                    result = self.process_qa_pair(question, simulated_answer, topic)
                    
                    print(f"\n📊 結果:")
                    print(f"   生成されたカード: {result['cards_generated']}枚")
                    print(f"   追加されたカード: {result['cards_added']}枚")
                    if result['cards_failed'] > 0:
                        print(f"   失敗したカード: {result['cards_failed']}枚")
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ エラーが発生しました: {e}")
        
        self.show_session_summary()
    
    def _generate_simulated_answer(self, question: str, topic: str) -> str:
        """シミュレーション用の回答生成（実際の使用ではLLM APIを使用）"""
        
        # デモ用の回答パターン
        demo_answers = {
            "python": """Pythonは1991年にGuido van Rossumによって開発されたプログラミング言語です。

主な特徴：
1. シンプルで読みやすい文法
2. 豊富なライブラリエコシステム
3. インタープリター型言語
4. オブジェクト指向とその他のパラダイムをサポート

Pythonは機械学習、Web開発、データ分析、自動化スクリプトなど幅広い分野で使用されています。""",
            
            "機械学習": """機械学習は、コンピューターがデータから自動的にパターンを学習し、予測や判断を行う技術です。

主なタイプ：
1. 教師あり学習 - ラベル付きデータから学習
2. 教師なし学習 - ラベルなしデータからパターンを発見
3. 強化学習 - 行動と報酬から学習

代表的なアルゴリズムには、線形回帰、決定木、ニューラルネットワークなどがあります。""",
            
            "web開発": """Web開発は、ウェブサイトやウェブアプリケーションを構築するプロセスです。

主な構成要素：
1. フロントエンド - ユーザーが見る部分（HTML、CSS、JavaScript）
2. バックエンド - サーバーサイドの処理（Python、PHP、Node.jsなど）
3. データベース - データの保存と管理

フレームワークを使用することで、効率的な開発が可能になります。"""
        }
        
        # トピックまたは質問から適切な回答を選択
        search_text = (topic + " " + question).lower()
        
        for key, answer in demo_answers.items():
            if key in search_text:
                return answer
        
        # デフォルト回答
        return f"""「{question}」について説明します。

これは{topic or '一般的な'}トピックに関する質問です。

主なポイント：
1. 基本的な定義と概念
2. 重要な特徴や性質
3. 実際の応用例や使用場面
4. 関連する技術や概念との関係

より詳細な情報については、専門的な資料を参照することをお勧めします。"""
    
    def batch_mode(self, qa_pairs: List[Dict[str, str]]):
        """バッチモードで複数のQ&Aペアを処理"""
        print(f"📦 バッチモード: {len(qa_pairs)}件のQ&Aペアを処理します")
        
        total_generated = 0
        total_added = 0
        
        for i, qa_pair in enumerate(qa_pairs, 1):
            print(f"\n[{i}/{len(qa_pairs)}] 処理中...")
            
            question = qa_pair.get('question', '')
            answer = qa_pair.get('answer', '')
            topic = qa_pair.get('topic', '')
            
            if question and answer:
                result = self.process_qa_pair(question, answer, topic)
                total_generated += result['cards_generated']
                total_added += result['cards_added']
        
        print(f"\n📊 バッチ処理完了:")
        print(f"   総生成カード数: {total_generated}枚")
        print(f"   総追加カード数: {total_added}枚")
    
    def show_session_summary(self):
        """セッションの要約を表示"""
        if not self.session_history:
            print("\n📊 セッション履歴がありません")
            return
        
        total_questions = len(self.session_history)
        total_generated = sum(record['cards_generated'] for record in self.session_history)
        total_added = sum(record['cards_added'] for record in self.session_history)
        
        print(f"\n📊 セッション要約:")
        print(f"   質問数: {total_questions}件")
        print(f"   生成されたカード: {total_generated}枚")
        print(f"   Ankiに追加されたカード: {total_added}枚")
        print(f"   成功率: {(total_added/total_generated*100) if total_generated > 0 else 0:.1f}%")

def main():
    """メイン関数"""
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        # デモモード
        print("🎮 デモモードで実行中...")
        session = LearningSession("デモ学習")
        
        demo_qa = {
            "question": "Pythonの特徴について教えてください",
            "answer": """Pythonは1991年にGuido van Rossumによって開発されたプログラミング言語です。

主な特徴：
1. シンプルで読みやすい文法
2. 豊富なライブラリ
3. インタープリター型言語
4. オブジェクト指向プログラミングをサポート

Pythonは機械学習やWeb開発など多くの分野で使用されています。""",
            "topic": "Python"
        }
        
        session.process_qa_pair(demo_qa["question"], demo_qa["answer"], demo_qa["topic"])
        session.show_session_summary()
    else:
        # インタラクティブモード
        try:
            session = LearningSession()
            session.interactive_mode()
        except Exception as e:
            print(f"❌ 初期化エラー: {e}")
            print("💡 Ankiが起動していて、AnkiConnectアドオンが有効になっていることを確認してください")

if __name__ == "__main__":
    main()