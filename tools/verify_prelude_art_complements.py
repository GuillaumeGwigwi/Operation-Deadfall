"""Verify the ten art additions against their actual files and prior manuscript."""
import hashlib,json,re
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'sources/propositions/preludes-thay/illustrations'
BASE=ART/'archives/avant-complements'
brief=json.loads((ART/'briefs-complements-mj.json').read_text())
items=brief['images'];keys=[i['id'] for i in items]
assert len(keys)==len(set(keys))==10
manifest=json.loads((ART/'generation-results-mj.json').read_text())
source=(ART.parent/'01-les-cavernes-du-chaos.homebrewery.md').read_text()
old=(BASE/'manuscrit.homebrewery.md').read_text()
pattern=r'^\{\{(?:wide|block)\n<img src="illustrations/incrustees/(?:'+ '|'.join(map(re.escape,keys))+r')\.webp"[^\n]*>\n\}\}\n\n'
unchanged,n=re.subn(pattern,'',source,flags=re.M)
assert n==10 and unchanged==old, 'Le récit doit rester strictement identique hors des dix images ajoutées'
preserved=[]
for folder,files in json.loads((BASE/'empreintes.json').read_text()).items():
 for filename,expected in files.items():
  actual=hashlib.sha256((ART/folder/filename).read_bytes()).hexdigest()
  assert actual==expected, f'Illustration antérieure modifiée : {folder}/{filename}'
  preserved.append(f'{folder}/{filename}')
soup=BeautifulSoup((ROOT/'site/prelude-cavernes-du-chaos-mj.html').read_text(),'html.parser')
data=json.loads(soup.select_one('#prelude-data').string)
placements=[]
for page,html in enumerate(data['documents'][0]['pages'],1):
 for image in BeautifulSoup(html,'html.parser').select('img'):
  assert image['src'].startswith('data:image/webp;base64,')
  placements.append({'page':page,'label':image.get('alt')})
assert len(placements)==15
for item in items:
 record=manifest[item['id']]
 assert record['success'] and Path(record['original']).is_file()
 target=ROOT/'site/illustrations-cavernes-joueurs'/item['player_file']
 assert target.resolve()==Path(record['player_image']).resolve()
 with Image.open(target) as image:
  image.load();assert not image.info and not image.getexif()
 assert sum(p['label']==item['label'] for p in placements)==1
report={'ten_requested_images':len(items),'embedded_images':len(placements),'pages':len(data['documents'][0]['pages']),'story_exactly_preserved':True,'previous_files_unchanged':preserved,'player_copies_metadata_free':True,'placements':placements}
(ART/'verification-complements-mj.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
