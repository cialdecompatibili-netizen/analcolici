# -*- coding: utf-8 -*-
"""PASSATA 1 (testo minimale, SENZA foto): 5 categorie nuove + prodotti nuovi in tutte le categorie. Rilanciabile.
Passata 2 = foto (foto_nuovi.py), passata 3 = testi completi. python automation/aggiungi_catalogo.py [--no-push]"""
import json, os, re, subprocess, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATS = """bollicine-0|Bollicine 0%|Sparkling 0%|sparkling-0|\U0001F37E|Spumante, Prosecco e cocktail con le bollicine senza alcol: Bellini, Rossini, Mimosa e brindisi 0%.|Alcohol-free sparkling wine, Prosecco and bubbly cocktails: Bellini, Rossini, Mimosa and 0% toasts.|Bollicine Analcoliche 0% - Spumante, Prosecco, Bellini|Non-Alcoholic Sparkling 0% - Prosecco, Bellini, Mimosa
box-regalo-0|Box regalo 0%|Gift boxes 0%|gift-boxes-0|\U0001F381|Confezioni regalo di cocktail e bollicine analcolici: l'idea giusta per Natale, compleanni e Dry January.|Gift boxes of non-alcoholic cocktails and sparkling: the right idea for Christmas, birthdays and Dry January.|Box Regalo Analcolici 0% - Cocktail e Bollicine|Non-Alcoholic Gift Boxes 0% - Cocktails and Sparkling
martini-dessert-0|Martini e dessert 0%|Martinis and desserts 0%|martinis-desserts-0|\U0001F370|Pornstar Martini, French Martini, Cosmopolitan e cocktail da dessert senza alcol, cremosi e fruttati.|Pornstar Martini, French Martini, Cosmopolitan and dessert cocktails without alcohol, creamy and fruity.|Martini e Cocktail Dessert Analcolici 0%|Non-Alcoholic Martinis and Dessert Cocktails 0%
vino-0|Vino 0%|Wine 0%|wine-0|\U0001F347|Vino rosso, bianco e rosato senza alcol, più vin brulé e sangria: il gusto del vino, senza una goccia di alcol.|Red, white and rosé wine without alcohol, plus mulled wine and sangria: the taste of wine, without a drop of alcohol.|Vino Analcolico 0% - Rosso, Bianco, Rosato|Non-Alcoholic Wine 0% - Red, White, Rosé
mixer-0|Mixer e toniche|Mixers and tonics|mixers-0|\U0001F9CA|Toniche, ginger beer, soda e sciroppi per preparare i tuoi cocktail analcolici a casa.|Tonics, ginger beer, soda and syrups to make your non-alcoholic cocktails at home.|Mixer e Toniche per Cocktail Analcolici|Mixers and Tonics for Non-Alcoholic Cocktails"""
P = """bollicine-0|prosecco-brut-0|Prosecco Brut 0%||Perlage fine e note di mela verde e agrumi: la bollicina italiana per eccellenza, senza alcol.|Fine bubbles with green apple and citrus notes: the Italian sparkling classic, alcohol-free.|1190
bollicine-0|spumante-dolce-0|Spumante Dolce 0%|Sweet Sparkling 0%|Aromatico e fruttato, in stile moscato: per brindisi e dessert di Capodanno, senza alcol.|Aromatic and fruity, Moscato style: for toasts and New Year desserts, alcohol-free.|990
bollicine-0|spumante-rose-0|Spumante Rosé 0%|Sparkling Rosé 0%|Profumo di fragola e lampone, fresco e vivace: perfetto per l'aperitivo, senza alcol.|Strawberry and raspberry aroma, fresh and lively: perfect for aperitivo, alcohol-free.|1190
bollicine-0|bellini-0|Bellini 0%||Spumante e purea di pesca bianca: il cocktail veneziano del Harry's Bar, ora 0%.|Sparkling wine and white peach purée: the Venetian Harry's Bar cocktail, now 0%.|990
bollicine-0|rossini-0|Rossini 0%||Spumante e fragole fresche frullate: il cugino rosso del Bellini, ora 0%.|Sparkling wine and blended fresh strawberries: the red cousin of the Bellini, now 0%.|990
bollicine-0|mimosa-0|Mimosa 0%||Spumante e succo d'arancia spremuto: il cocktail del brunch, ora 0%.|Sparkling wine and fresh orange juice: the brunch cocktail, now 0%.|990
bollicine-0|kir-royale-0|Kir Royale 0%||Spumante e crème de cassis: elegante e fruttato, ora senza alcol.|Sparkling wine and crème de cassis: elegant and fruity, now alcohol-free.|990
box-regalo-0|box-espresso-martini-0|Box Espresso Martini 0%|Espresso Martini Box 0%|Il necessario per l'Espresso Martini 0% a casa: base 0%, crema al caffè 0% e ricetta, in confezione regalo.|Everything for a 0% Espresso Martini at home: 0% base, coffee cream 0% and recipe card, in a gift box.|3490
box-regalo-0|box-spritz-party-0|Box Spritz Party 0%|Spritz Party Box 0%|Per 6 persone: aperitivo 0%, spumante 0% e soda in confezione regalo.|For 6 people: 0% aperitif, 0% sparkling and soda in a gift box.|3990
box-regalo-0|box-aperitivo-italiano-0|Box Aperitivo Italiano 0%|Italian Aperitivo Box 0%|Spritz, Americano e Bitter Soda 0% in una scatola: l'aperitivo italiano da regalare.|Spritz, Americano and Bitter Soda 0% in one box: the Italian aperitivo to give as a gift.|3490
box-regalo-0|box-dry-january-0|Box Dry January 0%||Un mese senza alcol con stile: 6 cocktail 0% diversi da provare, con le schede ricetta.|A month without alcohol in style: 6 different 0% cocktails to try, with recipe cards.|4490
box-regalo-0|box-natale-bollicine-0|Box Natale Bollicine 0%|Christmas Sparkling Box 0%|Spumante 0%, Bellini 0% e Vin Brulé 0% in una confezione natalizia.|Sparkling 0%, Bellini 0% and Mulled Wine 0% in a Christmas gift box.|4990
box-regalo-0|box-mixology-starter-0|Box Mixology Starter 0%||Il kit per iniziare a miscelare analcolici: 3 distillati 0%, tonic e guida ai cocktail.|The starter kit for non-alcoholic mixology: 3 spirits 0%, tonic and a cocktail guide.|5490
martini-dessert-0|pornstar-martini-0|Pornstar Martini 0%||Frutto della passione, vaniglia e bollicine: uno dei cocktail più cercati online, ora 0%.|Passion fruit, vanilla and bubbles: one of the most searched cocktails online, now 0%.|990
martini-dessert-0|french-martini-0|French Martini 0%||Ananas e lampone con un tocco di vaniglia: fruttato e vellutato, ora 0%.|Pineapple and raspberry with a touch of vanilla: fruity and velvety, now 0%.|990
martini-dessert-0|cosmopolitan-0|Cosmopolitan 0%||Mirtillo rosso, lime e arancia: il cocktail rosa icona degli anni Novanta, ora 0%.|Cranberry, lime and orange: the iconic pink cocktail of the nineties, now 0%.|990
martini-dessert-0|lychee-martini-0|Lychee Martini 0%||Litchi, lime e un velo di rosa: delicato e profumato, ora 0%.|Lychee, lime and a hint of rose: delicate and fragrant, now 0%.|990
martini-dessert-0|tiramisu-martini-0|Tiramisù Martini 0%||Caffè, mascarpone e cacao in un bicchiere: il dessert italiano in forma di cocktail, 0%.|Coffee, mascarpone and cocoa in a glass: the Italian dessert as a cocktail, 0%.|990
martini-dessert-0|white-russian-0|White Russian 0%||Caffè, crema e ghiaccio: il classico cremoso da fine serata, ora 0%.|Coffee, cream and ice: the creamy late-night classic, now 0%.|990
aperitivi-0|negroni-sbagliato-0|Negroni Sbagliato 0%||Bitter, vermouth rosso e spumante: lo sbaglio più famoso di Milano, ora 0%.|Bitter, red vermouth and sparkling wine: Milan's most famous mistake, now 0%.|990
aperitivi-0|bitter-soda-0|Bitter Soda 0%||Bitter rosso e soda ghiacciata: l'aperitivo da bar italiano più semplice, ora 0%.|Red bitter and ice-cold soda: the simplest Italian bar aperitivo, now 0%.|990
aperitivi-0|limoncello-spritz-0|Limoncello Spritz 0%||Limoncello 0%, spumante e soda: fresco e agrumato, lo spritz del sud Italia.|Limoncello 0%, sparkling wine and soda: fresh and citrusy, the southern Italian spritz.|990
aperitivi-0|spritz-bianco-0|Spritz Bianco 0%|White Spritz 0%|Vermouth bianco, spumante e soda con fetta di limone: lo spritz chiaro e leggero, ora 0%.|White vermouth, sparkling wine and soda with a lemon slice: the light, pale spritz, now 0%.|990
aperitivi-0|bitter-orange-0|Bitter Orange 0%||Bitter e succo d'arancia: dolce-amaro, colorato, perfetto prima di cena, ora 0%.|Bitter and orange juice: bittersweet, colorful, perfect before dinner, now 0%.|990
distillati-0|whisky-sour-0|Whisky Sour 0%||Whisky 0%, limone e zucchero con schiuma vellutata: il sour più amato, ora 0%.|Whisky 0%, lemon and sugar with a velvety foam: the best-loved sour, now 0%.|990
distillati-0|boulevardier-0|Boulevardier 0%||Whisky 0%, bitter e vermouth rosso: il cugino scuro del Negroni, ora 0%.|Whisky 0%, bitter and red vermouth: the Negroni's darker cousin, now 0%.|990
distillati-0|sazerac-0|Sazerac 0%||Rye 0%, zucchero, bitter e scorza di limone: il cocktail storico di New Orleans, ora 0%.|Rye 0%, sugar, bitters and lemon peel: the historic New Orleans cocktail, now 0%.|990
distillati-0|gimlet-0|Gimlet 0%||Gin 0% e lime: secco, pulito e tagliente, ora 0%.|Gin 0% and lime: dry, clean and sharp, now 0%.|990
distillati-0|gin-martini-dry-0|Gin Martini Dry 0%||Gin 0% e vermouth secco con oliva o limone: il Martini classico, ora 0%.|Gin 0% and dry vermouth with olive or lemon: the classic Martini, now 0%.|990
tropicali-0|caipirinha-0|Caipirinha 0%||Lime pestato, zucchero di canna e cachaça 0%: il cocktail brasiliano, ora 0%.|Muddled lime, cane sugar and cachaça 0%: the Brazilian cocktail, now 0%.|990
tropicali-0|caipiroska-0|Caipiroska 0%||Lime pestato, zucchero e vodka 0%: la variante fresca e secca, ora 0%.|Muddled lime, sugar and vodka 0%: the fresh, dry variation, now 0%.|990
tropicali-0|sex-on-the-beach-0|Sex on the Beach 0%||Pesca, arancia e mirtillo rosso: dolce, fruttato e colorato, ora 0%.|Peach, orange and cranberry: sweet, fruity and colorful, now 0%.|990
tropicali-0|blue-lagoon-0|Blue Lagoon 0%||Blu curaçao, limonata e ghiaccio: blu elettrico e rinfrescante, ora 0%.|Blue curaçao, lemonade and ice: electric blue and refreshing, now 0%.|990
tropicali-0|singapore-sling-0|Singapore Sling 0%||Gin 0%, ciliegia, ananas e lime: il classico tiki di Singapore, ora 0%.|Gin 0%, cherry, pineapple and lime: the Singapore tiki classic, now 0%.|990
tropicali-0|hurricane-0|Hurricane 0%||Rum 0%, frutto della passione e lime: il cocktail di New Orleans, ora 0%.|Rum 0%, passion fruit and lime: the New Orleans cocktail, now 0%.|990
long-drink-0|tom-collins-0|Tom Collins 0%||Gin 0%, limone, zucchero e soda: alto, frizzante e rinfrescante, ora 0%.|Gin 0%, lemon, sugar and soda: tall, fizzy and refreshing, now 0%.|990
long-drink-0|gin-fizz-0|Gin Fizz 0%||Gin 0%, limone e soda: leggero e frizzante, il classico senza tempo, ora 0%.|Gin 0%, lemon and soda: light and fizzy, the timeless classic, now 0%.|990
long-drink-0|cape-codder-0|Cape Codder 0%||Vodka 0%, mirtillo rosso e lime: semplice, rosso e rinfrescante, ora 0%.|Vodka 0%, cranberry and lime: simple, red and refreshing, now 0%.|990
long-drink-0|sea-breeze-0|Sea Breeze 0%||Vodka 0%, mirtillo rosso e pompelmo: fresco, rosato e estivo, ora 0%.|Vodka 0%, cranberry and grapefruit: fresh, pink and summery, now 0%.|990
liquori-0|anisetta-0|Anisetta 0%||Anice e finocchietto delicati, dolce e fresca: perfetta ghiacciata o nel caffè.|Delicate anise and fennel, sweet and fresh: perfect ice-cold or in coffee.|1290
liquori-0|genepi-0|Genepì 0%||Erbe alpine e artemisia in infusione: balsamico, verde, tipico di montagna.|Infused alpine herbs and artemisia: balsamic, green, typical of the mountains.|1290
liquori-0|liquore-nocciole-0|Liquore alle Nocciole 0%|Hazelnut Liqueur 0%|Nocciole tostate e cacao: dolce e avvolgente, per dessert e cocktail.|Toasted hazelnuts and cocoa: sweet and rounded, for desserts and cocktails.|1290
liquori-0|liquore-ciliegia-0|Liquore di Ciliegia 0%|Cherry Liqueur 0%|Ciliegie nere e mandorla: dolce e intenso, per dolci e cocktail.|Black cherries and almond: sweet and intense, for desserts and cocktails.|1290
vino-0|vino-rosso-0|Vino Rosso 0%|Red Wine 0%|Frutti rossi, tannino morbido e spezie: il rosso da tavola, senza alcol.|Red fruit, soft tannins and spice: the table red, without alcohol.|890
vino-0|vino-bianco-0|Vino Bianco 0%|White Wine 0%|Agrumi e fiori bianchi, fresco: il bianco da aperitivo e da pesce, senza alcol.|Citrus and white flowers, fresh: the white for aperitivo and fish, without alcohol.|890
vino-0|vino-rosato-0|Vino Rosato 0%|Rosé Wine 0%|Fragola, petali di rosa e freschezza: il rosato dell'estate, senza alcol.|Strawberry, rose petals and freshness: the summer rosé, without alcohol.|890
vino-0|vin-brule-0|Vin Brulé 0%|Mulled Wine 0%|Cannella, chiodi di garofano e scorza d'arancia da servire caldo: il Natale, senza alcol.|Cinnamon, cloves and orange peel served hot: Christmas, without alcohol.|790
vino-0|sangria-0|Sangria 0%||Frutta fresca, spezie e agrumi: la sangria da condividere, senza alcol.|Fresh fruit, spices and citrus: the sangria to share, without alcohol.|790
mixer-0|tonic-premium|Tonic Premium||Acqua tonica con chinino e botanici: la base del Gin Tonic perfetto.|Tonic water with quinine and botanicals: the base of the perfect Gin Tonic.|390
mixer-0|ginger-beer|Ginger Beer||Zenzero piccante e frizzante: per Moscow Mule, Dark & Stormy e long drink.|Spicy, fizzy ginger: for Moscow Mule, Dark & Stormy and long drinks.|390
mixer-0|soda-limone|Soda al Limone|Lemon Soda|Soda leggera con limone vero: per spritz e long drink.|Light soda with real lemon: for spritz and long drinks.|350
mixer-0|sciroppo-spritz|Sciroppo Spritz|Spritz Syrup|Concentrato per preparare lo spritz 0% in un attimo: arancia amara e botanici.|Concentrate to make a 0% spritz in a moment: bitter orange and botanicals.|690"""
def w(rel, txt):
    p = os.path.join(R, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, 'w', encoding='utf-8', newline='\n').write(txt)
