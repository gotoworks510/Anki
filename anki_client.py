import json
import urllib.request
import urllib.parse
from typing import List, Dict, Any, Optional
from anki_schema import AnkiCard, LearningContent

class AnkiConnectClient:
    """AnkiConnect APIクライアント"""
    
    def __init__(self, base_url: str = "http://localhost:8765"):
        self.base_url = base_url
        
    def _send_request(self, action: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """AnkiConnect APIにリクエストを送信"""
        data = {
            "action": action,
            "version": 6
        }
        if params:
            data["params"] = params
            
        try:
            json_data = json.dumps(data).encode('utf-8')
            
            req = urllib.request.Request(
                self.base_url,
                data=json_data,
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
            
            if result.get("error"):
                raise Exception(f"AnkiConnect Error: {result['error']}")
                
            return result
        except Exception as e:
            raise Exception(f"Connection Error: {e}")
    
    def test_connection(self) -> bool:
        """AnkiConnect APIの接続をテスト"""
        try:
            result = self._send_request("version")
            return result.get("result") == 6
        except Exception:
            return False
    
    def get_deck_names(self) -> List[str]:
        """利用可能なデッキ名を取得"""
        result = self._send_request("deckNames")
        return result.get("result", [])
    
    def get_model_names(self) -> List[str]:
        """利用可能なノートタイプを取得"""
        result = self._send_request("modelNames")
        return result.get("result", [])
    
    def add_note(self, card: AnkiCard) -> int:
        """単一のカードをAnkiに追加"""
        note_data = card.to_anki_connect_format()
        result = self._send_request("addNote", note_data["params"])
        return result.get("result")  # ノートIDを返す
    
    def add_notes(self, cards: List[AnkiCard]) -> List[int]:
        """複数のカードをAnkiに追加"""
        notes = []
        for card in cards:
            note_format = card.to_anki_connect_format()
            notes.append(note_format["params"]["note"])
        
        result = self._send_request("addNotes", {"notes": notes})
        return result.get("result", [])
    
    def create_deck(self, deck_name: str) -> bool:
        """新しいデッキを作成"""
        try:
            self._send_request("createDeck", {"deck": deck_name})
            return True
        except Exception:
            return False
    
    def add_learning_content(self, content: LearningContent, deck_name: str = "LLM学習") -> List[int]:
        """学習内容からカードを生成してAnkiに追加"""
        # デッキが存在しない場合は作成
        if deck_name not in self.get_deck_names():
            self.create_deck(deck_name)
        
        # カードを生成
        cards = content.extract_cards()
        
        # デッキ名を設定
        for card in cards:
            card.deck_name = deck_name
        
        # Ankiに追加
        return self.add_notes(cards)

# 使用例とテスト関数
def test_anki_client():
    """AnkiClientのテスト"""
    client = AnkiConnectClient()
    
    print("=== AnkiConnect接続テスト ===")
    if not client.test_connection():
        print("❌ AnkiConnectに接続できません")
        return False
    print("✅ AnkiConnect接続成功")
    
    print("\n=== 利用可能なデッキ ===")
    decks = client.get_deck_names()
    for deck in decks:
        print(f"  - {deck}")
    
    print("\n=== 利用可能なノートタイプ ===")
    models = client.get_model_names()
    for model in models:
        print(f"  - {model}")
    
    return True

if __name__ == "__main__":
    test_anki_client()