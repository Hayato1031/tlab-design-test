"""Build the six static design pages. No packages or build server required."""
from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parent.parent
ARROW = '<span class="arrow" aria-hidden="true">↗</span>'
SYLLABUS = 'https://gslbs.keio.jp/syllabus/detail?ttblyr=2026&entno=03720&lang=jp'
CAMPUS = 'https://www.keio.ac.jp/ja/about/campus/sfc/'
MAP = CAMPUS + 'map/'
FACULTY = 'https://www.keio.ac.jp/ja/sfc-pem/faculty/ei/'

# Research descriptions summarize the supplied syllabus. The six headings follow
# the public-facing site structure; they do not describe internal teams.
AREAS = [
 ('cg', 'CG', 'Computer graphics', '3DCG・アニメーション・映像表現', '3D graphics, animation and visual expression', 'コンピュータグラフィックスによる映像表現を扱います。映像を構成する技術や技法を学び、制作を通じて表現の可能性を探ります。', 'We explore visual expression through computer graphics, studying techniques and creating work to investigate new possibilities.'),
 ('drone', 'ドローン', 'Drones / UAV', '機体開発・制御・飛行試験', 'Development, control and flight testing', '信頼性・機動性の高いドローンの開発と応用を研究します。飛行試験、低遅延映像処理、自律飛行などを扱います。', 'We study the development and application of reliable, agile drones, including flight testing, low-latency video processing and autonomous flight.'),
 ('xr', 'VR / AR / XR', 'Extended reality', '体験設計・アプリケーション開発', 'Experiences and application development', 'VRアプリケーションの開発、VRChatなどの教育への応用、ドローンを用いたVRアプリ、WebとVR技術の融合を研究します。', 'We develop VR applications and explore educational uses of platforms such as VRChat, drone-based VR applications, and connections between the web and VR.'),
 ('video', '動画・映像', 'Film / Video', '撮影・編集・モーショングラフィックス', 'Filming, editing and motion graphics', '映像表現を支える技術・技法、新しい技術による表現、映像コンテンツの共同制作に取り組みます。', 'We work on techniques for visual storytelling, expression through new technologies, and collaborative film and video production.'),
 ('media', 'メディア', 'Media art', '光・音響・空間への表現', 'Light, sound and spatial expression', 'プロジェクションマッピング、レーザー光線を用いた表現、音楽と映像の融合など、テクノロジーを用いた表現を実践します。', 'We create technology-based expression through projection mapping, laser light, and combinations of music and moving images.'),
 ('ai', '生成AI', 'Generative AI', '映像制作・新しい問題解決の手法', 'Video production and new approaches to problems', '生成AIを活用した映像制作や、新たな問題解決手法の開発について研究します。', 'We investigate video production using generative AI and the development of new approaches to solving problems.'),
]

