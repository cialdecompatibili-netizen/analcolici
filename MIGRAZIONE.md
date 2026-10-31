# MIGRAZIONE analcolici3 (CartaCMS) -> questa repo

Sito di origine: CartaCMS, sito `analcolici3` (indirizzo e token API: vedi `C:\Users\mirco\Desktop\claudetemp\tmp\list_cats_analcolici3.py`). Brand "Spirito Libero": aperitivi, long drink, tropicali e distillati analcolici 0%, formato 1L, 9,90 euro a bottiglia.
Obiettivo: copiare TUTTO (home, pagine, categorie shop, prodotti, categorie blog, articoli, menu, colori, immagini) in questo clone del template. Procedura generale: `CLAUDE.md` (sezione migrazione pelletteria).

## Dove sta il lavoro (fuori dalla repo, NON pubblico)
Cartella: `C:\Users\mirco\Desktop\claudetemp\migra_analcolici\`
- `export.py`, `export2.py` = scaricano da CartaCMS (sola lettura) e scrivono `export\*.json`
- `fase2_immagini.py` = scarica le immagini (JPEG max 1200px) in `assets/images/{prodotti,categorie,blog}/`, mappa in `export\immagini_map.json`
- `fase3_build.py` = costruisce tutto dalla export (catalogo, `_negozio/`, categorie blog, `_posts/`, blocchi home e chi siamo, menu, config). Si puo' rilanciare; dopo di lui va rilanciato `python automation\permalink_articoli.py --apply` (i post perdono il permalink) e vanno cancellati i file `redirect/*.html` appena creati (inutili: gli indirizzi vecchi non sono mai stati online).
- Il token API NON va scritto nella repo (e' pubblica).

## Contenuto migrato (31/10/2026)
- 4 categorie shop: aperitivi-0, long-drink-0, tropicali-0, distillati-0 (icona emoji, descrizione, immagine)
- 40 prodotti a 9,90 euro (10 per categoria), tipo fisico, con immagine, descrizione breve e completa, SEO
- 4 categorie blog: Guide all'Aperitivo, Wellness & Detox, Trend & Cultura, Ricette Mocktail
- 13 articoli (luglio 2026) con immagine di copertina (`header.teaser`) e SEO; indirizzi `/blog/<categoria>/<titolo>/`
- Home a blocchi (hero, numeri, collezioni, perche', blog, invito) e Chi siamo (3 blocchi) con i testi dell'origine
- Menu: Home, Shop, Blog, Chi siamo, Contatti. Colori: corallo #ff6b5b (accento dell'origine), logo "S", sfondo home generato.

## Scelte prese
- SOLO ITALIANO: l'origine ha il selettore EN ma nessun contenuto tradotto. Tolti `en/` e `_data/i18n/en`; `languages: [it]`. Per aggiungere l'inglese: admin > Lingue (poi tradurre).
- Dati corretti rispetto all'origine: la home origine diceva "10 ricette" e 3 collezioni (residuo di `analcolici2`); nel nuovo sito 40 ricette e 4 collezioni, link rifatti verso lo shop del nuovo sito.
- Footer: quello di default del template (credito webtomars). Il footer origine era "CartaCMS" con link vuoti: non portato.
- Contatti: pagina standard del template. L'origine aveva solo un'email segnaposto (info@esempio.it): NON portata. Il modulo resta spento finche' `contact_endpoint` e' vuoto.
- Privacy e Cookie: non esistono nell'origine (link vuoti), quindi non create.

## STATO
- [x] Repo creata da mistraltemplate1, online su https://cialdecompatibili-netizen.github.io/analcolici/
- [x] Fase 1 export JSON; Fase 1b dettaglio 40 prodotti e 13 articoli
- [x] Fase 2 immagini (61 file, circa 2 MB)
- [x] Fase 3 tema, logo, hero, catalogo, negozio, blog, home, chi siamo, menu, config; segnaposto del template tolti
- [ ] Verifica online dopo il push: home, /negozio/, una categoria, un prodotto, /blog/, un articolo, /chi-siamo/ (Mirco controlla da solo)
- [ ] Da compilare a mano: `contact_endpoint` (serve un Worker Cloudflare), `whatsapp`, `email` in `_config.yml`; pagine Privacy e Cookie
- [ ] Opzionale: lingua inglese, ordini (`ordini:` in `_config.yml`), dominio personalizzato

## Regole per questa migrazione
- Generare tutto con script, mai a mano: accenti e apostrofi nei blocchi come entita' HTML, JSON con rilettura.
- Non portare i `<style>` del vecchio sito: si usano le classi `gc-*` / `ent-*` e `_data/tema.json`.
- Dati e testi solo quelli dell'origine, niente invenzioni.

## Fase 4 (31/10/2026): inglese + marketing
- [x] Versione inglese completa: `en/` (home, shop, 4 categorie, 40 prodotti, blog 4 categorie + 13 articoli, chi siamo, contatti, carrello, ordine, grazie, filosofia). Lingue: `languages: [it, en]`. Dati EN in `_data/i18n/en/`, testi prodotti/categorie in `catalogo.json` (`tr.en`).
- Script: `claudetemp\migra_analcolici\fase4a_en.py` (struttura EN), `tr_prodotti_en.py` (traduzioni prodotti scritte a mano), `fase4b_marketing.py` (blocchi home/azienda/filosofia IT+EN, menu, config). Articoli EN tradotti con `automation/traduci_lingua.py en` (motore automatico: rileggere i testi), poi `permalink_articoli.py --apply`, cancellati `redirect/*.html`, `allinea_hash.py en`.
- [x] Marketing: blocco "Filosofia" in home (eccellenza italiana, cura, gusto) + pagina `/filosofia/` (EN `/en/philosophy/`), blocco "Come si gusta" (3 gesti), voce di menu Filosofia.
- ATTENZIONE: i testi "filosofia" sono messaggi di marca, non fatti verificati (nessun "fatto a mano in Italia" letterale: non e' nell'origine). Se vuoi dichiararlo, va confermato.
- [ ] Da rileggere a mano: traduzione automatica degli articoli EN (nomi propri, termini bar).
