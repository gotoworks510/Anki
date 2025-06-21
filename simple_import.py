#!/usr/bin/env python3
"""
シンプルなAnkiカードインポート機能
LLMの出力を直接Ankiに登録するための最短パス
"""

from direct_card_importer import DirectCardImporter

def import_to_anki(data: str, deck_name: str = "LLM学習", format_type: str = "auto") -> dict:
    """
    データを直接Ankiにインポートする最短関数
    
    Args:
        data: インポートするデータ（テキストまたはJSON）
        deck_name: Ankiデッキ名
        format_type: "auto", "table", "json"
    
    Returns:
        インポート結果の辞書
    """
    try:
        importer = DirectCardImporter(deck_name)
        result = importer.import_from_text(data, deck_name, format_type)
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}

def quick_import(front_back_pairs: list, deck_name: str = "クイック学習", tags: list = None) -> dict:
    """
    シンプルな(表面, 裏面)ペアのリストからカードを作成
    
    Args:
        front_back_pairs: [(表面1, 裏面1), (表面2, 裏面2), ...]
        deck_name: デッキ名
        tags: 共通タグのリスト
    
    Returns:
        インポート結果
    """
    from anki_schema import AnkiCard
    
    try:
        importer = DirectCardImporter(deck_name)
        cards = []
        
        for front, back in front_back_pairs:
            card = AnkiCard(
                front=str(front),
                back=str(back),
                deck_name=deck_name,
                tags=tags or []
            )
            
            # StructuredCardに変換
            from direct_card_importer import StructuredCard
            structured_card = StructuredCard(
                front=card.front,
                back=card.back,
                tags=card.tags,
                deck_name=card.deck_name
            )
            cards.append(structured_card)
        
        return importer.import_cards(cards)
        
    except Exception as e:
        return {"success": False, "error": str(e)}

def import_llm_output(llm_response: str, deck_name: str = "LLM出力", topic: str = "") -> dict:
    """
    LLMの構造化出力を直接インポート
    
    Args:
        llm_response: LLMからの回答（構造化されたテキスト）
        deck_name: デッキ名
        topic: トピック（タグに追加）
    
    Returns:
        インポート結果
    """
    try:
        # トピックをタグに含める場合の処理
        if topic:
            # 各行にトピックタグを追加する処理をここに実装可能
            pass
        
        return import_to_anki(llm_response, deck_name, "auto")
        
    except Exception as e:
        return {"success": False, "error": str(e)}

# 使用例
if __name__ == "__main__":
    
    # 例1: あなたの移民法データ
    immigration_text = """
A person seeking protection from persecution in their home country may apply for (). asylum (政治的亡命)<br>意味: (特に政治的理由による)亡命、庇護。<br>補足: 庇護希望者 (asylum seeker) は、自国に戻ると人種、宗教、国籍、政治的意見などを理由に迫害を受ける恐れがあることを証明する必要がある。Refugee (難民) とは法的な定義や申請プロセスが異なる。 immigration legal humanitarian
The petitioner's application was denied due to a finding of (), as they were deemed likely to become a public charge. inadmissibility (入国不許可)<br>意味: (法的な基準に基づく)入国不適格性、入国不許可事由。<br>補足: 犯罪歴、健康上の問題、経済的な問題 (public charge) など、法律で定められた特定の理由により入国が許可されない状態を指す。これはビザ申請の却下 (rejection) や拒否 (denial) の根本的な理由となる。 immigration legal screening
"""
    
    print("🎯 移民法データを直接インポート")
    result1 = import_to_anki(immigration_text, "移民法学習")
    print(f"結果: {result1['successful']}/{result1['total_cards']} カード追加成功")
    
    # 例2: シンプルなペアリスト
    word_pairs = [
        ("What does 'asylum' mean?", "Protection granted to someone who has fled their country due to persecution"),
        ("Define 'inadmissibility'", "Legal grounds for denying entry to a country"),
        ("What is 'naturalization'?", "The process by which a foreign citizen becomes a citizen of another country")
    ]
    
    print("\n🎯 単語ペアをクイックインポート")
    result2 = quick_import(word_pairs, "英語学習", ["移民法", "英単語"])
    print(f"結果: {result2['successful']}/{result2['total_cards']} カード追加成功")
    
    # 例3: LLM出力形式
    llm_output = """
表面: Pythonの特徴は？
裏面: シンプルで読みやすい文法、豊富なライブラリ、インタープリター型言語
タグ: Python プログラミング 特徴

表面: 機械学習の定義は？
裏面: コンピューターがデータから自動的にパターンを学習し、予測や判断を行う技術
タグ: 機械学習 AI 定義
"""
    
    print("\n🎯 LLM出力を直接インポート")
    result3 = import_llm_output(llm_output, "AI学習", "機械学習")
    print(f"結果: {result3.get('successful', 0)}/{result3.get('total_cards', 0)} カード追加成功")