# -*- coding: utf-8 -*-
"""Categoria 'Liquori 0%' + 10 prodotti (catalogo, pagine IT/EN, foto Gemini). Rilanciabile.
python automation/liquori_0.py [--no-foto] [--no-push]   (account Gemini: env GEMINI_ACCOUNT)"""
import csv, json, os, re, subprocess, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = r'C:\Users\mirco\Desktop\gemini_auto\img.py'
OUT = os.path.join(R, 'assets', 'images', 'prodotti')
CID, CNOME, CEN, CSLUG = 'liquori-0', 'Liquori 0%', 'Liqueurs 0%', 'liqueurs-0'
CAT_IT = 'Liquori analcolici 0%: amaretto, limoncello, amaro, sambuca, nocino e mirto. I grandi classici italiani da fine pasto, senza alcol.'
CAT_EN = 'Non-alcoholic liqueurs at 0%: amaretto, limoncello, amaro, sambuca, nocino and mirto. The great Italian after-dinner classics, alcohol-free.'
# id, nome, nome EN, desc IT, desc EN, aspetto bottiglia
P = [
 ('amaretto-0', 'Amaretto 0%', 'Amaretto 0%', 'Dolce e avvolgente, con mandorle amare e nocciolo di albicocca: il classico da fine pasto, senza alcol.', 'Sweet and rounded, with bitter almonds and apricot kernel: the classic after-dinner liqueur, alcohol-free.', 'squat amber-brown bottle with a wooden cork'),
 ('limoncello-0', 'Limoncello 0%', 'Limoncello 0%', 'Scorze di limone in infusione, fresco e zuccherino. Da servire ghiacciato, come da tradizione.', 'Infused lemon zest, fresh and lightly sweet. Serve ice-cold, as tradition wants.', 'tall elegant bottle filled with bright lemon-yellow liquid'),
 ('amaro-erbe-0', 'Amaro alle Erbe 0%', 'Herbal Amaro 0%', 'Genziana, rabarbaro ed erbe officinali: il bitter-dolce da digestivo, con tutto il carattere dell\'amaro e nessun alcol.', 'Gentian, rhubarb and medicinal herbs: the bittersweet digestif, with all the character of an amaro and no alcohol.', 'dark brown apothecary-style bottle with very dark liquid'),
 ('sambuca-0', 'Sambuca 0%', 'Sambuca 0%', 'Anice stellato e finocchietto: dolce, balsamica e inconfondibile. Perfetta liscia o con il caffè.', 'Star anise and fennel: sweet, balsamic and unmistakable. Perfect neat or with coffee.', 'tall slim bottle with crystal-clear transparent liquid'),
 ('crema-caffe-0', 'Crema al Caffè 0%', 'Coffee Cream Liqueur 0%', 'Espresso e crema vellutata: ideale sul gelato, nei dessert e nei cocktail da fine serata.', 'Espresso and velvety cream: ideal over ice cream, in desserts and in late-night cocktails.', 'round bottle with creamy coffee-brown liquid'),
 ('irish-cream-style-0', 'Irish Cream Style 0%', 'Irish Cream Style 0%', 'Crema, cacao e vaniglia in stile liquore irlandese: morbida, cremosa, da bere con ghiaccio o nel caffè.', 'Cream, cocoa and vanilla in the Irish liqueur style: soft, creamy, to sip over ice or in coffee.', 'bottle with creamy light-beige opaque liquid'),
 ('triple-sec-0', 'Triple Sec Arancia 0%', 'Triple Sec Orange 0%', 'Scorze di arancia amara e dolce: la base dei grandi cocktail agli agrumi, Margarita e Cosmopolitan inclusi.', 'Bitter and sweet orange peel: the base of the great citrus cocktails, Margarita and Cosmopolitan included.', 'square-shouldered bottle with clear golden-orange liquid'),
 ('nocino-0', 'Nocino 0%', 'Nocino 0%', 'Mallo di noci verdi e spezie: scuro, profondo, con note di cannella e chiodi di garofano.', 'Green walnut husk and spices: dark and deep, with notes of cinnamon and cloves.', 'dark bottle with almost black walnut-brown liquid'),
 ('mirto-0', 'Mirto 0%', 'Mirto 0%', 'Bacche di mirto in stile sardo: aromatico, balsamico, dal colore rosso-viola intenso.', 'Myrtle berries in the Sardinian style: aromatic, balsamic, with an intense red-purple color.', 'bottle with deep ruby purple-red liquid'),
 ('liquirizia-0', 'Liquore alla Liquirizia 0%', 'Liquorice Liqueur 0%', 'Radice di liquirizia, nero e setoso, dolce-amaro: da servire freddo a fine pasto.', 'Liquorice root, black and silky, bittersweet: serve chilled after dinner.', 'bottle with glossy jet-black liquid'),
]
PREZZO = 1290
EXTRA = ('Single premium bottle centered, pure white #FFFFFF background, soft shadow, studio product photo. The label must contain ONLY the product name '
         'in large elegant letters and the text "0%" below it. No other text at all: no small print, no volume, no alcohol statement, no brand, no slogans.')