def build(variant, lang):
    en = lang == 'en'
    def t(ja, english): return english if en else ja
    def link(url, label, cls='text-link', external=False):
        attrs = ' target="_blank" rel="noopener noreferrer"' if external else ''
        return f'<a class="{cls}" href="{escape(url, quote=True)}"{attrs}>{label}{ARROW}</a>'
    def heading(number, english, japanese, note=''):
        return f'<div class="page-heading"><p>{number} / {english}</p><h2>{t(japanese,english)}</h2>{f"<span>{note}</span>" if note else ""}</div>'
    def placeholder(kind, label):
        return f'<div class="media-slot slot-{kind}"><span class="slot-art" aria-hidden="true"></span><span class="slot-label">{label}</span></div>'

    suffix = '-en' if en else ''
    filename = f'takeda-kinetic-{variant}{suffix}.html'
    nav_items = [('about',t('研究会について','About')),('research-details',t('研究領域','Research')),('outputs',t('成果・活動','Works')),('members',t('メンバー','Members')),('connect',t('交流・参加','Connect')),('access',t('アクセス・お問い合わせ','Access / Contact'))]
    nav = ''.join(f'<a href="#{id}">{label}</a>' for id,label in nav_items)
    languages = '<nav class="language-nav" aria-label="Language">'+''.join(f'<a href="takeda-kinetic-{variant}{s}.html" lang="{l}" hreflang="{l}"'+(' aria-current="page"' if l==lang else '')+f'>{label}</a>' for l,s,label in [('ja','','JP'),('en','-en','EN')])+'</nav>'
    header = f'''<a class="skip" href="#main">{t('本文へ移動','Skip to content')}</a>
<header class="site-header"><div class="shell header-row"><a href="#main" class="brand" aria-label="{t('トップへ','Back to top')}"><div><strong>{t('武田圭史研究室','Takeda Lab.')}</strong><small>Keio University, SFC / {t('Takeda Lab.','Keiji Takeda Laboratory')}</small></div></a><nav class="header-nav" aria-label="{t('メインナビゲーション','Main navigation')}">{nav}</nav><div class="header-tools">{languages}<details class="menu"><summary>{t('メニュー ＋','Menu +')}</summary><nav aria-label="{t('モバイルナビゲーション','Mobile navigation')}">{nav}</nav></details></div></div></header>'''
    hero = ''
    if variant != 'd':
        hero = (ROOT/f'tools/hero-{variant}.html').read_text()
        hero = hero.replace('Film &amp; CG','Film &amp; Video').replace('メディア応用','メディア')
        hero = hero.replace('<span class="word" data-topic="ai"', '<span class="word" data-topic="cg" aria-hidden="true">Computer Graphics</span><span class="word" data-topic="ai"')
        if variant == 'b':
            hero = hero.replace('<img src="assets/concept-kinetic-object.png" data-photo="ai"', '<img src="assets/concept-kinetic-object.png" data-photo="cg" alt=""><img src="assets/concept-kinetic-object.png" data-photo="ai"')
        if en:
            for a,b in [('aria-label="研究領域"','aria-label="Research areas"'),('>メディア<','>Media art<'),('光・音響・空間への表現','Light, sound and spatial expression'),('研究領域をみる','Explore research areas'),('Visual study / イメージ','Visual study / Placeholder'),('研究分野のイメージ / 仮画像','Research imagery / Placeholder')]: hero=hero.replace(a,b)
        hero += f'<nav class="field-links" aria-label="{t("研究領域の詳しい説明へ","Explore each research area")}">'+''.join(link('#research-'+a[0],t(a[1],a[2]),'') for a in AREAS)+'</nav></section>'
    about = f'''<section class="lab-intro" id="about" aria-labelledby="intro-title"><div class="intro-summary"><h2 id="intro-title">{t('研究会について','About the lab')}<small>{t('About Takeda Lab.','Keio University, SFC')}</small></h2><p>{t('CG・映像・光・音響を用いたメディア表現を研究しています。生成AI・ドローン・VR/AR/XRの実践的な応用にも取り組んでいます。','We explore expression through computer graphics, film, light and sound, alongside practical applications of generative AI, drones and VR/AR/XR.')}</p></div><div class="audience-shortcuts">{link('#collaboration',t('共同研究・交流をお考えの方','For collaboration & exchange'))}{link('#join',t('参加を検討している学生の方','For prospective students'))}</div>
<details class="about-more" id="practice"><summary>{t('活動方針・制作環境をみる','Our approach & working environment')}<span class="plus" aria-hidden="true">＋</span></summary><div class="about-more-content"><div class="process-grid">'''
    for n,ja,eng,jp,ep in [(1,'調査・サーベイ','Explore','関連研究や事例を調べ、研究の背景や課題を整理します。','Review related research and examples to understand the background and open questions.'),(2,'制作・実験','Make & test','個人の研究テーマとグループ活動を通じて、制作・開発・実験に取り組みます。','Develop individual research themes through production, development, experiments and group activities.'),(3,'発表・共有','Present & share','中間・最終発表で進捗や成果を共有し、取り組みを深めます。','Share progress and outcomes through interim and final presentations.')]:
        about += f'<article class="process-item"><span class="process-number">0{n}</span><h3>{t(ja,eng)}</h3><p>{t(jp,ep)}</p></article>'
    about += f'''</div><div class="environment-slot">{placeholder('environment',t('設備・制作環境の写真を配置','Space for a photograph of the working environment'))}<div><h3>{t('設備・制作環境','Working environment')}</h3><p>{t('制作・実験に使用する設備や活動風景を紹介する欄です。写真・設備情報は掲載準備中です。','This section will introduce the equipment and spaces used for production and experiments. Photographs and details are being prepared.')}</p>{link(SYLLABUS,t('活動内容をシラバスで確認','Read the course syllabus'),external=True)}</div></div></div></details></section>'''

    if variant == 'd':
        about = about.replace('<h2 id="intro-title">', '<h1 id="intro-title">').replace('</small></h2>', '</small></h1>')

    research = '<section class="page-section research-section" id="research-details">'+heading('01','Research areas','研究領域')+'<div class="research-list">'
    for n,a in enumerate(AREAS,1):
        id,ja,english,summary,esummary,body,ebody=a
        thumb = ''
        if variant == 'd':
            image = {'cg':'concept-kinetic-object.png','drone':'concept-drone.jpg','xr':'concept-xr.jpg','video':'concept-film.jpg','media':'concept-media.jpg','ai':'concept-kinetic-object.png'}[id]
            thumb = f'<span class="research-thumb thumb-{id}" aria-hidden="true"><img src="assets/{image}" width="96" height="96" alt=""></span>'
        research+=f'''<details class="research-detail" id="research-{id}"><summary><span class="area-number">0{n}</span>{thumb}<div class="area-name"><h3>{t(ja,english)}</h3><small>{t(english,ja if ja=='CG' else '')}</small></div><p class="area-summary">{t(summary,esummary)}</p><span class="plus" aria-hidden="true">＋</span></summary><div class="detail-copy"><p>{t(body,ebody)}</p><div class="detail-links">{link('#outputs',t('関連する成果・活動','Works & activities'))}{link('#collaboration',t('この領域について相談する','Discuss this research area'))}</div></div></details>'''
    research += '</div></section>'

    works = '<section class="page-section works-section" id="outputs">'+heading('02','Works & activities','研究成果・活動報告',t('プロジェクト・制作物から、展示・発表、日々の研究活動まで。','Projects and creative work, exhibitions and presentations, and research in progress.'))+'<div class="works-grid">'
    for kind,eng,jp,label,jbody,ebody in [('project','Projects','プロジェクト・制作物','作品写真・映像を配置','作品の概要、関連する研究領域、制作物や公開リンクを掲載します。','Space for a project summary, related research areas, outputs and public links.'),('exhibition','Exhibitions','展示・発表','展示・発表の写真を配置','展示や研究発表の内容、開催情報、発表資料を掲載します。','Space for exhibition and presentation reports, event details and presentation materials.'),('report','Lab notes','活動報告','研究活動の写真を配置','制作や実験の過程、イベントなど、研究会の活動を掲載します。','Space for reports on production, experiments, events and other lab activities.')]:
        works+=f'<article class="work-card">{placeholder(kind,t(label,"Image / video placeholder"))}<div class="work-meta"><span>{eng}</span><span>{t("掲載準備中","Coming soon")}</span></div><h3>{t(jp,eng)}</h3><p>{t(jbody,ebody)}</p></article>'
    works+='</div></section>'

    members='<section class="page-section members-section" id="members">'+heading('03','Members','メンバー',t('教員と、研究・制作に取り組む学生。','The faculty and students behind the research.'))+'<div class="members-grid">'
    members+=f'''<article class="member-card faculty-card">{placeholder('portrait',t('教員の写真を配置','Faculty portrait placeholder'))}<p class="member-role">{t('担当教員','Faculty')}</p><h3>{t('武田 圭史','Keiji Takeda')}</h3><p class="member-english">{t('Keiji Takeda','Takeda Lab.')}</p><p class="member-description">{t('慶應義塾大学 環境情報学部','Faculty of Environment and Information Studies, Keio University')}</p>{link(FACULTY,t('大学の教員紹介','University faculty directory'),external=True)}</article>'''
    for n in range(1,4):
        members+=f'''<article class="member-card student-card">{placeholder('portrait',t('学生の写真を配置','Student portrait placeholder'))}<p class="member-role">{t('学生 / プロフィール掲載枠','Student / Profile placeholder')} {n:02}</p><h3>{t('メンバー名','Member name')}</h3><p class="member-english">{t('学年・所属','Year / Affiliation')}</p><p class="member-description">{t('研究テーマ・専門分野を掲載','Research topic and interests')}</p></article>'''
    members+=f'</div><p class="section-note">{t("学生の氏名・写真・プロフィールは掲載準備中です。上のカードはレイアウト確認用の掲載枠です。","Student names, photographs and profiles are being prepared. The cards above are layout placeholders.")}</p></section>'

    connect='<section class="page-section connect-section" id="connect">'+heading('04','Connect with us','交流・参加のご案内')+'<div class="connect-grid">'
    connect+=f'''<article class="connect-card" id="collaboration"><p class="eyebrow">Collaboration &amp; exchange</p><h3>{t('共同研究・交流を<br>お考えの方へ','For collaboration<br>&amp; exchange')}</h3><p>{t('共同研究、技術や表現に関する意見交換、展示・取材など、研究会との交流に関するご相談はこちらへ。','For inquiries about collaborative research, exchanges on technology and creative practice, exhibitions, or media coverage.')}</p><ol class="connect-steps"><li>{link('#research-details',t('関連する研究領域を知る','Explore relevant research areas'))}</li><li>{link('#outputs',t('研究成果・活動をみる','Browse works & activities'))}</li><li><span>{t('相談内容と所属を添えてご連絡ください。','Contact us with your affiliation and a brief description of your inquiry.')}</span></li></ol>{link('mailto:keiji@sfc.keio.ac.jp?subject='+t('共同研究・交流について','Collaboration and exchange inquiry'),t('共同研究・交流について相談する','Contact us about collaboration'),'outline-link')}</article>'''
    connect+=f'''<article class="connect-card student-connect" id="join"><p class="eyebrow">For prospective students</p><h3>{t('研究会への参加を<br>検討している方へ','For students interested<br>in joining the lab')}</h3><p>{t('関心のある研究テーマを見つけ、研究会の活動内容を確認したうえで、参加・履修についてご相談ください。','Explore the research areas and how the lab works, then contact the faculty to discuss participation and enrollment.')}</p><ol class="connect-steps"><li>{link('#practice',t('研究会の活動の進め方を知る','Read about how the lab works'))}</li><li>{link(SYLLABUS,t('シラバスで活動内容を確認する','Review the course syllabus'),external=True)}</li><li><span>{t('所属・学年と、興味のあるテーマを添えてご連絡ください。','Contact us with your affiliation, year of study and research interests.')}</span></li></ol>{link('mailto:keiji@sfc.keio.ac.jp?subject='+t('研究会への参加・履修について','Participation and enrollment inquiry'),t('参加・履修について相談する','Ask about joining the lab'),'outline-link')}<p class="section-note">{t('最新の履修条件・募集時期は担当教員へご確認ください。','Please ask the faculty about current enrollment requirements and application periods.')}</p></article></div></section>'''

    access = '<section class="page-section access-section" id="access">'+heading('05','Access & contact','アクセス・お問い合わせ')
    access+=f'''<div class="campus-layout"><figure class="campus-photo"><img src="assets/takeda-campus.jpg" width="1800" height="989" loading="lazy" alt="{t('慶應義塾大学湘南藤沢キャンパス','Keio University Shonan Fujisawa Campus')}"><figcaption>Keio University / Shonan Fujisawa Campus</figcaption></figure><div class="access-copy"><p class="eyebrow">Shonan Fujisawa Campus</p><h3>{t('慶應義塾大学<br>湘南藤沢キャンパス','Keio University<br>Shonan Fujisawa Campus')}</h3><address>{t('〒252-0882<br>神奈川県藤沢市遠藤5322','5322 Endo, Fujisawa, Kanagawa<br>252-0882, Japan')}</address><p>{t('湘南台駅西口、または辻堂駅北口より<br>「慶応大学」行きバスをご利用ください。','Take a bus bound for Keio University from the west exit of Shonandai Station or the north exit of Tsujido Station.')}</p><div class="access-links">{link(CAMPUS,t('交通アクセス（大学公式）','Directions (Keio University)'),external=True)}{link(MAP,t('キャンパスマップ','Campus map'),external=True)}</div><p class="section-note">{t('研究室への訪問は、事前にメールでご相談ください。','Please contact us by email before visiting the lab.')}</p></div></div><div class="contact-block" id="contact"><div><p class="eyebrow">Get in touch</p><h3>{t('お問い合わせ','Contact')}</h3><p>{t('共同研究・交流・取材、研究会への参加・履修のご相談。','For collaboration, exchange, media inquiries, and student participation.')}</p></div><div>{link('mailto:keiji@sfc.keio.ac.jp','keiji@sfc.keio.ac.jp','contact-email')}<p class="section-note">{t('武田圭史 / 2026年度春学期シラバス記載の連絡先','Keiji Takeda / Contact listed in the Spring 2026 syllabus')}</p></div></div></section>'''

    footer=f'''<footer class="page-footer"><div class="shell"><div class="footer-top"><a href="#main" class="footer-brand">Takeda Lab<span>.</span></a>{link('#main',t('ページ上部へ','Back to top'))}</div><nav class="footer-site-nav" aria-label="{t('フッターナビゲーション','Footer navigation')}">{nav}</nav><div class="footer-links"><span>{t('慶應義塾大学 SFC / 武田圭史研究室','Keio University, SFC / Keiji Takeda Laboratory')}</span><nav aria-label="{t('デザイン案の切り替え','Compare designs')}"><a href="index.html">{t('4案を比較','Compare designs')}</a>'''
    footer+=''.join(f'<a href="takeda-kinetic-{v}{suffix}.html"'+(' aria-current="page"' if v==variant else '')+f'>{v.upper()}</a>' for v in 'abcd')
    footer+=f'''</nav></div><p class="prototype-note">{t('デザイン検討用プロトタイプ。研究内容は','Design prototype. Research descriptions summarize the ')}<a href="{escape(SYLLABUS,quote=True)}" target="_blank" rel="noopener noreferrer">{t('2026年度春学期「研究会Ａ」シラバス','Spring 2026 Research Seminar A syllabus')}</a>{t('をもとにしています。生成画像・アートは仮イメージ。成果・学生プロフィールの掲載枠は実在の実績・人物を示すものではありません。','. Generated visuals are illustrative. Work and student profile placeholders do not represent actual projects or people.')}</p></div></footer>'''
    layout={'a':'object','b':'photo','c':'field','d':'index'}[variant]
    title={'a':'Sculptural art','b':'Photography','c':'Generative field','d':'Research index'}[variant]
    out=f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><meta name="description" content="{t('武田圭史研究室の研究領域・研究成果・メンバー・交流と参加のご案内。デザイン検討用プロトタイプ。','Explore Takeda Lab research, work, members, collaboration and student participation. Design prototype.')}"><title>{variant.upper()} | {title} | Takeda Lab.</title><link rel="alternate" hreflang="ja" href="takeda-kinetic-{variant}.html"><link rel="alternate" hreflang="en" href="takeda-kinetic-{variant}-en.html"><link rel="stylesheet" href="takeda-visual.css"><link rel="stylesheet" href="takeda-kinetic.css"><link rel="stylesheet" href="takeda-page.css"><script src="takeda-kinetic.js" defer></script></head><body data-layout="{layout}">
{header}<main class="shell" id="main">{hero}{about}<div class="page-body">{research}{works}{members}{connect}{access}</div></main>{footer}</body></html>'''
    (ROOT/filename).write_text(out)

if __name__ == '__main__':
    for variant in 'abcd':
        for lang in ['ja','en']: build(variant,lang)
    print('Built 4 designs in Japanese and English.')
