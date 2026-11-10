# Logo/favicon a tema: coppa cocktail (martini) vintage su quadrato corallo. Colori da _data/tema.json. Uso: python automation/genera_logo_cocktail.py
# Scrive favicon.svg, favicon-32/192/512.png, apple-touch-icon.png, favicon.ico in assets/images e nella radice.
import json, os
from PIL import Image, ImageDraw
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); IMG = os.path.join(ROOT, 'assets', 'images')
t = json.load(open(os.path.join(ROOT, '_data', 'tema.json'), encoding='utf-8'))
def hx(s): s = s.lstrip('#'); return tuple(int(s[i:i+2], 16) for i in (0, 2, 4))
def mix(a, b, k): return tuple(round(a[i] + (b[i] - a[i]) * k) for i in range(3))
def h(c): return '#%02x%02x%02x' % c
acc = hx(t.get('accent', '#ff6b5b')); TOP = mix(acc, (255, 255, 255), .12); BOT = mix(acc, (150, 40, 40), .45)
CREAM = (255, 246, 236); LIQ = (255, 214, 150); OLV = (176, 214, 96)
BOWL = [(13, 15), (51, 15), (32, 38)]; LQ = [(17.6, 21), (46.4, 21), (32, 36.4)]
svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient></defs>'
 '<rect width="64" height="64" rx="14" fill="url(#s)"/><polygon points="17.6,21 46.4,21 32,36.4" fill="%s"/>'
 '<g fill="none" stroke="%s" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><polygon points="13,15 51,15 32,38"/><line x1="32" y1="38" x2="32" y2="51"/><line x1="22" y1="52" x2="42" y2="52"/></g>'
 '<line x1="45" y1="8" x2="33" y2="29" stroke="%s" stroke-width="1.6" stroke-linecap="round"/><circle cx="36" cy="24" r="3.2" fill="%s"/></svg>\n' % (h(TOP), h(BOT), h(LIQ), h(CREAM), h(CREAM), h(OLV)))
open(os.path.join(IMG, 'favicon.svg'), 'w', encoding='utf-8', newline='\n').write(svg)
def render(N):
    M = N * 8; k = M / 64
    g = Image.new('RGB', (1, M))
    for y in range(M): g.putpixel((0, y), mix(TOP, BOT, y / (M - 1)))
    im = Image.new('RGBA', (M, M), (0, 0, 0, 0)); mask = Image.new('L', (M, M), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, M - 1, M - 1), radius=int(14 * k), fill=255)
    im.paste(g.resize((M, M)).convert('RGBA'), (0, 0), mask); d = ImageDraw.Draw(im)
    P = lambda pts: [(x * k, y * k) for x, y in pts]; w = int(2.4 * k)
    d.polygon(P(LQ), fill=LIQ)
    d.line(P([(45, 8), (33, 29)]), fill=OLV if False else CREAM, width=int(1.6 * k))
    cx, cy, r = 36 * k, 24 * k, 3.2 * k; d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=OLV)
    d.line(P(BOWL + [BOWL[0], BOWL[1]]), fill=CREAM, width=w, joint='curve')
    d.line(P([(32, 38), (32, 51)]), fill=CREAM, width=w); d.line(P([(22, 52), (42, 52)]), fill=CREAM, width=w)
    for x, y in [(13, 15), (51, 15), (32, 38), (32, 51), (22, 52), (42, 52)]:
        d.ellipse(((x - 1.2) * k, (y - 1.2) * k, (x + 1.2) * k, (y + 1.2) * k), fill=CREAM)
    return im.resize((N, N), Image.LANCZOS)
for n, name in [(32, 'favicon-32.png'), (192, 'favicon-192.png'), (512, 'favicon-512.png'), (180, 'apple-touch-icon.png')]:
    render(n).save(os.path.join(IMG, name))
ico = render(256); ico.save(os.path.join(IMG, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48)])
import shutil
for f in ('favicon.ico',): shutil.copy(os.path.join(IMG, f), os.path.join(ROOT, f))
print('ok')