ICONA = '\U0001F377'
def w(rel, txt):
    p = os.path.join(R, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8', newline='\n').write(txt)
def fm(**k):
    return '---\n' + ''.join('%s: %s\n' % (a, json.dumps(b, ensure_ascii=False) if isinstance(b, str) and a in ('title', 'description', 'seo_title', 'seo_description') else b) for a, b in k.items()) + '---\n'
def sh(*a): return subprocess.run(['git', '-C', R, *a], capture_output=True, text=True, encoding='utf-8', errors='replace')

def main():
    cp = os.path.join(R, '_data', 'catalogo.json'); raw = open(cp, encoding='utf-8-sig').read(); c = json.loads(raw)
    ind = len(re.match(r'\{\n( *)', raw).group(1)) or 2
    # foto
    if '--no-foto' not in sys.argv:
        todo = [p for p in P if not os.path.exists(os.path.join(OUT, p[0] + '.webp'))]
        if todo:
            lista = os.path.join(R, 'automation', 'tmp_lista.csv')
            with open(lista, 'w', encoding='utf-8', newline='') as f:
                wr = csv.writer(f, delimiter=';')
                for i, n, ne, di, de, b in todo:
                    wr.writerow([i, 'Premium non-alcoholic Italian %s liqueur: %s. Label text: "%s".' % (ne, b, n.upper()), 'prodotto'])
            print('img.py exit', subprocess.run([sys.executable, IMG, '--lista', lista, '--out', OUT, '--extra', EXTRA], cwd=R, text=True, encoding='utf-8', errors='replace').returncode)
    # categoria
    cimg = 'assets/images/categorie/%s.webp' % CID
    if not [x for x in c['categorie'] if x['id'] == CID]:
        c['categorie'].append(dict(id=CID, nome=CNOME, icona=ICONA, descrizione=CAT_IT, immagine=cimg, tr=dict(en=dict(nome=CEN, descrizione=CAT_EN))))
    src = os.path.join(OUT, 'amaretto-0.webp'); dst = os.path.join(R, cimg)
    if os.path.exists(src) and not os.path.exists(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True); open(dst, 'wb').write(open(src, 'rb').read())
    w('_negozio/categoria-%s.md' % CID, fm(layout='negozio-categoria', title=CNOME, cid=CID, ref='shop-cat-' + CID, permalink='/negozio/categoria/%s/' % CID, description=CAT_IT,
      seo_title='Liquori Analcolici 0% - Amaretto, Limoncello, Amaro, Sambuca', seo_description=CAT_IT, seo_image='/' + cimg))
    w('en/negozio/categoria/%s.md' % CID, fm(layout='negozio-categoria', title=CEN, cid=CID, permalink='/en/shop/category/%s/' % CSLUG, description=CAT_EN,
      seo_title='Non-Alcoholic Liqueurs 0% - Amaretto, Limoncello, Amaro, Sambuca', seo_description=CAT_EN, seo_image='/' + cimg, lang='en', locale='en', ref='shop-cat-' + CID, tr='tradotto'))
    # prodotti
    for i, n, ne, di, de, b in P:
        has = os.path.exists(os.path.join(OUT, i + '.webp'))
        new = dict(tipo='fisico', id=i, nome=n, categoria=CID, prezzo_centesimi=PREZZO, descrizione=di, descrizione_completa=di,
                   immagine='assets/images/prodotti/%s.webp' % i if has else '', icona=ICONA, visibile=True, tr=dict(en=dict(descrizione=de, descrizione_completa=de)))
        if ne != n: new['tr']['en']['nome'] = ne
        old = [x for x in c['prodotti'] if x['id'] == i]
        if old: c['prodotti'][c['prodotti'].index(old[0])] = new
        else: c['prodotti'].append(new)
        img = '/assets/images/prodotti/%s.webp' % i
        w('_negozio/%s.md' % i, fm(layout='negozio-prodotto', title=n, pid=i, permalink='/negozio/%s/' % i, description='%s: %s' % (n, di),
          seo_title='%s Analcolico - Liquore senza alcol' % n.replace(' 0%', ' 0%'), seo_description='%s: %s' % (n, di), seo_image=img, ref='shop-prod-' + i))
        w('en/negozio/%s.md' % i, fm(layout='negozio-prodotto', title=ne, pid=i, permalink='/en/shop/%s/' % i, description='%s: %s' % (ne, de),
          seo_title='Non-Alcoholic %s - Alcohol-Free Liqueur' % ne, seo_description='%s: %s' % (ne, de), seo_image=img, lang='en', locale='en', ref='shop-prod-' + i, tr='tradotto'))
    open(cp, 'w', encoding='utf-8', newline='\n').write(json.dumps(c, ensure_ascii=False, indent=ind) + ('\n' if raw.endswith('\n') else ''))
    print('prodotti nel catalogo:', len(c['prodotti']), '| senza foto:', [p['id'] for p in c['prodotti'] if p['categoria'] == CID and not p['immagine']])
    if '--no-push' not in sys.argv:
        sh('add', '_data/catalogo.json', '_negozio', 'en/negozio', 'assets/images', 'automation/liquori_0.py')
        print(sh('commit', '-q', '-m', 'Categoria Liquori 0%: 10 prodotti analcolici con foto, pagine IT/EN').stderr[-200:])
        sh('pull', '-q', '--rebase'); print(sh('push').stderr[-200:]); print('push ok')

if __name__ == '__main__':
    main()
