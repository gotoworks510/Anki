#!/usr/bin/env python3
"""
自動的にすべてのデッキを削除するスクリプト
"""

from anki_client import AnkiConnectClient

def auto_delete_all_decks():
    """すべてのデッキを自動削除（デフォルトを除く）"""
    
    try:
        client = AnkiConnectClient()
        
        # 接続確認
        if not client.test_connection():
            print("❌ AnkiConnectに接続できません")
            print("💡 Ankiが起動していることを確認してください")
            return False
        
        print("✅ AnkiConnect接続確認")
        
        # 現在のデッキ一覧を取得
        deck_names = client.get_deck_names()
        print(f"\n📂 現在のデッキ一覧 ({len(deck_names)}個):")
        for i, deck in enumerate(deck_names, 1):
            print(f"   {i}. {deck}")
        
        # デフォルトデッキは削除しない
        deletable_decks = [deck for deck in deck_names if deck != "デフォルト"]
        
        if not deletable_decks:
            print("\n✅ 削除可能なデッキはありません（デフォルトのみ）")
            return True
        
        print(f"\n🗑️  {len(deletable_decks)}個のデッキを削除中...")
        
        # デッキを削除
        deleted_count = 0
        failed_count = 0
        
        for deck_name in deletable_decks:
            try:
                # デッキ削除API呼び出し
                result = client._send_request("deleteDecks", {
                    "decks": [deck_name],
                    "cardsToo": True  # カードも一緒に削除
                })
                
                if result.get("error"):
                    print(f"❌ {deck_name}: 削除失敗 - {result['error']}")
                    failed_count += 1
                else:
                    print(f"✅ {deck_name}: 削除完了")
                    deleted_count += 1
                    
            except Exception as e:
                print(f"❌ {deck_name}: エラー - {e}")
                failed_count += 1
        
        # 結果報告
        print(f"\n📊 削除結果:")
        print(f"   成功: {deleted_count}個")
        print(f"   失敗: {failed_count}個")
        
        # 最終確認
        remaining_decks = client.get_deck_names()
        print(f"\n📂 残っているデッキ ({len(remaining_decks)}個):")
        for deck in remaining_decks:
            print(f"   - {deck}")
        
        return deleted_count > 0
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        return False

if __name__ == "__main__":
    print("🗑️  すべてのAnkiデッキを自動削除")
    print("="*40)
    auto_delete_all_decks()
    print("\n👋 完了")