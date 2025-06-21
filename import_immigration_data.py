#!/usr/bin/env python3
"""
移民法英語データをAnkiにインポート
"""

from simple_import import import_to_anki

# 移民法英語データ
immigration_data = """
A person seeking protection from persecution in their home country may apply for (). asylum (政治的亡命)<br>意味: (特に政治的理由による)亡命、庇護。<br>補足: 庇護希望者 (asylum seeker) は、自国に戻ると人種、宗教、国籍、政治的意見などを理由に迫害を受ける恐れがあることを証明する必要がある。Refugee (難民) とは法的な定義や申請プロセスが異なる。 immigration legal humanitarian
The petitioner's application was denied due to a finding of (), as they were deemed likely to become a public charge. inadmissibility (入国不許可)<br>意味: (法的な基準に基づく)入国不適格性、入国不許可事由。<br>補足: 犯罪歴、健康上の問題、経済的な問題 (public charge) など、法律で定められた特定の理由により入国が許可されない状態を指す。これはビザ申請の却下 (rejection) や拒否 (denial) の根本的な理由となる。 immigration legal screening
After maintaining a green card for five years, he was eligible to begin the () process. naturalization (帰化)<br>意味: 帰化。外国人がその国の国籍を取得する法的な手続き。<br>補足: 米国の場合、居住要件、英語能力、米国の歴史・公民に関する知識 (civics test)、そして善良な道徳的性格 (good moral character) が求められる。 citizenship legal process
The attorney filed a motion to () the removal proceedings. terminate (終了させる)<br>意味: (法的な手続きや契約を)終了させる、終結させる。<br>補足: この文脈では「強制送還手続きを終結させるための申し立て」を意味する。一般的な「end」や「finish」よりも、法的な手続きを正式に終わらせるという強いニュアンスを持つ。 immigration legal proceedings
He received a "Request for Evidence" (RFE) asking for more documents to () his claim of extraordinary ability. substantiate (立証する)<br>意味: (主張や申し立てを)証拠をもって立証する、実証する。<br>補足: 「prove」よりもフォーマルで、具体的な証拠によって主張を裏付けることを強調する。ビザ申請において、申請者が提出した情報の信憑性を証明する際によく使われる動詞。 visa application legal evidence
The applicant was granted a () of the inadmissibility finding, allowing him to receive a visa. waiver (免除)<br>意味: (権利・要件などの)放棄、免除。<br>補足: 本来ならば入国不適格 (inadmissible) となる理由があっても、特定の状況下でその適用を免除してもらう特別な許可。非常に限定的な状況でのみ認められる。 immigration legal process
The case was returned to the lower court for further (). adjudication (裁定)<br>意味: (裁判所や行政機関による)法的な判断、裁定、判決。<br>補足: ビザ申請の文脈では、移民局の審査官が申請を審査し、承認または却下を決定する公式なプロセス全体を指す。 immigration legal proceedings
An employer must file a Labor Condition Application (LCA) with the Department of Labor before petitioning for an H-1B (). beneficiary (受益者)<br>意味: (ビザや信託などの)受益者、受取人。<br>補足: 移民法の文脈では、ビザ申請の恩恵を受ける外国人本人を指す。申請を提出する側は「petitioner (申請者)」。例えば、会社がPetitioner、外国人労働者がBeneficiaryとなる。 visa application roles
His previous visa violation ()ed him ineligible for adjustment of status. render (〜の状態にする)<br>意味: (人や物を)ある特定の状態にする、至らせる。<br>補足: 「make」よりもフォーマルで、ある行為が法的な結果として特定の状態を引き起こした、という因果関係を明確に示す際に使われる。「The violation rendered him ineligible. (その違反が彼を不適格にした)」 legal language causality
The court's decision in this case sets a new () for future asylum claims. precedent (判例、先例)<br>意味: 先例、判例。将来の同様の事件を決定する際の基準となる過去の決定。<br>補足: コモンロー (英米法) の国では、過去の裁判所の判断が非常に重要視される。新しい判例は、移民法の解釈や運用に大きな影響を与えることがある。 immigration legal principle
"""

def main():
    print("🚀 移民法英語データをAnkiにインポート開始")
    print("="*50)
    
    # データをインポート
    result = import_to_anki(immigration_data, deck_name="移民英語")
    
    if result.get('success'):
        print(f"\n✅ インポート完了!")
        print(f"📊 結果:")
        print(f"   総カード数: {result['total_cards']}枚")
        print(f"   追加成功: {result['successful']}枚")
        print(f"   追加失敗: {result['failed']}枚")
        
        if result['successful'] > 0:
            print(f"\n🎉 「移民英語」デッキに {result['successful']} 枚のカードが追加されました!")
            print("💡 Ankiを開いて学習を開始してください")
        
        if result['failed'] > 0:
            print(f"\n⚠️  {result['failed']} 枚のカードの追加に失敗しました")
            
    else:
        print(f"❌ インポートに失敗しました: {result.get('error', '不明なエラー')}")
    
    print("\n👋 処理完了")

if __name__ == "__main__":
    main()