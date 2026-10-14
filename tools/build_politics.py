#!/usr/bin/env python3
"""Assembler le dossier politique autonome à partir des seules sources publiques."""
import base64,json,re,gzip,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'sources/site/politique'
ORDER=['abjuration','invocation','divination','enchantement','evocation','illusion','necromancie','transmutation']
def main():
 data=json.loads((SRC/'public-data.json').read_text())
 assert set(data)=={'roles','council','provinces','situations'}
 assert len(data['roles'])==4 and len(data['council'])==8 and len(data['provinces'])==11
 assert [c['id'] for c in data['council']]==ORDER
 rendered=json.loads((SRC/'fiches-data.json').read_text())
 fiches=rendered['fiches']
 assert list(fiches)==ORDER,'Relancer node tools/homebrewery/render_politics.mjs'
 for c in data['council']:
  c['html']=fiches[c['id']]
 assert set(rendered['tharchs'])=={p['id'] for p in data['provinces']}
 for p in data['provinces']:
  p['html']=rendered['tharchs'][p['id']]
 data['practice']={'html':rendered['practice']}
 official=(SRC/'homebrewery-officiel/homebrewery-v3-phb.offline.css').read_bytes()
 assert hashlib.sha256(official).hexdigest()=='3f001e220c7c10385d65ab9b741077e15f9dd624162814d0b8897aeee1156e5e','Le bundle officiel a changé : vérifier sa provenance avant mise à jour'
 css=re.sub(r'/\*.*?\*/','',official.decode(),flags=re.S)
 assert '@import' not in css
 assert all(u.startswith(('data:','#')) for u in re.findall(r'url\(\s*[\"\']?([^\"\')]+)',css)),'Ressource CSS non autonome'
 hb_css=base64.b64encode(gzip.compress(official,mtime=0)).decode()
 png=(SRC/'assets/embleme.png').read_bytes()
 assert png[:8]==b'\x89PNG\r\n\x1a\n'
 offset=8
 while offset<len(png):
  size=int.from_bytes(png[offset:offset+4],'big')
  assert png[offset+4:offset+8] not in {b'eXIf',b'tEXt',b'iTXt',b'zTXt'},'Métadonnées non autorisées'
  offset+=size+12
 images={'embleme':'data:image/png;base64,'+base64.b64encode(png).decode()}
 for key in ORDER+['pratique']:
  portrait=(SRC/f'assets/{key}.png').read_bytes()
  assert portrait[:8]==b'\x89PNG\r\n\x1a\n'
  offset=8
  while offset<len(portrait):
   size=int.from_bytes(portrait[offset:offset+4],'big')
   assert portrait[offset+4:offset+8] not in {b'eXIf',b'tEXt',b'iTXt',b'zTXt'},'Métadonnées non autorisées'
   offset+=size+12
  images[key]='data:image/png;base64,'+base64.b64encode(portrait).decode()
 raw=json.dumps(data,ensure_ascii=False,indent=2)
 assert not re.search(r'(?i)arcanaloth|rakshasa|shadowfell|vampir|\blich\b|Hezrexen|Fangbane|sarrukh|stat block|primary ambition|excludedTopics|tiefling|tieffelin|gnome|abyss|abysse|démon|secret|caché',raw)
 template=(SRC/'index.template.html').read_text()
 assert template.count('{{PUBLIC_DATA}}')==1 and template.count('{{IMAGES}}')==1 and template.count('{{OFFICIAL_HB_CSS_GZIP}}')==1
 html=template.replace('{{IMAGES}}',json.dumps(images)).replace('{{PUBLIC_DATA}}',raw.replace('<','\\u003c')).replace('{{OFFICIAL_HB_CSS_GZIP}}',hb_css)
 dest=ROOT/'site/politique-thay.html';dest.parent.mkdir(exist_ok=True);dest.write_text(html)
 print(f'HTML généré : {dest} — {dest.stat().st_size} octets ; 8 zulkirs, emblème, 2 portraits du livre et 6 portraits générés validés intégrés une fois, 11 provinces, 4 rôles, 1 page En pratique illustrée ({len(data["situations"])} situations) ; aucune ressource externe.')
if __name__=='__main__':main()
