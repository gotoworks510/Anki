"""
構造化データからAnkiカードを直接インポートするモジュール
LLMの出力や既存のデータを直接Ankiに登録
"""

import json
import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from anki_client import AnkiConnectClient

@dataclass
class StructuredCard:
    """構造化されたカードデータ"""
    front: str
    back: str
    tags: List[str]
    deck_name: str = "構造化学習"
    
    def to_anki_format(self) -> Dict[str, Any]:
        """AnkiConnect形式に変換"""
        return {
            "deckName": self.deck_name,
            "modelName": "基本",
            "fields": {
                "表面": self.front,
                "裏面": self.back
            },
            "tags": self.tags
        }

class DirectCardImporter:
    """構造化データを直接Ankiにインポートするクラス"""
    
    def __init__(self, default_deck: str = "構造化学習"):
        self.anki_client = AnkiConnectClient()
        self.default_deck = default_deck
        
        # 接続確認
        if not self.anki_client.test_connection():
            raise Exception("AnkiConnectに接続できません")
        
        # デッキ作成
        if default_deck not in self.anki_client.get_deck_names():
            self.anki_client.create_deck(default_deck)
    
    def parse_table_format(self, table_text: str, deck_name: str = None) -> List[StructuredCard]:
        """
        表形式のテキストからカードデータを解析
        形式: "表面 裏面 タグ" (タブ区切り、空白区切り、またはパイプ区切り)
        """
        cards = []
        lines = table_text.strip().split('\n')
        
        # ヘッダー行をスキップ
        data_lines = [line for line in lines if line.strip() and not self._is_header_line(line)]
        
        for line in data_lines:
            try:
                # 区切り文字を自動判定
                if '\t' in line:
                    parts = line.split('\t')
                elif '|' in line:
                    parts = [p.strip() for p in line.split('|') if p.strip()]
                else:
                    # 複雑な分割: 最初の()までが表面、最後の単語群がタグ、中間が裏面
                    parts = self._smart_split_line(line)
                
                if len(parts) >= 3:
                    front = parts[0].strip()
                    back = parts[1].strip()
                    tags_text = parts[2].strip()
                    
                    # タグを分割
                    tags = [tag.strip() for tag in re.split(r'[,\s]+', tags_text) if tag.strip()]
                    
                    card = StructuredCard(
                        front=front,
                        back=back,
                        tags=tags,
                        deck_name=deck_name or self.default_deck
                    )
                    cards.append(card)
                    
            except Exception as e:
                print(f"⚠️  行の解析に失敗: {line[:50]}... - {e}")
                continue
        
        return cards
    
    def _is_header_line(self, line: str) -> bool:
        """ヘッダー行かどうかを判定"""
        header_indicators = ['表面', '裏面', 'タグ', 'front', 'back', 'tags', '---', '===']
        line_lower = line.lower().strip()
        return any(indicator in line_lower for indicator in header_indicators)
    
    def _smart_split_line(self, line: str) -> List[str]:
        """
        複雑な行を賢く分割
        例: "A person seeking protection... (). asylum (政治的亡命)<br>意味: ... immigration legal humanitarian"
        """
        # パターン1: () で終わる部分を表面として抽出
        front_match = re.match(r'^(.+?\(\)\s*\.?)', line)
        if front_match:
            front = front_match.group(1).strip()
            remaining = line[len(front):].strip()
            
            # 最後の単語群（タグ）を抽出
            words = remaining.split()
            if len(words) >= 3:
                # 最後の2-4語をタグとして扱う
                tags_start = -3
                for i in range(-1, -min(5, len(words)+1), -1):
                    if any(char in words[i] for char in ['<', '>', '(', ')', '意味', '補足']):
                        tags_start = i + 1
                        break
                
                if tags_start < 0:
                    tags = ' '.join(words[tags_start:])
                    back = ' '.join(words[:tags_start])
                else:
                    tags = ' '.join(words[-3:])  # デフォルトで最後の3語
                    back = ' '.join(words[:-3])
                
                return [front, back, tags]
        
        # フォールバック: 空白で分割して最初と最後を使用
        words = line.split()
        if len(words) >= 3:
            return [words[0], ' '.join(words[1:-1]), words[-1]]
        
        return [line, "", ""]
    
    def parse_json_format(self, json_data: str, deck_name: str = None) -> List[StructuredCard]:
        """JSON形式からカードデータを解析"""
        try:
            data = json.loads(json_data) if isinstance(json_data, str) else json_data
            cards = []
            
            # リスト形式の場合
            if isinstance(data, list):
                for item in data:
                    card = self._create_card_from_dict(item, deck_name)
                    if card:
                        cards.append(card)
            
            # 辞書形式の場合
            elif isinstance(data, dict):
                if 'cards' in data:
                    for item in data['cards']:
                        card = self._create_card_from_dict(item, deck_name)
                        if card:
                            cards.append(card)
                else:
                    card = self._create_card_from_dict(data, deck_name)
                    if card:
                        cards.append(card)
            
            return cards
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON解析エラー: {e}")
            return []
    
    def _create_card_from_dict(self, item: Dict, deck_name: str = None) -> Optional[StructuredCard]:
        """辞書からStructuredCardを作成"""
        try:
            # 様々なキー名に対応
            front_keys = ['front', 'question', 'q', '表面', '質問']
            back_keys = ['back', 'answer', 'a', '裏面', '回答', '答え']
            tags_keys = ['tags', 'tag', 'categories', 'タグ']
            
            front = None
            back = None
            tags = []
            
            # 表面を探す
            for key in front_keys:
                if key in item:
                    front = str(item[key])
                    break
            
            # 裏面を探す
            for key in back_keys:
                if key in item:
                    back = str(item[key])
                    break
            
            # タグを探す
            for key in tags_keys:
                if key in item:
                    tags_value = item[key]
                    if isinstance(tags_value, list):
                        tags = [str(tag) for tag in tags_value]
                    elif isinstance(tags_value, str):
                        tags = [tag.strip() for tag in tags_value.split(',')]
                    break
            
            if front and back:
                return StructuredCard(
                    front=front,
                    back=back,
                    tags=tags,
                    deck_name=deck_name or self.default_deck
                )
            
        except Exception as e:
            print(f"⚠️  カード作成エラー: {e}")
        
        return None
    
    def import_cards(self, cards: List[StructuredCard]) -> Dict[str, Any]:
        """カードをAnkiにインポート"""
        if not cards:
            return {"success": False, "message": "インポートするカードがありません"}
        
        # デッキを作成（必要に応じて）
        deck_names = set(card.deck_name for card in cards)
        existing_decks = self.anki_client.get_deck_names()
        
        for deck_name in deck_names:
            if deck_name not in existing_decks:
                self.anki_client.create_deck(deck_name)
                print(f"📂 デッキ '{deck_name}' を作成しました")
        
        # カードを追加
        successful_cards = []
        failed_cards = []
        
        for card in cards:
            try:
                note_data = {
                    "deckName": card.deck_name,
                    "modelName": "基本",
                    "fields": {
                        "表面": card.front,
                        "裏面": card.back
                    },
                    "tags": card.tags
                }
                
                note_id = self.anki_client._send_request("addNote", {"note": note_data})
                
                if note_id.get("result"):
                    successful_cards.append(card)
                    print(f"✅ カード追加: {card.front[:50]}...")
                else:
                    failed_cards.append(card)
                    error = note_id.get("error", "不明なエラー")
                    print(f"❌ カード追加失敗: {card.front[:50]}... - {error}")
                
            except Exception as e:
                failed_cards.append(card)
                print(f"❌ エラー: {card.front[:50]}... - {e}")
        
        return {
            "success": True,
            "total_cards": len(cards),
            "successful": len(successful_cards),
            "failed": len(failed_cards),
            "successful_cards": successful_cards,
            "failed_cards": failed_cards
        }
    
    def import_from_text(self, text_data: str, deck_name: str = None, format_type: str = "auto") -> Dict[str, Any]:
        """テキストデータから直接インポート"""
        
        if format_type == "auto":
            # 形式を自動判定
            if text_data.strip().startswith('{') or text_data.strip().startswith('['):
                format_type = "json"
            else:
                format_type = "table"
        
        if format_type == "json":
            cards = self.parse_json_format(text_data, deck_name)
        else:  # table
            cards = self.parse_table_format(text_data, deck_name)
        
        print(f"📊 解析結果: {len(cards)}枚のカードを検出")
        
        if cards:
            return self.import_cards(cards)
        else:
            return {"success": False, "message": "有効なカードデータが見つかりませんでした"}

