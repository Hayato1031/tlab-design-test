"""Build H, I and J independently; retain G's lower-page information and interactions."""
from pathlib import Path
import re
from build_pages import AREAS
ROOT=Path(__file__).resolve().parent.parent

def build(v,lang):
 en=lang=='en'
 def t(j,e):return e if en else j
 def a(h,label,cls=''):return f'<a class="{cls}" href="{h}">{label}<span aria-hidden="true">↗</span></a>'
 suffix='-en' if en else ''
 source=(ROOT/f'takeda-kinetic-g{suffix}.html').read_text()
 source=source.replace('takeda-kinetic-g',f'takeda-kinetic-{v}').replace('G | Research list',f'{v.upper()} | '+({'h':'Kinetic studio','i':'Research atlas','j':'Campus editorial'}[v]))
 source=source.replace('data-variant="g"','data-variant="g" data-portal="'+v+'"')
 source=source.replace('</head>','<link rel="stylesheet" href="takeda-portals.css?v=2"></head>')
 if v=='h':
  source=source.replace('</head>','<link rel="stylesheet" href="takeda-h-studio.css?v=3"></head>')
 if v=='h':
  source=source.replace('</head>','<script src="takeda-studio-motion.js?v=1" defer></script>')
 if v=='j':
  source=source.replace('</head>','<link rel="stylesheet" href="takeda-j-editorial.css?v=1"></head>')
 header=f'''<a class="skip" href="#main">{t('本文へ移動','Skip to content')}</a><header class="portal-header"><div class="portal-header-inner"><a class="portal-brand" href="#main"><span class="brand-mark" aria-hidden="true">t<span>l</span></span><span><strong>Takeda Lab.</strong><small>{t('慶應義塾大学 湘南藤沢キャンパス','Keio University, SFC')}</small></span></a><nav class="portal-header-nav" aria-label="{t('メインナビゲーション','Main navigation')}">{a('#research-details',t('研究領域','Research'))}{a('#outputs',t('成果・活動','Journal'))}{a('#members',t('メンバー','Members'))}{a('#access',t('アクセス','Access'))}</nav><div class="portal-tools"><nav class="language-nav" aria-label="Language"><a href="takeda-kinetic-{v}.html" lang="ja" {'aria-current="page"' if not en else ''}>JP</a><a href="takeda-kinetic-{v}-en.html" lang="en" {'aria-current="page"' if en else ''}>EN</a></nav>{a('#contact',t('お問い合わせ','Contact'),'portal-contact')}</div></div></header>'''
 source=re.sub(r'<a class="skip".*?</header>',lambda _:header,source, count=1,flags=re.S)
 intro=f'''<div class="gateway-copy"><p class="portal-kicker">KEIO UNIVERSITY / SFC</p><h1>{t('武田圭史研究室','Keiji Takeda Laboratory')}</h1><p class="gateway-description">{t('CG・映像・光・音響によるメディア表現と、<br class="desktop-break">生成AI・ドローン・XRの実践的な応用を研究しています。','We explore media expression through CG, film, light and sound, and practical applications of generative AI, drones and XR.')}</p></div>'''
 fields=''
 for n,(key,jp,eng,short,eshort,*_) in enumerate(AREAS,1):
  fields+=a('#research-'+key,f'<span class="field-index">0{n}</span><span class="field-label">{t(jp,eng)}<small>{t(short,eshort)}</small></span>','gateway-field')
 fieldnav=f'<nav class="gateway-fields" aria-label="{t("6つの研究領域","Six research areas")}">{fields}</nav>'
 actions=f'''<nav class="gateway-actions" aria-label="{t('目的別のご案内','Start here')}">{a('#collaboration',f'<span><small>COLLABORATION</small><strong>{t("共同研究・交流をお考えの方","Collaboration & exchange")}</strong><em>{t("研究相談・展示・取材について","Research inquiries, exhibitions & media")}</em></span>','gateway-action collaboration-action')}{a('#join',f'<span><small>JOIN THE LAB</small><strong>{t("研究会への参加を考えている方","Interested in joining the lab?")}</strong><em>{t("研究テーマ・履修・参加のご案内","Research interests, enrollment & participation")}</em></span>','gateway-action join-action')}</nav>'''
 quick=f'''<nav class="gateway-quick" aria-label="{t('研究会の情報','Lab information')}">{a('#outputs',f'<span><small>JOURNAL</small><strong>{t("研究成果・活動報告","Works & activities")}</strong></span>')}{a('#members',f'<span><small>PEOPLE</small><strong>{t("武田先生・メンバー","Faculty & members")}</strong></span>')}{a('#access',f'<span><small>VISIT / CONTACT</small><strong>{t("アクセス・お問い合わせ","Access & contact")}</strong></span>')}</nav>'''
 if v=='h':
  themes=['Computer<br>Graphics','Drones','Extended<br>Reality','Film &amp;<br>Video','Media Art','Generative<br>AI']
  words=''.join(f'<span class="studio-word {"is-active" if n==0 else ""}" data-studio-word aria-hidden="true">{word}</span>' for n,word in enumerate(themes))
  media=f'''<figure class="studio-visual" aria-label="{t('6つの研究領域を表す動く立体アート。仮ビジュアル。','Animated sculpture with six research themes. Placeholder visual.')}"><div class="studio-disc" aria-hidden="true"></div><div class="studio-orbit orbit-one" aria-hidden="true"></div><div class="studio-orbit orbit-two" aria-hidden="true"></div><div class="studio-words" aria-hidden="true">{words}<span class="studio-for">For Takeda Lab.</span></div><img class="studio-object" src="assets/concept-kinetic-object.png" width="1280" height="1280" alt=""><span class="studio-cross" aria-hidden="true">＋</span><figcaption><span>RESEARCH IN MOTION <b data-studio-count>01 / 06</b></span><span>{t('研究領域のイメージ','Research imagery')}</span></figcaption></figure>'''
  top=f'<section class="gateway gateway-h" id="about"><div class="gateway-main"><div class="gateway-information">{intro}<p class="fields-heading">{t("研究領域","RESEARCH AREAS")}<span>06 FIELDS</span></p>{fieldnav}</div>{media}</div>{actions}{quick}</section>'
 elif v=='j':
  media=f'''<figure class="campus-composition"><span class="campus-outline" aria-hidden="true">SFC</span><div class="campus-image-mask"><img src="assets/takeda-campus.jpg" width="1800" height="989" alt="{t('慶應義塾大学湘南藤沢キャンパス','Keio University Shonan Fujisawa Campus')}"><span class="campus-image-shade" aria-hidden="true"></span><span class="campus-image-type" aria-hidden="true">Takeda<br><i>Lab.</i></span></div><span class="campus-side-note" aria-hidden="true">KEIO UNIVERSITY — SHONAN FUJISAWA</span><figcaption><span class="campus-location-mark" aria-hidden="true">↗</span><span>{t('慶應義塾大学 湘南藤沢キャンパス','Keio University, Shonan Fujisawa Campus')}<small>{t('研究と制作の場','A place for research and creation')}</small></span></figcaption></figure>'''
  top=f'<section class="gateway gateway-j" id="about"><div class="gateway-main"><div class="gateway-information">{intro}<p class="fields-heading">{t("研究領域","RESEARCH AREAS")}<span>06 FIELDS</span></p>{fieldnav}</div>{media}</div>{actions}{quick}</section>'
 else:
  art=f'''<div class="atlas-art" aria-hidden="true"><svg viewBox="0 0 480 200" fill="none"><g stroke="currentColor" stroke-width=".65">{''.join(f'<ellipse cx="240" cy="100" rx="{45+i*7}" ry="{18+i*3}" transform="rotate({i*9} 240 100)"/>' for i in range(24))}</g><circle cx="240" cy="100" r="5" fill="currentColor"/></svg><span>FORM / CODE / EXPRESSION</span></div>'''
  top=f'<section class="gateway gateway-i" id="about"><div class="atlas-intro">{intro}{art}</div><div class="atlas-board"><div class="atlas-research"><div class="fields-heading">{t("研究領域から探す","Explore research")}<span>01 — 06</span></div>{fieldnav}</div>{actions}</div>{quick}</section>'
 source=re.sub(r'<section class="lab-intro editorial-intro".*?<div class="page-body">',lambda _:top+'<div class="page-body">',source,count=1,flags=re.S)
 # A new concept switcher appears only on the new pages; A–G remain untouched.
 source=re.sub(r'<nav aria-label="(?:デザイン案の切り替え|Compare designs)">.*?</nav>',lambda _:'<nav aria-label="Compare designs">'+a('index.html',t('全案を比較','Compare all'))+''.join(f'<a href="takeda-kinetic-{k}{suffix}.html"'+(' aria-current="page"' if k==v else '')+f'>{k.upper()}</a>' for k in ('abcdefghij' if v in 'hj' else 'abcdefghi'))+'</nav>',source,flags=re.S)
 (ROOT/f'takeda-kinetic-{v}{suffix}.html').write_text(source)

if __name__=='__main__':
 for v in 'hij':
  for lang in ['ja','en']:build(v,lang)
 print('Built H, I and J in Japanese and English.')
