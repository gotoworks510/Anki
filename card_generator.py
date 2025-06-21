import re
import json
from typing import List, Dict, Any, Tuple
from anki_schema import AnkiCard, LearningContent

class SmartCardGenerator:
    """LLMの回答から効果的なAnkiカードを生成するクラス"""
    
    def __init__(self):
        self.question_patterns = [
            r"(.+?)とは[？?]?",
            r"(.+?)の特徴は[？?]?",
            r"(.+?)のメリットは[？?]?",
            r"(.+?)のデメリットは[？?]?",
            r"(.+?)の使い方は[？?]?",
            r"(.+?)について説明してください"
        ]
        
    def extract_key_concepts(self, text: str) -> List[str]:
        """テキストから重要な概念を抽出"""
        # 技術用語（英数字混じり）をマッチ
        tech_terms = re.findall(r'[A-Za-z][A-Za-z0-9]*(?:[A-Za-z0-9\-_]*[A-Za-z0-9])*', text)
        
        # 日本語の重要語句（「」で囲まれた部分）
        quoted_terms = re.findall(r'「([^」]+)」', text)
        
        # 箇条書きの項目
        bullet_points = re.findall(r'[・•]\s*([^\n]+)', text)
        
        # 数字付きリストの項目
        numbered_items = re.findall(r'\d+[\.．)\)]\s*([^\n]+)', text)
        
        concepts = []
        concepts.extend([term for term in tech_terms if len(term) > 2])
        concepts.extend(quoted_terms)
        concepts.extend(bullet_points)
        concepts.extend(numbered_items)
        
        # 重複を削除し、長い順にソート
        unique_concepts = list(set(concepts))
        unique_concepts.sort(key=len, reverse=True)
        
        return unique_concepts[:10]  # 最大10個
    
    def generate_definition_cards(self, concepts: List[str], context: str, topic: str) -> List[AnkiCard]:
        """概念の定義カードを生成"""
        cards = []
        
        for concept in concepts:
            # コンテキストから定義を抽出しようと試みる
            definition = self._extract_definition(concept, context)
            
            if definition and len(definition) > 20:
                card = AnkiCard(
                    front=f"{concept}とは何ですか？",
                    back=definition,
                    tags=[topic, "定義", "重要概念"]
                )
                cards.append(card)
        
        return cards
    
    def _extract_definition(self, concept: str, context: str) -> str:
        """コンテキストから概念の定義を抽出"""
        # 概念の前後の文章を探す
        patterns = [
            rf"{re.escape(concept)}とは、([^。]+。)",
            rf"{re.escape(concept)}は、([^。]+。)",
            rf"{re.escape(concept)}：([^。\n]+)",
            rf"{re.escape(concept)}\s*[-－]\s*([^。\n]+)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, context)
            if match:
                return f"{concept}は、{match.group(1)}"
        
        # パターンマッチに失敗した場合、概念を含む文を探す
        sentences = re.split(r'[。．\n]', context)
        for sentence in sentences:
            if concept in sentence and len(sentence) > 20:
                return sentence.strip() + "。"
        
        return ""
    
    def generate_comparison_cards(self, text: str, topic: str) -> List[AnkiCard]:
        """比較・対比のカードを生成"""
        cards = []
        
        # "AとB"のような比較表現を探す
        comparison_patterns = [
            r'([^と\s]+)と([^と\s]+)の違い',
            r'([^と\s]+)と([^と\s]+)を比較',
            r'([^、\s]+)、([^、\s]+)の特徴'
        ]
        
        for pattern in comparison_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                item1, item2 = match
                card = AnkiCard(
                    front=f"{item1}と{item2}の違いは？",
                    back=self._extract_comparison_text(item1, item2, text),
                    tags=[topic, "比較", "対比"]
                )
                if len(card.back) > 20:
                    cards.append(card)
        
        return cards
    
    def _extract_comparison_text(self, item1: str, item2: str, text: str) -> str:
        """比較に関するテキストを抽出"""
        sentences = re.split(r'[。．]', text)
        comparison_text = []
        
        for sentence in sentences:
            if (item1 in sentence or item2 in sentence) and len(sentence) > 15:
                comparison_text.append(sentence.strip())
        
        return "。".join(comparison_text[:3]) + "。"
    
    def generate_process_cards(self, text: str, topic: str) -> List[AnkiCard]:
        """手順・プロセスのカードを生成"""
        cards = []
        
        # 手順を表す表現を探す
        steps = re.findall(r'(\d+)[\.．)\)]\s*([^\n]+)', text)
        
        if len(steps) >= 2:
            # 全体の手順を問うカード
            process_text = "\n".join([f"{step[0]}. {step[1]}" for step in steps])
            card = AnkiCard(
                front=f"{topic}の手順を説明してください",
                back=process_text,
                tags=[topic, "手順", "プロセス"]
            )
            cards.append(card)
            
            # 個別の手順を問うカード
            for i, (num, content) in enumerate(steps):
                if i > 0:  # 最初の手順以外
                    card = AnkiCard(
                        front=f"{topic}の手順{num}は？",
                        back=content,
                        tags=[topic, "手順", f"ステップ{num}"]
                    )
                    cards.append(card)
        
        return cards
    
    def generate_cards_from_llm_response(self, question: str, answer: str, topic: str = "") -> List[AnkiCard]:
        """LLMの質問と回答からAnkiカードを包括的に生成"""
        cards = []
        
        # トピックが指定されていない場合、質問から推定
        if not topic:
            topic = self._infer_topic(question)
        
        # 1. メインの質問回答カード
        main_card = AnkiCard(
            front=question,
            back=answer,
            tags=[topic, "メイン回答"]
        )
        cards.append(main_card)
        
        # 2. 重要概念の定義カード
        concepts = self.extract_key_concepts(answer)
        definition_cards = self.generate_definition_cards(concepts, answer, topic)
        cards.extend(definition_cards)
        
        # 3. 比較・対比カード
        comparison_cards = self.generate_comparison_cards(answer, topic)
        cards.extend(comparison_cards)
        
        # 4. 手順・プロセスカード
        process_cards = self.generate_process_cards(answer, topic)
        cards.extend(process_cards)
        
        # 5. 逆方向カード（回答から質問を推測）
        if len(answer) < 200:  # 短い回答の場合のみ
            reverse_card = AnkiCard(
                front=f"次の内容について質問してください：\n{answer[:100]}...",
                back=question,
                tags=[topic, "逆方向", "質問推測"]
            )
            cards.append(reverse_card)
        
        return cards
    
    def _infer_topic(self, question: str) -> str:
        """質問からトピックを推定"""
        # 技術用語を探す
        tech_terms = re.findall(r'[A-Za-z][A-Za-z0-9]*', question)
        if tech_terms:
            return tech_terms[0]
        
        # 日本語の重要語句
        important_words = re.findall(r'([ァ-ヶー]+|[一-龯]+)', question)
        if important_words:
            return important_words[0]
        
        return "一般"

# 使用例
def test_card_generator():
    """カード生成器のテスト"""
    generator = SmartCardGenerator()
    
    question = "Pythonの特徴について教えてください"
    answer = """
    Pythonは、1991年にGuido van Rossumによって開発されたプログラミング言語です。
    
    主な特徴：
    1. シンプルで読みやすい文法
    2. 豊富なライブラリ
    3. インタープリター型言語
    4. オブジェクト指向プログラミングをサポート
    
    Pythonは「機械学習」や「Web開発」など多くの分野で使用されています。
    JavaやC++と比較して、学習コストが低く、開発速度が速いという特徴があります。
    """
    
    cards = generator.generate_cards_from_llm_response(question, answer, "Python")
    
    print(f"生成されたカード数: {len(cards)}")
    for i, card in enumerate(cards, 1):
        print(f"\n=== カード {i} ===")
        print(f"表面: {card.front}")
        print(f"裏面: {card.back}")
        print(f"タグ: {card.tags}")

if __name__ == "__main__":
    test_card_generator()