# 使用例とテスト関数
def test_immigration_data():
    """提供された移民法データのテスト"""
    
    # あなたが提供したデータ
    immigration_data = """
A person seeking protection from persecution in their home country may apply for (). asylum (政治的亡命)<br>意味: (特に政治的理由による)亡命、庇護。<br>補足: 庇護希望者 (asylum seeker) は、自国に戻ると人種、宗教、国籍、政治的意見などを理由に迫害を受ける恐れがあることを証明する必要がある。Refugee (難民) とは法的な定義や申請プロセスが異なる。 immigration legal humanitarian
The petitioner's application was denied due to a finding of (), as they were deemed likely to become a public charge. inadmissibility (入国不許可)<br>意味: (法的な基準に基づく)入国不適格性、入国不許可事由。<br>補足: 犯罪歴、健康上の問題、経済的な問題 (public charge) など、法律で定められた特定の理由により入国が許可されない状態を指す。これはビザ申請の却下 (rejection) や拒否 (denial) の根本的な理由となる。 immigration legal screening
After maintaining a green card for five years, he was eligible to begin the () process. naturalization (帰化)<br>意味: 帰化。外国人がその国の国籍を取得する法的な手続き。<br>補足: 米国の場合、居住要件、英語能力、米国の歴史・公民に関する知識 (civics test)、そして善良な道徳的性格 (good moral character) が求められる。 citizenship legal process
The attorney filed a motion to () the removal proceedings. terminate (終了させる)<br>意味: (法的な手続きや契約を)終了させる、終結させる。<br>補足: この文脈では「強制送還手続きを終結させるための申し立て」を意味する。一般的な「end」や「finish」よりも、法的な手続きを正式に終わらせるという強いニュアンスを持つ。 immigration legal proceedings
He received a "Request for Evidence" (RFE) asking for more documents to () his claim of extraordinary ability. substantiate (立証する)<br>意味: (主張や申し立てを)証拠をもって立証する、実証する。<br>補足: 「prove」よりもフォーマルで、具体的な証拠によって主張を裏付けることを強調する。ビザ申請において、申請者が提出した情報の信憑性を証明する際によく使われる動詞。 visa application legal evidence
"""
    
    print("🧪 移民法データのインポートテスト")
    
    importer = DirectCardImporter("移民法学習")
    result = importer.import_from_text(immigration_data, deck_name="移民法学習")
    
    print(f"\n📊 インポート結果:")
    print(f"   総カード数: {result.get('total_cards', 0)}")
    print(f"   成功: {result.get('successful', 0)}")
    print(f"   失敗: {result.get('failed', 0)}")
    
    return result

def demo_json_import():
    """JSON形式のデモ"""
    
    json_data = [
        {
            "front": "Pythonの特徴は？",
            "back": "シンプルで読みやすい文法、豊富なライブラリ、インタープリター型言語",
            "tags": ["Python", "プログラミング", "特徴"]
        },
        {
            "question": "機械学習とは？",
            "answer": "コンピューターがデータから自動的にパターンを学習する技術",
            "tags": ["機械学習", "AI", "定義"]
        }
    ]
    
    print("🧪 JSON形式インポートテスト")
    
    importer = DirectCardImporter("プログラミング学習")
    result = importer.import_cards(importer.parse_json_format(json_data))
    
    print(f"\n📊 JSON インポート結果:")
    print(f"   総カード数: {result.get('total_cards', 0)}")
    print(f"   成功: {result.get('successful', 0)}")
    
    return result

if __name__ == "__main__":
    print("🚀 構造化データインポーター")
    
    # 移民法データのテスト
    test_immigration_data()
    
    print("\n" + "="*50)
    
    # JSONデータのテスト
    demo_json_import()