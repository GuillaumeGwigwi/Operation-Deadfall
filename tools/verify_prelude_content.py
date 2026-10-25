"""Check final source coverage and lossless book composition."""
import hashlib,json,re
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
RAW={'cavernes':('sources/raw/chaos-caves/chaos-caves.html',64,r'[A-K]\d+'),'alaor':('sources/raw/dragon-delves-the-dragon-of-najkir/dragon-of-najkir.html',39,r'M\d+')}
def text(s):return re.sub(r'\s+',' ',BeautifulSoup(s,'html.parser').get_text(' ',strip=True)).strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
reports=[]
for spec in json.loads((ROOT/'sources/site/preludes/rendered.json').read_text()):
 source=ROOT/'sources/propositions/preludes-thay'/spec['source'];raw_path,count,pattern=RAW[spec['id']]
 raw=ROOT/raw_path;soup=BeautifulSoup(raw.read_bytes(),'html.parser');expected=set()
 for h in soup.select('h1,h2,h3,h4,h5,h6'):
  label=(h.select_one('.entry-title-inner') or h).get_text(' ',strip=True);match=re.match('('+pattern+r'): ',label)
  if match:expected.add(match.group(1))
 assert len(expected)==count,(spec['id'],expected)
 found=re.findall(r'^### .*\(('+pattern+r')\)$',source.read_text(),re.M)
 assert len(found)==count and set(found)==expected,(spec['id'],found)
 target=ROOT/'site'/spec['file'];page=BeautifulSoup(target.read_text(),'html.parser');data=json.loads(page.select_one('#prelude-data').string)
 assert data['source_sha256']==sha(source)
 assert len(data['documents'])==1
 assert text(spec['html'])==text(' '.join(data['documents'][0]['pages'])),spec['id']
 assert set(e['key'] for e in data['entries'] if e['kind']=='room')==expected
 assert not any(old in source.read_text() for old in ['Relève Noire','Cloche Creuse','noms effacés','Carrières du Serment'])
 reports.append({'source':str(source),'source_sha256':sha(source),'original':str(raw),'original_sha256':sha(raw),'html':str(target),'html_sha256':sha(target),'locations':count,'no_missing_locations':True,'no_duplicate_locations':True,'lossless_rendered_text':True,'continuous_books':1,'pages':len(data['documents'][0]['pages']),'audience':'MJ','proposal_not_canon':True,'mechanical_balance_guaranteed':False})
report={'books':reports,'total_locations':sum(r['locations'] for r in reports),'limits':['Profils référencés ou particuliers à préparer depuis les ressources autorisées.','Annexe A des récompenses des Cavernes manquante.','Cartes et illustrations référencées dans les HTML originaux non récupérées ; les nouvelles illustrations ne remplacent pas les plans.','Durée réelle et composition du groupe non confirmées.']}
path=ROOT/'sources/propositions/preludes-thay/verification.json';path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
