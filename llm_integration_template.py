"""
LLM API統合テンプレート
実際のLLM APIと統合するための拡張例
"""

import os
import json
from typing import Dict, List, Optional
from llm_interface import LearningSession

class LLMIntegratedSession(LearningSession):
    """実際のLLM APIと統合した学習セッション"""
    
    def __init__(self, deck_name: str = "LLM学習", llm_provider: str = "openai"):
        super().__init__(deck_name)
        self.llm_provider = llm_provider
        self.setup_llm()
    
    def setup_llm(self):
        """LLM APIの設定"""
        if self.llm_provider == "openai":
            # OpenAI API設定例
            self.api_key = os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                print("⚠️  OPENAI_API_KEYが設定されていません")
                print("📝 export OPENAI_API_KEY='your-api-key' を実行してください")
        
        elif self.llm_provider == "claude":
            # Claude API設定例
            self.api_key = os.getenv("ANTHROPIC_API_KEY")
            if not self.api_key:
                print("⚠️  ANTHROPIC_API_KEYが設定されていません")
                print("📝 export ANTHROPIC_API_KEY='your-api-key' を実行してください")
    
    def call_llm_api(self, question: str, context: str = "") -> str:
        """LLM APIを呼び出して回答を生成"""
        
        # 学習用プロンプトテンプレート
        prompt = f"""
あなたは優秀な教師です。以下の質問に対して、Ankiカード学習に適した形で回答してください。

回答の要件：
1. 明確で簡潔な説明
2. 重要なポイントは箇条書きで整理
3. 専門用語は定義も含めて説明
4. 実例や比較があれば含める
5. 段階的な手順がある場合は番号付きで整理

質問: {question}

{context and f"追加コンテキスト: {context}" or ""}

回答:"""
        
        if self.llm_provider == "openai":
            return self._call_openai_api(prompt)
        elif self.llm_provider == "claude":
            return self._call_claude_api(prompt)
        else:
            # フォールバック: シミュレーション回答
            return self._generate_simulated_answer(question, "")
    
    def _call_openai_api(self, prompt: str) -> str:
        """OpenAI API呼び出し（実装例）"""
        try:
            # import openai  # pip install openai
            # 
            # response = openai.ChatCompletion.create(
            #     model="gpt-3.5-turbo",
            #     messages=[
            #         {"role": "system", "content": "あなたは優秀な教師です。"},
            #         {"role": "user", "content": prompt}
            #     ],
            #     max_tokens=1000,
            #     temperature=0.7
            # )
            # return response.choices[0].message.content
            
            # 実装プレースホルダー
            return "OpenAI APIとの統合が必要です。コメントアウトされたコードを参照してください。"
            
        except Exception as e:
            print(f"❌ OpenAI API呼び出しエラー: {e}")
            return self._generate_simulated_answer(prompt, "")
    
    def _call_claude_api(self, prompt: str) -> str:
        """Claude API呼び出し（実装例）"""
        try:
            # import anthropic  # pip install anthropic
            # 
            # client = anthropic.Anthropic(api_key=self.api_key)
            # response = client.messages.create(
            #     model="claude-3-sonnet-20240229",
            #     max_tokens=1000,
            #     messages=[
            #         {"role": "user", "content": prompt}
            #     ]
            # )
            # return response.content[0].text
            
            # 実装プレースホルダー
            return "Claude APIとの統合が必要です。コメントアウトされたコードを参照してください。"
            
        except Exception as e:
            print(f"❌ Claude API呼び出しエラー: {e}")
            return self._generate_simulated_answer(prompt, "")
    
    def smart_learning_session(self):
        """スマートな学習セッション（AI回答付き）"""
        print("🤖 AI統合学習セッションを開始します")
        print("📝 実際のLLMが回答を生成します")
        print("💡 トピックを明確に指定すると、より良い回答が得られます")
        print("-" * 60)
        
        while True:
            try:
                user_input = input("\n🤔 質問を入力してください: ").strip()
                
                if user_input.lower() in ['quit', 'exit', '終了', 'q']:
                    break
                
                if not user_input:
                    continue
                
                # トピックと質問を分離
                topic = ""
                question = user_input
                context = ""
                
                if user_input.startswith('[') and ']' in user_input:
                    parts = user_input.split(']', 1)
                    if len(parts) == 2:
                        topic = parts[0][1:].strip()
                        question = parts[1].strip()
                        context = f"この質問は{topic}に関するものです。"
                
                print(f"\n🤖 LLMに問い合わせ中...")
                
                # 実際のLLM APIを呼び出し
                llm_answer = self.call_llm_api(question, context)
                
                print(f"\n💡 LLM回答:\n{llm_answer}")
                
                # カード生成の確認
                confirm = input("\n❓ この回答からAnkiカードを生成しますか？ (y/n): ").strip().lower()
                
                if confirm in ['y', 'yes', 'はい', 'h']:
                    result = self.process_qa_pair(question, llm_answer, topic)
                    
                    print(f"\n📊 結果:")
                    print(f"   生成されたカード: {result['cards_generated']}枚")
                    print(f"   追加されたカード: {result['cards_added']}枚")
                    if result['cards_failed'] > 0:
                        print(f"   失敗したカード: {result['cards_failed']}枚")
                    
                    # 生成されたカードの概要を表示
                    if result['successful_cards']:
                        print(f"\n📋 追加されたカード:")
                        for i, card_front in enumerate(result['successful_cards'][:3], 1):
                            print(f"   {i}. {card_front[:50]}...")
                        if len(result['successful_cards']) > 3:
                            print(f"   ... 他{len(result['successful_cards'])-3}枚")
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ エラーが発生しました: {e}")
        
        self.show_session_summary()

