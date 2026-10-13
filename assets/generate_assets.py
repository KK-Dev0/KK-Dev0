import math, os, glob
from xml.sax.saxutils import escape as E
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

GF = '/usr/share/fonts/truetype/google-fonts/'
OUT = '/mnt/user-data/outputs/profile-readme/assets/'
for f in glob.glob(OUT + '*.svg'): os.remove(f)

class F:
    def __init__(s, font):
        s.gs = font.getGlyphSet(); s.cm = font.getBestCmap(); s.u = font['head'].unitsPerEm; s.h = font['hmtx']
    def g(s, c): return s.cm.get(ord(c), s.cm[32])
    def w(s, t, size, ls=0): return sum(s.h[s.g(c)][0] for c in t) * size / s.u + ls * len(t)
    def p(s, t, x, y, size, fill, anchor='start', ls=0, extra=''):
        W = s.w(t, size, ls); x = x - W / 2 if anchor == 'middle' else (x - W if anchor == 'end' else x)
        k = size / s.u; d = ''; cx = x
        for c in t:
            g = s.g(c); pen = SVGPathPen(s.gs, ntos=lambda v: f'{v:.1f}')
            s.gs[g].draw(TransformPen(pen, (k, 0, 0, -k, cx, y))); d += pen.getCommands(); cx += s.h[g][0] * k + ls
        return f'<path d="{d}" fill="{fill}" {extra}/>'

def lora(fn, w): return F(instancer.instantiateVariableFont(TTFont(GF + fn), {'wght': w}))
LI6 = lora('Lora-Italic-Variable.ttf', 600); LI7 = lora('Lora-Italic-Variable.ttf', 700)
PR = F(TTFont(GF + 'Poppins-Regular.ttf')); PM = F(TTFont(GF + 'Poppins-Medium.ttf'))

T = {
 'light': dict(paper='#FBF5EC', ink='#4B3A3A', soft='#8A7373', rose='#C2566B', pink='#E9A7A7', line='#E3D3C2', white='#FFFFFF', note='#FBEBA8', blob1='#F7C9C9', blob2='#D8CCF1', pol='#FFFFFF',
   card=['#F7D9D9','#DCE8D5','#E6DEF7','#FBF0C8','#DCEAF3','#FADFCB'], tape=['#E9A7A7','#A8C3A0','#BBA9E6','#EBCB6A','#9CC3DA','#EDAA80'], pill=['#F7D9D9','#DCE8D5','#E6DEF7','#FBF0C8','#DCEAF3','#FADFCB']),
 'dark': dict(paper='#1F1720', ink='#F3E9E4', soft='#B7A3A8', rose='#F0A3B5', pink='#D98B9B', line='#3A2D3A', white='#2A2030', note='#6E5F2A', blob1='#6B2F46', blob2='#3F3470', pol='#F3E9E4',
   card=['#3A2631','#2B3A2F','#342C52','#4A4025','#263B47','#4A3027'], tape=['#9C5A6B','#5F7F5C','#6C5CA8','#A38C3E','#4F7F99','#A66A4A'], pill=['#3A2631','#2B3A2F','#342C52','#4A4025','#263B47','#4A3027']),
}
CSS = '''<style>
.bob{animation:bob 6s ease-in-out infinite}@keyframes bob{50%{transform:translateY(-5px)}}
.bob2{animation:bob 8s ease-in-out infinite;animation-delay:-3s}
.sw{transform-box:fill-box;transform-origin:50% 100%;animation:sw 5s ease-in-out infinite}@keyframes sw{0%,100%{transform:rotate(-5deg)}50%{transform:rotate(5deg)}}
.sp{transform-box:fill-box;transform-origin:center;animation:sp 3.4s ease-in-out infinite}@keyframes sp{0%,100%{opacity:.25;transform:scale(.7) rotate(0)}50%{opacity:1;transform:scale(1.15) rotate(25deg)}}
.dr{stroke-dasharray:420;animation:dr 4s ease-in-out infinite}@keyframes dr{0%{stroke-dashoffset:420}55%,100%{stroke-dashoffset:0}}
.rl{opacity:0;animation:rl 12s infinite}@keyframes rl{0%{opacity:0;transform:translateY(8px)}5%,22%{opacity:1;transform:none}27%,100%{opacity:0}}
.sp2{transform-box:fill-box;transform-origin:center;animation:spin 14s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}
</style>'''

def sparkle(x, y, r, fill, delay=0):
    d = f'M{x} {y-r} Q{x} {y} {x+r} {y} Q{x} {y} {x} {y+r} Q{x} {y} {x-r} {y} Q{x} {y} {x} {y-r}Z'
    return f'<path class="sp" d="{d}" fill="{fill}" style="animation-delay:{delay}s"/>'
