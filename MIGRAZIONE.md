# MIGRAZIONE analcolici3 (CartaCMS) -> questa repo

Sito di origine: https://cartacms.ipermark.com/analcolici3/it/ (brand "Spirito Libero", aperitivi e cocktail analcolici 0%, formato 1L, 9,90 euro a bottiglia).
Obiettivo: copiare TUTTO (home, pagine, categorie shop, prodotti, categorie blog, articoli, menu, footer, colori, immagini) in questo clone di mistraltemplate1. Si segue la procedura "migrazione pelletteria -> pelletteria2" in `CLAUDE.md`.

## Dove sta il lavoro (fuori dalla repo, NON pubblico)
- Cartella di lavoro: `C:\Users\mirco\Desktop\claudetemp\migra_analcolici\`
  - `export.py` = scarica da CartaCMS (sola lettura) categorie, elenchi, menu, footer, tema, pagine
  - `export2.py` = scarica il dettaglio di tutti i prodotti e articoli
  - `export\*.json` = i dati scaricati (origine dei dati per i build)
- Il token API di analcolici3 NON va mai scritto qui (la repo e' pubblica): gli script lo leggono da `claudetemp\tmp\list_cats_analcolici3.py`. Modulo API: `Desktop\cartacms.ipermark.com\cartacms\pyton\cartacms_tools.py`.

## Contenuto del sito di origine (verificato 31/10/2026)
- Solo italiano: la versione EN esiste nel menu ma categorie, prodotti e articoli EN sono vuoti (0). Le pagine EN rispondono ma non sono tradotte.
- 4 categorie shop: aperitivi-0, long-drink-0, tropicali-0, distillati-0 (con titolo, seo, immagine og, descrizione).
- 40 prodotti, tutti a 9,90 euro, tipo fisico, stato published, con immagine og_image su cartacms.ipermark.com/analcolici3/assets/uploads/...
- 4 categorie blog: guide-aperitivo, wellness-detox, trend-cultura, ricette-mocktail.
- 13 articoli (guide e ricette mocktail, luglio 2026), ciascuno con corpo HTML, seo e immagine di copertina.
- Pagine: home, about, contact, blog (corpo HTML a blocchi con `<style>` inline).
- Menu: Home, Shop, Blog, Chi siamo, Contatti. Footer: Privacy, Cookie, Contatti (link vuoti).
- Nota: nella home di origine i pulsanti e le categorie puntano ancora a `/analcolici2/` (residuo di clonazione): nel nuovo sito vanno rifatti i link.

## STATO (aggiornare a ogni passo)
- [x] 31/10 Repo creata da mistraltemplate1 (`nuovo_sito.ps1 -Brand "Spirito Libero"`), online su https://cialdecompatibili-netizen.github.io/analcolici/
- [x] 31/10 Fase 1: esportati in JSON categorie shop/blog, elenchi, menu, footer, css tema, pagine home/about/contact/blog
- [x] 31/10 Fase 1b: scaricato il dettaglio di 40 prodotti e 13 articoli (`export\prodotti_full_it.json`, `articoli_full_it.json`)
- [ ] Fase 2: scaricare le immagini (prodotti, categorie, articoli) in `assets/images/` della repo (le url puntano al vecchio sito)
- [ ] Fase 3: `_data/tema.json` (colori dal css del vecchio sito), logo e texture hero (`automation/genera_logo.py`, `genera_texture.py`)
- [ ] Fase 4: `ecommerce: true`, `_data/catalogo.json` (prezzi in centesimi: 990) + `_negozio/` categorie e prodotti (ref `shop-cat-<id>` e `shop-prod-<id>`)
- [ ] Fase 5: blog: categorie (`_data/categorie.json`) + `_posts/` con 13 articoli, poi `python automation/permalink_articoli.py --apply`
- [ ] Fase 6: home, chi siamo, contatti, menu (`navigation.yml`), footer, privacy/cookie
- [ ] Fase 7: togliere i segnaposto del template (articoli `*-prova`/`*-test`, categoria e prodotto di esempio, `_pages/servizi.md`)
- [ ] Fase 8: traduzioni EN (da decidere se tenerle), `python automation/allinea_hash.py en`
- [ ] Fase 9: `_config.yml` (description, email, whatsapp, contact_endpoint), commit e push con `..\pubblica.ps1 -Files ...`, verifica online

## Regole per questa migrazione
- Generare tutto con script (node o python), mai a mano: accenti e apostrofi nei blocchi come entita' HTML, JSON con rilettura.
- Non portare i `<style>` del vecchio sito: usare le classi `gc-*` / `ent-*` e `_data/tema.json`.
- Dati e testi solo quelli dell'origine, niente invenzioni.
