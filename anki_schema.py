from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import json

@dataclass
class AnkiCard:
    """Ankiカードのデータ構造"""
    front: str  # 表面（質問）
    back: str   # 裏面（答え）
    deck_name: str = "デフォルト"  # デッキ名
    model_name: str = "基本"      # ノートタイプ
    tags: Optional[List[str]] = None  # タグ

    def to_anki_connect_format(self) -> Dict[str, Any]:
        """AnkiConnect API用のフォーマットに変換"""
        note_data = {
            "deckName": self.deck_name,
            "modelName": self.model_name,
            "fields": {
                "表面": self.front,
                "裏面": self.back
            }
        }
        
        if self.tags:
            note_data["tags"] = self.tags
            
        return {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": note_data
            }
        }

@dataclass
class LearningContent:
    """学習内容からAnkiカードを生成するためのデータ構造"""
    topic: str           # 学習トピック
    question: str        # ユーザーの質問
    answer: str          # LLMの回答
    key_points: List[str] # 重要なポイント

    def extract_cards(self) -> List[AnkiCard]:
        """学習内容からAnkiカードを抽出"""
        cards = []
        
        # メインの質問と回答をカードに
        main_card = AnkiCard(
            front=self.question,
            back=self.answer,
            tags=[self.topic, "LLM学習"]
        )
        cards.append(main_card)
        
        # 重要なポイントを個別のカードに
        for i, point in enumerate(self.key_points):
            if len(point) > 10:  # 短すぎるポイントは除外
                card = AnkiCard(
                    front=f"{self.topic}について: {point.split('。')[0]}とは？",
                    back=point,
                    tags=[self.topic, "重要ポイント"]
                )
                cards.append(card)
        
        return cards