def flower(x, y, r, petal, center):
    ps = ''.join(f'<circle cx="{x+r*.62*math.cos(a*1.2566)}" cy="{y+r*.62*math.sin(a*1.2566)}" r="{r*.46}" fill="{petal}"/>' for a in range(5))
    return f'<g class="sp2">{ps}<circle cx="{x}" cy="{y}" r="{r*.34}" fill="{center}"/></g>'
def heart(x, y, s, fill):
    return f'<path d="M{x} {y+s*.9} C{x-s*1.6} {y-s*.2} {x-s*.7} {y-s*1.2} {x} {y-s*.4} C{x+s*.7} {y-s*1.2} {x+s*1.6} {y-s*.2} {x} {y+s*.9}Z" fill="{fill}"/>'
def squiggle(x, y, w, col, sw=3, cls='dr'):
    n = int(w // 24); d = f'M{x} {y}' + ''.join(f' q6 {-7 if i%2==0 else 7} 12 0 t12 0' for i in range(n * 2))
    return f'<path class="{cls}" d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round"/>'
def tape(x, y, w, h, col, rot, uid):
    return (f'<g transform="translate({x} {y}) rotate({rot})"><defs><pattern id="{uid}" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            f'<rect width="5" height="10" fill="{col}" opacity=".9"/><rect x="5" width="5" height="10" fill="{col}" opacity=".6"/></pattern></defs>'
            f'<rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" fill="url(#{uid})" opacity=".92"/></g>')
def grain(w, h, rx=0):
    return (f'<filter id="gr"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2"/><feColorMatrix type="saturate" values="0"/>'
            f'<feComponentTransfer><feFuncA type="linear" slope=".10"/></feComponentTransfer></filter><rect width="{w}" height="{h}" rx="{rx}" filter="url(#gr)"/>')
def dots(w, h, c):
    return f'<pattern id="dt" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="{c}"/></pattern><rect width="{w}" height="{h}" fill="url(#dt)" opacity=".7"/>'
def svg(w, h, body): return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{CSS}{body}</svg>'

def hills(c, m):
    sky = '#CFE3EE' if m == 'light' else '#3F5F73'
    return (f'<rect width="230" height="230" fill="{sky}"/><circle cx="170" cy="60" r="26" fill="#FBE7A6"/>'
            f'<ellipse cx="70" cy="48" rx="34" ry="11" fill="#fff" opacity=".8"/><ellipse cx="96" cy="42" rx="22" ry="9" fill="#fff" opacity=".8"/>'
            f'<path d="M0 150 Q60 95 120 140 T230 120 V230 H0Z" fill="#C5D8BC"/><path d="M0 185 Q70 130 140 175 T230 160 V230 H0Z" fill="#9DBB93"/>'
            f'<path d="M0 215 Q80 180 160 205 T230 195 V230 H0Z" fill="#7BA06F"/>'
            + ''.join(f'<path d="M{x} {y} l-9 22 h18z M{x} {y+10} l-11 22 h22z" fill="#5E8454"/><rect x="{x-1.5}" y="{y+32}" width="3" height="7" fill="#7A5A44"/>' for x, y in [(40, 150), (62, 160), (196, 170)])
            + '<path d="M120 80 q5 -6 10 0 q5 -6 10 0 M148 96 q4 -5 8 0 q4 -5 8 0" fill="none" stroke="#6B5B5B" stroke-width="1.6" stroke-linecap="round"/>')

def header(m):
    c = T[m]; W, H = 1000, 380
    roles = ['bca student · asansol engineering college', 'computer vision & nlp', 'careful about model evaluation', 'hacktoberfest 2026 completionist']
    rt = ''.join(f'<g class="rl" style="animation-delay:{i*3}s">{PR.p(t, 64, 345, 19, c["soft"])}</g>' for i, t in enumerate(roles))
    karm = LI7.w('karmakar', 92)
    nt = '#4B3A3A' if m == 'light' else '#F3E9E4'
    note = ''.join(PR.p(t, 22, 62 + i * 24, 15, nt) for i, t in enumerate(['training models,', 'sketching hills,', 'touching grass.']))
    b = f'''<defs><filter id="bl"><feGaussianBlur stdDeviation="40"/></filter><filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="6" stdDeviation="7" flood-color="#000" flood-opacity=".22"/></filter>
<clipPath id="cp"><rect width="1000" height="380" rx="28"/></clipPath><clipPath id="ph"><rect width="230" height="230" rx="3"/></clipPath></defs>
<g clip-path="url(#cp)"><rect width="{W}" height="{H}" fill="{c['paper']}"/>{dots(W, H, c['line'])}
<g filter="url(#bl)"><circle class="bob" cx="150" cy="90" r="110" fill="{c['blob1']}" opacity=".55"/><circle class="bob2" cx="860" cy="300" r="120" fill="{c['blob2']}" opacity=".6"/></g>
{grain(W, H)}</g>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="28" fill="none" stroke="{c['line']}" stroke-width="2"/>
{LI6.p("hello, i'm", 66, 110, 30, c['soft'])}
{LI7.p('kaushikee', 60, 205, 92, c['ink'])}
{LI7.p('karmakar', 60, 292, 92, c['ink'])}{LI7.p('.', 60 + karm + 2, 292, 92, c['rose'])}
{squiggle(66, 316, 300, c['pink'], 3.5)}
{rt}
<g transform="translate(655 36) rotate(4)"><g class="bob"><rect x="0" y="0" width="262" height="322" rx="5" fill="{c['pol']}" filter="url(#sh)"/>
<g transform="translate(16 16)"><g clip-path="url(#ph)">{hills(c, m)}</g></g>
{LI6.p('view of the hills', 131, 292, 24, '#4B3A3A', 'middle')}{tape(131, 2, 104, 28, c['tape'][0], -5, 'tp1')}</g></g>
<g transform="translate(546 190) rotate(-6)"><g class="bob2"><rect width="188" height="112" fill="{c['note']}" filter="url(#sh)"/>
{LI7.p('currently:', 20, 40, 24, nt)}{note}{tape(94, 0, 70, 20, c['tape'][1], 3, 'tp2')}</g></g>
{sparkle(600, 70, 14, c['rose'], 0)}{sparkle(960, 60, 11, c['pink'], 1.2)}{sparkle(560, 180, 9, c['tape'][3], .6)}{sparkle(930, 355, 12, c['rose'], 2)}{sparkle(470, 40, 8, c['pink'], 1.8)}
{flower(612, 140, 16, c['pink'], c['tape'][3])}{flower(955, 335, 13, c['tape'][2], c['tape'][3])}
<g class="bob2">{heart(540, 120, 9, c['pink'])}</g>'''
    return svg(W, H, b)

def card(m, d, i):
    c = T[m]; rot = [-1.4, 1.1, -0.8, 1.5, -1.1, 0.9][i]; fill = c['card'][i]; tp = c['tape'][i]
    mw = LI7.w(d['m'], 48)
    x = 24; chips = ''
    for t in d['tags']:
        w = PM.w(t, 12) + 26
        chips += f'<rect x="{x}" y="212" width="{w}" height="28" rx="14" fill="{c["paper"]}" stroke="{tp}" stroke-width="1.6" stroke-dasharray="4 3"/>{PM.p(t, x+w/2, 231, 12, c["ink"], "middle")}'; x += w + 9
    b = f'''<g transform="rotate({rot} 250 142)"><g class="{'bob' if i%2==0 else 'bob2'}">
<rect x="14" y="20" width="472" height="250" rx="16" fill="{fill}" stroke="{c['line']}" stroke-width="1.5"/>
<rect x="22" y="28" width="456" height="234" rx="11" fill="none" stroke="{tp}" stroke-width="1.4" stroke-dasharray="6 5" opacity=".7"/>
{LI7.p(d['n'], 28, 72, 28, c['ink'])}
{PR.p(d['k'], 28, 98, 14.5, c['rose'])}
{PR.p(d['d1'], 28, 126, 13, c['soft'])}{PR.p(d['d2'], 28, 146, 13, c['soft'])}
{LI7.p(d['m'], 28, 196, 48, c['rose'])}{PR.p(d['ml'], 28 + mw + 14, 192, 13, c['soft'])}
{chips}
{heart(404, 62, 5.5, c['rose'])}{PM.p('live', 416, 66, 12, c['ink'])}
<g class="sw">{flower(448, 232, 15, tp, c['paper'])}</g>
{tape(250, 22, 96, 26, tp, -3 + i, f'tc{i}')}</g></g>'''
    return svg(500, 290, b)

def toolbox(m):
    c = T[m]; items = ['Python','Java','C','SQL','PyTorch','scikit-learn','YOLOv8','Flask','Streamlit','Gradio','Git','Power BI','NLP','Computer Vision','DSA']
    rows = [items[:8], items[8:]]; b = ''; k = 0
    for ri, row in enumerate(rows):
        ws = [PM.w(t, 17) + 38 for t in row]; tot = sum(ws) + 14 * (len(row) - 1); x = (1000 - tot) / 2; y = 30 + ri * 72
        for t, w in zip(row, ws):
            rot = [-3, 2, -1.5, 3, -2, 1.5][k % 6]; col = c['pill'][k % 6]
            b += (f'<g transform="translate({x} {y}) rotate({rot} {w/2} 22)"><g class="{"bob" if k%2 else "bob2"}" style="animation-delay:{-(k*0.7)%6}s">'
                  f'<rect width="{w}" height="44" rx="22" fill="{col}" stroke="{c["tape"][k%6]}" stroke-width="1.8" stroke-dasharray="5 4"/>{PM.p(t, w/2, 28, 17, c["ink"], "middle")}</g></g>')
            x += w + 14; k += 1
    b += sparkle(40, 40, 10, c['rose'], .4) + sparkle(960, 130, 10, c['pink'], 1.4) + flower(40, 120, 12, c['pink'], c['tape'][3])
    return svg(1000, 160, b)

def heading(m, t):
    c = T[m]; tw = LI7.w(t, 46)
    return svg(1000, 84, f'{LI7.p(t, 14, 54, 46, c["ink"])}{squiggle(16, 70, tw, c["pink"], 3.5)}{sparkle(tw + 40, 30, 11, c["rose"], 0)}{sparkle(tw + 66, 48, 7, c["pink"], 1)}')

def footer(m):
    c = T[m]
    b = (f'{LI7.p("little steps, big progress", 500, 72, 50, c["ink"], "middle")}{PR.p("made with care in Asansol", 500, 112, 15, c["soft"], "middle")}'
         f'{sparkle(120, 50, 13, c["rose"], 0)}{sparkle(880, 60, 13, c["pink"], 1)}{flower(70, 90, 13, c["pink"], c["tape"][3])}{flower(930, 100, 13, c["tape"][2], c["tape"][3])}<g class="bob">{heart(500, 140, 8, c["rose"])}</g>')
    return svg(1000, 160, b)

CARDS = [
 ('creditsense', dict(n='CreditSense AI', k='Explainable credit-risk decision support', d1='Cost-based approve / review / decline,', d2='plus an age-group fairness audit', m='0.868', ml='ROC-AUC on 30,000 held-out', tags=['scikit-learn','Flask','Fairness audit'])),
 ('docclassify', dict(n='Document Classification AI', k='6-topic NLP classifier', d1='TF-IDF + tuned Linear SVM, benchmarked', d2='against sentence embeddings', m='91.1%', ml='accuracy on 1,131 held-out docs', tags=['scikit-learn','TF-IDF','Streamlit'])),
 ('backyard', dict(n='Backyard Sweep', k='Mosquito breeding-site detector', d1='YOLOv8n trained on VisText-Mosquito,', d2='field-tested on real photos', m='0.926', ml='mAP50 on the test split', tags=['YOLOv8','Ultralytics','Python'])),
 ('vayuvega', dict(n='VAYUVEGA (PRISM-TC)', k='Tropical cyclone intensity classifier', d1='Smart India Hackathon 2026,', d2='where I was the Evaluation Lead', m='372', ml='held-out images evaluated', tags=['PyTorch','timm','EfficientNet-B0'])),
 ('stuckdoctor', dict(n='Stuck Doctor', k='Helps you finally book the doctor', d1='Hacktoberfest x HackTropica, Asansol,', d2='built in one day', m='4', ml='languages supported', tags=['Gemma 4','Gradio','JavaScript'])),
 ('taskflow', dict(n='TaskFlow', k='Task & focus workspace', d1='Priorities, dashboard and a transparent', d2='rules-based planner', m='25/15/5', ml='minute focus timer', tags=['Flask','SQLite','JavaScript'])),
]
HEADS = {'about': 'about me', 'work': 'selected work', 'beyond': 'beyond the code', 'hi': 'say hi'}
for m in ('light', 'dark'):
    open(f'{OUT}header-{m}.svg', 'w').write(header(m)); open(f'{OUT}toolbox-{m}.svg', 'w').write(toolbox(m)); open(f'{OUT}footer-{m}.svg', 'w').write(footer(m))
    for k, t in HEADS.items(): open(f'{OUT}h-{k}-{m}.svg', 'w').write(heading(m, t))
    for i, (k, d) in enumerate(CARDS): open(f'{OUT}{k}-{m}.svg', 'w').write(card(m, d, i))
print(len(os.listdir(OUT)), 'files')
