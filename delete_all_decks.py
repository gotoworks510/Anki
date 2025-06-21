#!/usr/bin/env python3
"""
すべてのAnkiデッキを削除するスクリプト
"""

from anki_client import AnkiConnectClient

def delete_all_decks():
    """すべてのデッキを削除（デフォルトを除く）"""
    
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
        
        print(f"\n⚠️  {len(deletable_decks)}個のデッキを削除します:")
        for deck in deletable_decks:
            print(f"   - {deck}")
        
        # 確認
        confirm = input("\n❓ 本当にすべてのデッキを削除しますか？ (yes/no): ").strip().lower()
        
        if confirm not in ['yes', 'y']:
            print("❌ 削除をキャンセルしました")
            return False
        
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

def delete_specific_decks(deck_patterns):
    """特定のパターンに一致するデッキのみ削除"""
    
    try:
        client = AnkiConnectClient()
        
        if not client.test_connection():
            print("❌ AnkiConnectに接続できません")
            return False
        
        deck_names = client.get_deck_names()
        
        # パターンに一致するデッキを検索
        matching_decks = []
        for deck in deck_names:
            for pattern in deck_patterns:
                if pattern.lower() in deck.lower():
                    matching_decks.append(deck)
                    break
        
        if not matching_decks:
            print(f"❌ パターン {deck_patterns} に一致するデッキが見つかりません")
            return False
        
        print(f"🎯 以下のデッキを削除します:")
        for deck in matching_decks:
            print(f"   - {deck}")
        
        confirm = input("\n❓ これらのデッキを削除しますか？ (yes/no): ").strip().lower()
        
        if confirm not in ['yes', 'y']:
            print("❌ 削除をキャンセルしました")
            return False
        
        # 削除実行
        for deck_name in matching_decks:
            try:
                result = client._send_request("deleteDecks", {
                    "decks": [deck_name],
                    "cardsToo": True
                })
                
                if result.get("error"):
                    print(f"❌ {deck_name}: {result['error']}")
                else:
                    print(f"✅ {deck_name}: 削除完了")
                    
            except Exception as e:
                print(f"❌ {deck_name}: エラー - {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

if __name__ == "__main__":
    print("🗑️  Ankiデッキ削除ツール")
    print("="*40)
    
    mode = input("削除モードを選択:\n1. すべてのデッキを削除\n2. 特定パターンのデッキを削除\n選択 (1/2): ").strip()
    
    if mode == "1":
        delete_all_decks()
    elif mode == "2":
        patterns = input("削除したいデッキ名のパターンを入力（カンマ区切り）: ").split(",")
        patterns = [p.strip() for p in patterns if p.strip()]
        if patterns:
            delete_specific_decks(patterns)
        else:
            print("❌ 有効なパターンが入力されていません")
    else:
        print("❌ 無効な選択です")
        
    print("\n👋 終了します")