def fm(**k):
    return '---\n' + ''.join('%s: %s\n' % (a, json.dumps(b, ensure_ascii=False) if isinstance(b, str) and a in ('title', 'description', 'seo_title', 'seo_description') else b) for a, b in k.items()) + '---\n'
def sh(*a): return subprocess.run(['git', '-C', R, *a], capture_output=True, text=True, encoding='utf-8', errors='replace')

def main():
    cp = os.path.join(R, '_data', 'catalogo.json'); raw = open(cp, encoding='utf-8-sig').read(); c = json.loads(raw)
    ind = len(re.match(r'\{\n( *)', raw).group(1)) or 2
    for l in CATS.split('\n'):
        cid, n, ne, sl, ic, di, de, sti, ste = l.split('|')
        if not [x for x in c['categorie'] if x['id'] == cid]:
            c['categorie'].append(dict(id=cid, nome=n, icona=ic, descrizione=di, immagine='', tr=dict(en=dict(nome=ne, descrizione=de))))
        w('_negozio/categoria-%s.md' % cid, fm(layout='negozio-categoria', title=n, cid=cid, ref='shop-cat-' + cid, permalink='/negozio/categoria/%s/' % cid, description=di, seo_title=sti, seo_description=di))
        w('en/negozio/categoria/%s.md' % cid, fm(layout='negozio-categoria', title=ne, cid=cid, permalink='/en/shop/category/%s/' % sl, description=de, seo_title=ste, seo_description=de, lang='en', locale='en', ref='shop-cat-' + cid, tr='tradotto'))
    icone = {x['id']: x.get('icona', '') for x in c['categorie']}
    nuovi = 0
    for l in P.split('\n'):
        cid, i, n, ne, di, de, pr = l.split('|'); ne = ne or n
        old = [x for x in c['prodotti'] if x['id'] == i]
        new = dict(tipo='fisico', id=i, nome=n, categoria=cid, prezzo_centesimi=int(pr), descrizione=di, descrizione_completa=di,
                   immagine=old[0].get('immagine', '') if old else '', icona=icone.get(cid, ''), visibile=True, tr=dict(en=dict(descrizione=de, descrizione_completa=de)))
        if ne != n: new['tr']['en']['nome'] = ne
        if old: c['prodotti'][c['prodotti'].index(old[0])] = new
        else: c['prodotti'].append(new); nuovi += 1
        w('_negozio/%s.md' % i, fm(layout='negozio-prodotto', title=n, pid=i, permalink='/negozio/%s/' % i, description='%s: %s' % (n, di), seo_title='%s Analcolico' % n, seo_description='%s: %s' % (n, di), ref='shop-prod-' + i))
        w('en/negozio/%s.md' % i, fm(layout='negozio-prodotto', title=ne, pid=i, permalink='/en/shop/%s/' % i, description='%s: %s' % (ne, de), seo_title='Non-Alcoholic %s' % ne, seo_description='%s: %s' % (ne, de), lang='en', locale='en', ref='shop-prod-' + i, tr='tradotto'))
    open(cp, 'w', encoding='utf-8', newline='\n').write(json.dumps(c, ensure_ascii=False, indent=ind) + ('\n' if raw.endswith('\n') else ''))
    print('categorie:', len(c['categorie']), '| prodotti:', len(c['prodotti']), '| nuovi:', nuovi)
    if '--no-push' not in sys.argv:
        sh('add', '_data/catalogo.json', '_negozio', 'en/negozio', 'automation/aggiungi_catalogo.py')
        print(sh('commit', '-q', '-m', 'Passata 1: 5 categorie nuove e %d prodotti nuovi (senza foto)' % nuovi).stderr[-200:])
        sh('pull', '-q', '--rebase'); print(sh('push').stderr[-200:]); print('push ok')

if __name__ == '__main__':
    main()
