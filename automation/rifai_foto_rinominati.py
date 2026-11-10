# Dopo il reset crediti Gemini (03:31): rifa le foto dei 5 prodotti rinominati (la vecchia etichetta riporta ancora il vecchio nome con marchio)
# e riattiva i 3 nascosti (aperol/crodino/select) solo se la foto nuova e' stata creata. Uso, dalla radice: python automation/rifai_foto_rinominati.py
import io, os, subprocess, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IDS = ['aperol-style-spritz-0', 'crodino-style-0', 'select-spritz-0', 'dark-stormy-0', 'painkiller-0']
NASCOSTI = IDS[:3]
FOTO = r'C:\Users\mirco\Desktop\gemini_auto\core\foto_sito.py'
subprocess.run([sys.executable, FOTO, '--repo', R, '--api', '--ids', ','.join(IDS)], cwd=os.path.dirname(FOTO))
p = os.path.join(R, '_data', 'catalogo.json')
s = io.open(p, 'r', encoding='utf-8', newline='').read(); fatti = []
for pid in NASCOSTI:
    i = s.find('"id": "%s"' % pid); j = s.find('"visibile": false', i); k = s.find('"immagine": "', i)
    img = s[k + 13:s.find('"', k + 13)] if k > 0 else ''
    if i >= 0 and 0 < j - i < 3000 and img.endswith('.webp'):
        s = s[:j] + '"visibile": true' + s[j + len('"visibile": false'):]; fatti.append(pid)
if fatti:
    io.open(p, 'w', encoding='utf-8', newline='').write(s)
    for c in (['git', 'add', '_data/catalogo.json'], ['git', 'commit', '-m', 'Riattivati prodotti rinominati con foto nuova'], ['git', 'push']): subprocess.run(c, cwd=R)
print('riattivati:', fatti or 'nessuno (foto non rifatte, crediti?)')
