#!/usr/bin/env python3
"""Applique les ancres revues sur la carte originale aux données d’édition."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'sources/site/atlas'

def main():
 ref=json.loads((SOURCE/'positions.json').read_text())
 assert hashlib.sha256((SOURCE/'assets/thay-joueurs.jpg').read_bytes()).hexdigest()==ref['imageSHA256'], 'La carte a changé : revoir les ancres avant application'
 path=SOURCE/'atlas-data.js'
 data=json.loads(path.read_text().removeprefix('window.THAY_ATLAS = ').strip().removesuffix(';'))
 points={p['id']:p for p in data['landmarks']}
 assert set(points)=={a['id'] for a in ref['anchors']}
 assert (data['mapWidth'],data['mapHeight'])==(ref['width'],ref['height'])
 for a in ref['anchors']:
  p=points[a['id']]; x,y=a['pixel']
  p['x']=round(x/ref['width']*100,6)
  p['y']=round(y/ref['height']*100,6)
 path.write_text('window.THAY_ATLAS = '+json.dumps(data,ensure_ascii=False,indent=2)+';\n')
 print(f'{len(points)} coordonnées appliquées depuis le relevé vérifié.')
if __name__=='__main__': main()
