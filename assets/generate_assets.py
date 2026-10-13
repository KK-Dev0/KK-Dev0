import random
from xml.sax.saxutils import escape as E
OUT = '/mnt/user-data/outputs/profile-readme/assets/'
T = {
 'dark':  dict(bg1='#0e0b1f', bg2='#241a52', card='#15112b', tx='#ece9f8', mu='#a29ec3', ac='#a78bfa', ac2='#f0abfc', ln='#2a2450', chip='#241d4a', ok='#4ade80'),
 'light': dict(bg1='#f5f0ff', bg2='#e4d9ff', card='#ffffff', tx='#1b1636', mu='#5f5a7e', ac='#7c3aed', ac2='#c026d3', ln='#ddd6fe', chip='#ede9fe', ok='#16a34a'),
}
FONT = "font-family:'Segoe UI',-apple-system,Helvetica,Arial,sans-serif"
MONO = "font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

def header(m):
    c = T[m]; r = random.Random(7)
    stars = ''.join(f'<circle cx="{r.randint(20,980)}" cy="{r.randint(15,150)}" r="{r.choice([1,1.5,2])}" fill="{c["ac2"]}" class="tw" style="animation-delay:{r.random()*4:.1f}s"/>' for _ in range(28))
    roles = ['BCA student · Asansol Engineering College', 'Computer vision & NLP', 'Careful about model evaluation', 'Hacktoberfest 2026 Completionist']
    rt = ''.join(f'<text x="500" y="168" text-anchor="middle" class="rl" style="animation-delay:{i*3}s;{MONO};font-size:19px" fill="{c["mu"]}">{E(t)}</text>' for i, t in enumerate(roles))
    wave = 'M0 205 ' + ' '.join(f'Q {125+250*i} {178 if i%2==0 else 232} {250+250*i} 205' for i in range(8)) + ' V240 H0 Z'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="240" viewBox="0 0 1000 240">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['bg1']}"/><stop offset="1" stop-color="{c['bg2']}"/></linearGradient>
<linearGradient id="nm" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c['ac']}"/><stop offset="1" stop-color="{c['ac2']}"/></linearGradient>
<filter id="bl"><feGaussianBlur stdDeviation="28"/></filter>
</defs>
<style>
.tw{{animation:tw 3.5s ease-in-out infinite}}@keyframes tw{{0%,100%{{opacity:.1}}50%{{opacity:.9}}}}
.b1{{animation:f1 9s ease-in-out infinite}}@keyframes f1{{50%{{transform:translate(90px,25px)}}}}
.b2{{animation:f2 11s ease-in-out infinite}}@keyframes f2{{50%{{transform:translate(-110px,-20px)}}}}
.wv{{animation:wv 14s linear infinite}}@keyframes wv{{to{{transform:translateX(-1000px)}}}}
.rl{{opacity:0;animation:rl 12s infinite}}@keyframes rl{{0%{{opacity:0;transform:translateY(8px)}}5%,22%{{opacity:1;transform:none}}27%,100%{{opacity:0}}}}
.nm{{animation:nm 1.4s ease-out both}}@keyframes nm{{from{{opacity:0;transform:translateY(14px)}}}}
.ul{{stroke-dasharray:260;animation:ul 3s ease-in-out infinite}}@keyframes ul{{0%{{stroke-dashoffset:260}}50%,100%{{stroke-dashoffset:0}}}}
</style>
<rect width="1000" height="240" fill="url(#bg)"/>
<g filter="url(#bl)"><circle class="b1" cx="220" cy="90" r="80" fill="{c['ac']}" opacity=".45"/><circle class="b2" cx="780" cy="110" r="90" fill="{c['ac2']}" opacity=".35"/></g>
{stars}
<text class="nm" x="500" y="108" text-anchor="middle" fill="url(#nm)" style="{FONT};font-size:58px;font-weight:700;letter-spacing:1px">Kaushikee Karmakar</text>
<line class="ul" x1="370" y1="124" x2="630" y2="124" stroke="url(#nm)" stroke-width="3" stroke-linecap="round"/>
{rt}
<path class="wv" d="{wave}" fill="{c['ac']}" opacity=".22"/>
<path class="wv" style="animation-duration:9s" d="{wave}" fill="{c['ac2']}" opacity=".15" transform="translate(-300 6)"/>
</svg>'''

def card(m, d):
    c = T[m]
    x = 22; chips = ''
    for t in d['tags']:
        w = len(t) * 7 + 18
        chips += f'<rect x="{x}" y="160" width="{w}" height="24" rx="12" fill="{c["chip"]}"/><text x="{x+w/2}" y="176" text-anchor="middle" style="{MONO};font-size:11.5px" fill="{c["tx"]}">{E(t)}</text>'
        x += w + 8
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="210" viewBox="0 0 480 210">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['ac']}"/><stop offset="1" stop-color="{c['ac2']}"/></linearGradient></defs>
<style>
.sh{{stroke-dasharray:150 1050;animation:sh 5s linear infinite}}@keyframes sh{{to{{stroke-dashoffset:-1200}}}}
.pd{{animation:pd 2s ease-in-out infinite}}@keyframes pd{{50%{{opacity:.25}}}}
.mt{{animation:mt 1s ease-out both}}@keyframes mt{{from{{opacity:0;transform:translateY(8px)}}}}
</style>
<rect x="1" y="1" width="478" height="208" rx="16" fill="{c['card']}" stroke="{c['ln']}" stroke-width="1.5"/>
<rect class="sh" x="1" y="1" width="478" height="208" rx="16" fill="none" stroke="url(#g)" stroke-width="2.5" stroke-linecap="round"/>
<text x="22" y="40" style="{FONT};font-size:21px;font-weight:700" fill="{c['tx']}">{E(d['n'])}</text>
<circle class="pd" cx="408" cy="34" r="4" fill="{c['ok']}"/><text x="418" y="38" style="{MONO};font-size:11px" fill="{c['mu']}">LIVE</text>
<text x="22" y="66" style="{FONT};font-size:14px" fill="{c['ac']}">{E(d['k'])}</text>
<text x="22" y="92" style="{FONT};font-size:13px" fill="{c['mu']}">{E(d['d1'])}</text>
<text x="22" y="112" style="{FONT};font-size:13px" fill="{c['mu']}">{E(d['d2'])}</text>
<text class="mt" x="22" y="146" style="{FONT};font-size:30px;font-weight:700" fill="url(#g)">{E(d['m'])}</text>
<text x="{22+len(d['m'])*17+10}" y="146" style="{FONT};font-size:12px" fill="{c['mu']}">{E(d['ml'])}</text>
{chips}
</svg>'''

