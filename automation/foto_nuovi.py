# -*- coding: utf-8 -*-
"""PASSATA 2: foto Gemini per i prodotti senza immagine + immagini categorie nuove. Rilanciabile (fa solo i mancanti).
python automation/foto_nuovi.py [--max N] [--no-push] [id ...]   Account: env GEMINI_ACCOUNT (img.py cambia da solo se finiscono i crediti)"""
import csv, json, os, re, shutil, subprocess, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAT = os.path.join(R, '_data', 'catalogo.json')
OUT = os.path.join(R, 'assets', 'images', 'prodotti')
IMG = r'C:\Users\mirco\Desktop\gemini_auto\img.py'
ORDINE = ['bollicine-0', 'box-regalo-0', 'martini-dessert-0', 'aperitivi-0', 'distillati-0', 'tropicali-0', 'long-drink-0', 'liquori-0', 'vino-0', 'mixer-0']
COPERTINE = {'bollicine-0': 'prosecco-brut-0', 'box-regalo-0': 'box-natale-bollicine-0', 'martini-dessert-0': 'pornstar-martini-0', 'vino-0': 'vino-rosso-0', 'mixer-0': 'tonic-premium'}
EXTRA = ('Single product centered, pure white #FFFFFF background, soft shadow, studio product photo. The label must contain ONLY the product name '
         'in large elegant letters and the text "0%" below it. No other text at all: no small print, no volume, no alcohol statement, no brand, no slogans.')
EXTRA_MIXER = EXTRA.replace(' and the text "0%" below it', '').replace('ONLY the product name', 'ONLY the product name')
def soggetto(p):
    en = p.get('tr', {}).get('en', {}); ne = en.get('nome') or p['nome']; de = en.get('descrizione', '')
    c = p['categoria']
    if c == 'box-regalo-0': return 'Premium gift box, closed, kraft and dark-green with a ribbon and a few blank bottles peeking out. Box lid text: "%s". Concept: %s' % (ne.upper(), de)
    if c == 'bollicine-0': return 'Elegant sparkling wine bottle with cork and wire cage, foil neck. Label text: "%s". Concept: %s' % (ne.upper(), de)
    if c == 'vino-0': return 'Classic wine bottle with the right wine color. Label text: "%s". Concept: %s' % (ne.upper(), de)
    if c == 'mixer-0': return 'Premium mixer bottle (small glass bottle). Label text: "%s". Concept: %s' % (ne.upper(), de)
    return 'Premium non-alcoholic ready-to-drink cocktail bottle, liquid color matching the drink. Label text: "%s". Concept: %s' % (ne.upper(), de)
def sh(*a): return subprocess.run(['git', '-C', R, *a], capture_output=True, text=True, encoding='utf-8', errors='replace')

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--') and not a.isdigit()]
    mx = int(sys.argv[sys.argv.index('--max') + 1]) if '--max' in sys.argv else 999
    d = json.load(open(CAT, encoding='utf-8-sig')); prod = d['prodotti']
    todo = [p for p in prod if (p['id'] in args if args else not p.get('immagine')) and not os.path.exists(os.path.join(OUT, p['id'] + '.webp'))]
    todo.sort(key=lambda p: ORDINE.index(p['categoria']) if p['categoria'] in ORDINE else 99)
    todo = todo[:mx]
    print('da generare:', len(todo))
    for g in range(0, len(todo), 1000):
        if not todo: break
        lista = os.path.join(R, 'automation', 'tmp_lista.csv')
        with open(lista, 'w', encoding='utf-8', newline='') as f:
            wr = csv.writer(f, delimiter=';')
            for p in todo: wr.writerow([p['id'], soggetto(p), 'prodotto'])
        print('img.py exit', subprocess.run([sys.executable, IMG, '--lista', lista, '--out', OUT, '--extra', EXTRA], cwd=R, text=True, encoding='utf-8', errors='replace').returncode)
        break
    ok = []
    for p in prod:
        f = os.path.join(OUT, p['id'] + '.webp')
        if os.path.exists(f) and not p.get('immagine'):
            p['immagine'] = 'assets/images/prodotti/%s.webp' % p['id']; ok.append(p['id'])
            for rel in ('_negozio/%s.md' % p['id'], 'en/negozio/%s.md' % p['id']):
                fp = os.path.join(R, rel)
                if os.path.exists(fp):
                    s = open(fp, encoding='utf-8').read()
                    if 'seo_image:' not in s:
                        s = s.replace('\nref:', '\nseo_image: /assets/images/prodotti/%s.webp\nref:' % p['id'], 1)
                        open(fp, 'w', encoding='utf-8', newline='\n').write(s)
    for c in d['categorie']:
        src = os.path.join(OUT, COPERTINE.get(c['id'], '') + '.webp'); dst = os.path.join(R, 'assets', 'images', 'categorie', c['id'] + '.webp')
        if c['id'] in COPERTINE and not c.get('immagine') and os.path.exists(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copyfile(src, dst); c['immagine'] = 'assets/images/categorie/%s.webp' % c['id']
    json.dump(d, open(CAT, 'w', encoding='utf-8', newline='\n'), ensure_ascii=False, indent=2)
    manca = [p['id'] for p in prod if not p.get('immagine')]
    print('collegate:', len(ok), '| ancora senza foto:', len(manca))
    if ok and '--no-push' not in sys.argv:
        sh('add', '_data/catalogo.json', '_negozio', 'en/negozio', 'assets/images', 'automation/foto_nuovi.py')
        sh('commit', '-q', '-m', 'Foto nuovi prodotti: %d immagini' % len(ok)); sh('pull', '-q', '--rebase'); print(sh('push').stderr[-150:]); print('push ok')

if __name__ == '__main__':
    main()