def create_study_plan(subjects: List[str], session_name: str = "学習計画") -> Dict:
    """体系的な学習計画の作成"""
    
    study_plan = {
        "session_name": session_name,
        "subjects": {},
        "total_questions": 0
    }
    
    for subject in subjects:
        questions = []
        print(f"\n📚 {subject}の学習内容を入力してください")
        print("💡 'done'と入力すると次の科目に進みます")
        
        while True:
            question = input(f"[{subject}] 質問: ").strip()
            if question.lower() == 'done':
                break
            if question:
                questions.append(f"[{subject}] {question}")
        
        study_plan["subjects"][subject] = questions
        study_plan["total_questions"] += len(questions)
    
    return study_plan

def execute_study_plan(study_plan: Dict, deck_name: str = None):
    """学習計画の実行"""
    
    if not deck_name:
        deck_name = study_plan["session_name"]
    
    session = LLMIntegratedSession(deck_name)
    
    print(f"\n🎯 学習計画'{study_plan['session_name']}'を実行します")
    print(f"📊 総質問数: {study_plan['total_questions']}件")
    
    total_cards = 0
    
    for subject, questions in study_plan["subjects"].items():
        print(f"\n📖 {subject} ({len(questions)}件の質問)")
        
        for i, question in enumerate(questions, 1):
            print(f"\n[{i}/{len(questions)}] {question}")
            
            # 実際のLLMを呼び出し
            answer = session.call_llm_api(question)
            print(f"回答: {answer[:100]}...")
            
            # 自動でカード生成
            result = session.process_qa_pair(question, answer, subject)
            total_cards += result['cards_added']
    
    print(f"\n🎉 学習計画完了!")
    print(f"📊 総生成カード数: {total_cards}枚")
    session.show_session_summary()

# 使用例
if __name__ == "__main__":
    print("🚀 LLM統合学習システム")
    
    mode = input("モードを選択してください (1: 対話学習, 2: 学習計画作成): ")
    
    if mode == "1":
        # 対話学習モード
        session = LLMIntegratedSession("AI学習")
        session.smart_learning_session()
        
    elif mode == "2":
        # 学習計画モード
        subjects = input("学習科目をカンマ区切りで入力: ").split(",")
        subjects = [s.strip() for s in subjects if s.strip()]
        
        plan = create_study_plan(subjects)
        
        execute = input("この学習計画を実行しますか？ (y/n): ")
        if execute.lower() in ['y', 'yes']:
            execute_study_plan(plan)
    
    else:
        print("デモモードで実行します")
        session = LLMIntegratedSession("デモ")
        session.smart_learning_session()