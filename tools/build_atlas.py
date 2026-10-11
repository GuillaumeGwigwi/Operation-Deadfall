#!/usr/bin/env python3
"""Construit site/index.html avec toutes ses ressources embarquées."""
import base64
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'sources/site/atlas'
OUTPUT=ROOT/'site/index.html'

def data_uri(path):
    return 'data:image/jpeg;base64,'+base64.b64encode(path.read_bytes()).decode('ascii')

def main():
    html=(SOURCE/'index.template.html').read_text()
    css=(SOURCE/'atlas.css').read_text()
    code=(SOURCE/'atlas.js').read_text()
    data=json.loads((SOURCE/'atlas-data.js').read_text().removeprefix('window.THAY_ATLAS = ').strip().removesuffix(';'))
    assert '</style' not in css.lower() and '</script' not in code.lower()
    assert not re.search(r'@import|url\(',css), 'Nouvelle ressource CSS : intégrer avant de distribuer'
    images={}
    for place in data['landmarks']:
        if place.get('image'):
            relative=Path(place['image'])
            assert relative.parts[0]=='assets' and '..' not in relative.parts
            key=relative.stem
            images.setdefault(key,data_uri(SOURCE/relative))
            place['image']=key
    data.pop('map',None)  # L’image de fond est embarquée une seule fois dans le HTML.
    data['embeddedImages']=images
    payload=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    data_tag='<script id="atlas-public-data" type="application/json">'+payload+'</script>'
    boot='window.THAY_ATLAS = JSON.parse(document.getElementById("atlas-public-data").textContent);\n'
    boot+='window.THAY_ATLAS.map = document.getElementById("map-image").src;\n'
    boot+='for (const place of window.THAY_ATLAS.landmarks) { if (place.image) place.image = window.THAY_ATLAS.embeddedImages[place.image]; }'
    assert html.count('<link rel="stylesheet" href="atlas.css">')==1
    html=html.replace('<link rel="stylesheet" href="atlas.css">','<style>\n'+css+'\n</style>')
    assert html.count('src="assets/thay-joueurs.jpg"')==1
    html=html.replace('src="assets/thay-joueurs.jpg"','src="'+data_uri(SOURCE/'assets/thay-joueurs.jpg')+'"')
    assert html.count('<script src="atlas-data.js"></script>')==1
    html=html.replace('<script src="atlas-data.js"></script>',data_tag+'\n<script>\n'+boot+'\n</script>')
    assert html.count('<script src="atlas.js"></script>')==1
    html=html.replace('<script src="atlas.js"></script>','<script>\n'+code+'\n</script>')
    assert '<script src=' not in html and 'href="atlas.css"' not in html
    assert 'assets/' not in html
    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    OUTPUT.write_text(html)
    print(f'HTML autonome généré : {OUTPUT}')
    print(f'{len(data["landmarks"])} notices ; {len(images)+1} images embarquées ; {OUTPUT.stat().st_size} octets')
if __name__=='__main__': main()