def ticker(m):
    c = T[m]
    items = ['Python','Java','C','SQL','PyTorch','scikit-learn','YOLOv8','Flask','Streamlit','Gradio','Git','Power BI','NLP','Computer Vision']
    s = '   ◆   '.join(items) + '   ◆   '
    w = round(len(s) * 8.4)
    t = lambda x: f'<text x="{x}" y="29" textLength="{w}" lengthAdjust="spacing" xml:space="preserve" style="{MONO};font-size:14px" fill="{c["tx"]}">{E(s)}</text>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="44" viewBox="0 0 1000 44">
<defs><linearGradient id="f" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c['bg1']}"/><stop offset=".08" stop-color="{c['bg1']}" stop-opacity="0"/><stop offset=".92" stop-color="{c['bg1']}" stop-opacity="0"/><stop offset="1" stop-color="{c['bg1']}"/></linearGradient></defs>
<style>.tk{{animation:tk 28s linear infinite}}@keyframes tk{{to{{transform:translateX(-{w}px)}}}}</style>
<rect width="1000" height="44" rx="10" fill="{c['card']}" stroke="{c['ln']}"/>
<g class="tk">{t(0)}{t(w)}{t(2*w)}</g>
<rect width="1000" height="44" rx="10" fill="url(#f)"/>
</svg>'''

CARDS = {
 'creditsense': dict(n='CreditSense AI', k='Explainable credit-risk decision support', d1='Cost-based approve / review / decline', d2='with an age-group fairness audit', m='0.868', ml='ROC-AUC on 30,000 held-out', tags=['scikit-learn','Flask','Fairness audit']),
 'docclassify': dict(n='Document Classification AI', k='6-topic NLP classifier', d1='TF-IDF + tuned Linear SVM, benchmarked', d2='against sentence embeddings', m='91.1%', ml='accuracy on 1,131 held-out docs', tags=['scikit-learn','TF-IDF','Streamlit']),
 'backyard': dict(n='Backyard Sweep', k='Mosquito breeding-site detector', d1='YOLOv8n trained on VisText-Mosquito,', d2='field-tested on real photos', m='0.926', ml='mAP50 on the test split', tags=['YOLOv8','Ultralytics','Python']),
 'vayuvega': dict(n='VAYUVEGA (PRISM-TC)', k='Tropical cyclone intensity classifier', d1='Smart India Hackathon 2026.', d2='I was the Evaluation Lead', m='372', ml='held-out images evaluated', tags=['PyTorch','timm','EfficientNet-B0']),
 'stuckdoctor': dict(n='Stuck Doctor', k='Helps you finally book the doctor', d1='Hacktoberfest x HackTropica, Asansol,', d2='built in one day', m='4', ml='languages supported', tags=['Gemma 4','Gradio','JavaScript']),
 'taskflow': dict(n='TaskFlow', k='Task & focus workspace', d1='Priorities, dashboard and a transparent', d2='rules-based planner', m='25/15/5', ml='minute focus timer', tags=['Flask','SQLite','JavaScript']),
}
for m in ('dark', 'light'):
    open(f'{OUT}header-{m}.svg', 'w').write(header(m))
    open(f'{OUT}skills-{m}.svg', 'w').write(ticker(m))
    for k, d in CARDS.items():
        open(f'{OUT}{k}-{m}.svg', 'w').write(card(m, d))
print('done')
