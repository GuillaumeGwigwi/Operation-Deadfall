"""Aggregate actual Alaor art, placements, integrity and PDF review images."""
import hashlib,json
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
import pypdfium2 as pdfium
ROOT=Path(__file__).resolve().parents[1];ART=ROOT/'sources/propositions/preludes-thay/illustrations-alaor';OUT=ROOT/'sources/site/preludes/verification/alaor-illustre';OUT.mkdir(exist_ok=True)
briefs=json.loads((ART/'briefs-mj.json').read_text());items=briefs['images'];records=json.loads((ART/'generation-results-mj.json').read_text());baseline=json.loads((ART/'archives/avant-illustrations/baseline.json').read_text())
assert len(items)==len({i['id'] for i in items})==14
for name,digest in baseline['cavernes'].items():assert hashlib.sha256((ROOT/'site'/name).read_bytes()).hexdigest()==digest
spec=next(s for s in json.loads((ROOT/'sources/site/preludes/rendered.json').read_text()) if s['id']=='alaor')
assert ' '.join(BeautifulSoup(spec['html'],'html.parser').stripped_strings)==baseline['alaor_text']
data=json.loads(BeautifulSoup((ROOT/'site/prelude-dragon-d-alaor-mj.html').read_text(),'html.parser').select_one('#prelude-data').string)
placements={}
for n,html in enumerate(data['documents'][0]['pages'],1):
 for img in BeautifulSoup(html,'html.parser').select('img'):
  label=img['alt'];assert label not in placements;placements[label]=n
assert len(placements)==14
rows=[];hashes=set()
for item in items:
 rec=records[item['id']];assert rec['success']
 path=ROOT/'site/illustrations-alaor-joueurs'/item['player_file']
 with Image.open(path) as im:im.load();assert not im.info and not im.getexif();size=im.size
 digest=hashlib.sha256(path.read_bytes()).hexdigest();assert digest not in hashes;hashes.add(digest)
 rows.append({'id':item['id'],'label':item['label'],'page':placements[item['label']],'file':item['player_file'],'pixels':size,'method':rec.get('method',rec.get('model')),'sha256':digest})
report={'images':rows,'count':len(rows),'generated':sum(i.get('method')!='reuse' for i in items),'reused':sum(i.get('method')=='reuse' for i in items),'pages':len(data['documents'][0]['pages']),'rooms':sum(e['kind']=='room' for e in data['entries']),'story_exactly_preserved':True,'cavernes_deliveries_unchanged':True,'metadata_clean':True,'files':{name:{'bytes':(ROOT/'site'/name).stat().st_size,'megabytes':round((ROOT/'site'/name).stat().st_size/1000000,1)} for name in ['prelude-dragon-d-alaor-mj.html','prelude-dragon-d-alaor-mj.pdf']}}
assert report['generated']==13 and report['reused']==1 and report['rooms']==39
(ART/'verification-mj.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
lines=['# Illustrations du Dragon d’Alaor — revue MJ','',f"Livre : {report['pages']} pages, {report['count']} illustrations ({report['reused']} image fournie, {report['generated']} créations). Récit et trente-neuf repères conservés. Les livraisons des Cavernes restent strictement identiques.",'','| Sujet | Page | Copie seule |','|---|---:|---|']
lines += [f"| {r['label']} | {r['page']} | {r['file']} |" for r in rows]
lines += ['','Les copies seules ne contiennent ni ce tableau, ni brief, ni métadonnées. À montrer uniquement lors de la rencontre ou découverte correspondante, pas en galerie anticipée. Le livre, le présent rapport et les manifestes restent MJ.','',"Source du port : illustration 01-007.ala-harbor-merchants.png du chapitre Thay fourni par le MJ, recadrée pour retirer le cadre éditorial. Original conservé inchangé. Les autres images sont générées, pas des portraits officiels. Les détails physiques non précisés par la source restent des propositions artistiques.",'',"Les fonds d’Ashlyn, Devi, Anish, de l’atelier et des joueurs de cartes ont été corrigés pour fermer des vues extérieures non décrites. Les figures et objets sont conservés. Aucun visuel ne dévoile la présence de Veen invisible, le poison, les pouvoirs des urnes ou la vraie nature des gardes. La canne d’Anish apparaît sculptée, pas transformée.",'',"Les images de lieux ne sont pas des plans exacts. Les cartes originales et les profils signalés dans l’annexe restent nécessaires ; aucune règle ni caractéristique n’a été inventée pour remplacer une lacune.",'']
(ART/'revue-mj.md').write_text('\n'.join(lines),encoding='utf-8')
pdf=pdfium.PdfDocument(ROOT/'site/prelude-dragon-d-alaor-mj.pdf');assert len(pdf)==report['pages']
for pattern,prefix in [('page[0-9][0-9][0-9].png','page'),('planche-[0-9][0-9].png','planche-')]:
 for old in OUT.glob(pattern):
  if int(old.stem.removeprefix(prefix))>len(pdf):old.unlink()
for i in range(len(pdf)):pdf[i].render(scale=100/72).to_pil().save(OUT/f'page{i+1:03}.png')
for start in range(1,len(pdf)+1,4):
 canvas=Image.new('RGB',(1200,1560),'#e8e4d9')
 for k,n in enumerate(range(start,min(start+4,len(pdf)+1))):
  im=Image.open(OUT/f'page{n:03}.png').convert('RGB');im.thumbnail((600,780));canvas.paste(im,((k%2)*600,(k//2)*780))
 canvas.save(OUT/f'planche-{start:02}.png')
print(json.dumps(report,ensure_ascii=False,indent=2));print('Rendus PDF et planches : '+str(OUT))
