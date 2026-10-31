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


## SISTEMA RIUSABILE PER ALTRI SITI (appunti 31/10/2026) - "il sistema perfetto"
Tutto quello che e' stato messo a punto su analcolici e vale per ogni nuovo sito clonato da mistraltemplate1. Mirco: "lo riutilizziamo su altri siti". Regola d'oro: Claude fa tutto da solo con Desktop Commander, senza chiedere cosa cliccare.

### 1) Foto automatiche (Gemini, senza Chrome ne server)
- Strumento universale: `C:\Users\mirco\Desktop\gemini_auto\img.py` (guida completa `gemini_auto\IMMAGINI_API.md`). Parla direttamente con Gemini col login Google salvato, 10-20 s a immagine, circa 3 crediti ciascuna (600 per finestra di 5 ore). Crediti: `python img.py --crediti`.
- Il PROFILO lo sceglie Claude da solo: `prodotto` (1:1, sfondo bianco #FFFFFF, soggetto all'80%, webp 1000/500/200), `categoria` (1:1), `blog` (16:9), `banner` (21:9), `generico`. I profili sono in `gemini_auto\profili\*.md`.
- Prodotti di un sito: metti nel `_data/catalogo.json` il prodotto con `"immagine": ""`, poi UN comando:
  `python C:\Users\mirco\Desktop\gemini_auto\core\foto_sito.py --repo C:\Users\mirco\Desktop\repository\<repo> --api`
  Fa foto, le copia in `assets/images/prodotti/<id>.webp`, aggiorna il catalogo, commit e push. Opzioni: `--ids a,b` (rifa solo quelli), `--extra "testo"`, `--dry`, `--no-push`, `--rielabora` (rifa sfondo/ritaglio senza Gemini). Doppio clic: `gemini_api_test\foto_prodotti.bat`.
- Colore del liquido per i prompt: `_data/colori_foto.json` (un id per riga). Va compilato per ogni nuovo prodotto.
- Foto blog: `python ...\img.py "<soggetto>" --profilo blog --nome <slug-articolo> --out <repo>\assets\images\blog` (esce webp; i vecchi articoli hanno jpg, funziona uguale).
- TRUCCO ANTI-INVENZIONI: Gemini inventa marche e scritte storpiate (visto: "Casa Agave", "Solstice", "NON-ALCOHOLIC" sbagliato). Rifare con `--extra "The label must contain ONLY the product name. No brand name, no other words, no small print, no logos."`. Guardare SEMPRE la foto prima di dire "fatto".
- Sfondo: deve essere bianco puro #FFFFFF (solo ombra leggera ammessa); bottiglia all'80% del quadrato. Se esce grigio/piccola: `--rielabora`.
- Secondo account Gemini (piu' crediti): `gemini_auto\loginsecondoaccount.bat` + `SECONDO_ACCOUNT.md`. Da finire: leggere i cookie del 2o profilo e passare in automatico sotto 10 crediti.

### 2) Nuovo prodotto in un negozio (ricetta usata per Tequila Tonic 0%)
1. Aggiungi la voce in `_data/catalogo.json` (nome, categoria, prezzo, descrizione IT + `tr.en`, SEO, `"immagine": ""`).
2. Crea le due pagine: `_negozio/<id>.md` (IT) e `en/negozio/<id>.md` (permalink `/en/shop/<id>/`), con `ref: shop-prod-<id>` in entrambe.
3. Compila `colori_foto.json`, lancia `foto_sito.py --api`, guarda la foto, ritocca con `--ids ... --extra ...` se serve.
4. Aggiorna i numeri in home e filosofia ("46 ricette" ecc.): sono testo fisso nei blocchi, NON si aggiornano da soli (a 48 prodotti erano ancora vecchi).
5. Per varianti "best seller": cercare sul web le classifiche reali, evitare i doppioni gia' nel catalogo, descrizione, consiglio di servizio e SEO unici per ogni variante.

### 3) Nuovo articolo di blog IT + EN (ricetta Frutti Rossi Fizz)
1. Cerca sul web le ricette reali di riferimento e prendi solo lo schema comune: la ricetta resta originale, mai copiata.
2. Foto con profilo `blog` in `assets/images/blog/<slug>.webp`, guardarla prima.
3. Articolo IT in `_posts/AAAA-MM-GG-<slug>.md` + EN in `en/_posts/` con stesso `ref:`.
4. `python automation/permalink_articoli.py --apply`, poi `python automation/allinea_hash.py en`.
5. Pubblica con `..\pubblica.ps1 -Repo <repo> -Msg "..." -Files ...` (oppure git add/commit/push), controlla IT, EN e la categoria online. Online ci mette 1-2 minuti.
- Accenti: i nuovi articoli usano gli accenti veri (e, piu); i vecchi hanno "e'" e "piu'". Uniformare solo se Mirco lo chiede.

### 4) SEO title: NON mettere il nome del sito nel `seo_title`
- `_includes/seo.html` compone `<title>` = `seo_title - nome sito`. Se nel `seo_title` c'e' gia' "| Spirito Libero" il nome esce DOPPIO.
- Fatto il 31/10/2026: tolto il suffisso da 133 file (IT+EN, _negozio, _posts, filosofia, categorie), commit 60ab276. Controllo veloce su qualsiasi sito: `git grep -n -I -E "seo_title:.*\|"`. Quando si genera contenuto con script, il `seo_title` deve essere SOLO il titolo.
- Regola identica per i prodotti/articoli nuovi: titolo breve e unico, senza nome sito.

### 5) Cose da ricordare quando si migra un sito da CartaCMS
- Export in sola lettura via API, dati fuori dalla repo (e' pubblica), token mai scritto in repo. Script in `claudetemp\migra_analcolici\` (export.py, export2.py, fase4a_en.py, tr_prodotti_en.py, fase4b_marketing.py).
- Testi "marketing/filosofia": solo messaggi di marca, NON dichiarazioni verificabili ("handmade in Italy" non c'e' nell'origine: non scriverlo senza conferma di Mirco).
- Traduzione automatica articoli EN (`traduci_lingua.py en`) sbaglia termini bar e nomi propri (es. "Spirito Libero" -> "Free Spirit", "Garnish" -> "Gasket"): rileggere sempre.

### 6) Stato a fine sessione (31/10/2026)
- [x] Online IT + EN: negozio 48 prodotti (con foto), blog 14 articoli, filosofia, home marketing, seo_title puliti.
- [ ] Controllo a occhio di Mirco: foto tequila (sfondo, dimensioni), lightbox, scheda EN, traduzioni articoli EN.
- [ ] Aggiornare i numeri in home/filosofia (48 prodotti) se vogliono restare corretti.
- [ ] Mancano `contact_endpoint`, `whatsapp`, `email` in `_config.yml`; pagine Privacy e Cookie.
- [ ] Opzionale: altre varianti stesso trattamento per gin, rum, ecc.; altre ricette agrumata/tropicale; accenti vecchi articoli.
