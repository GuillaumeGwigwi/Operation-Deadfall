"""Génération privée des six portraits ; aucune modification du site joueurs."""
import concurrent.futures
import importlib.util
import json
from pathlib import Path
import sys
import threading
import shutil
from PIL import Image,ImageDraw
ROOT=Path('/home/gwi/Operation-Deadfall')
DEST=ROOT/'sources/propositions/portraits-zulkirs-mj'
ENGINE=Path('/home/gwi/.hermes/hermes-agent')
sys.path.insert(0,str(ENGINE))
spec=importlib.util.spec_from_file_location('codex_image_backend',ENGINE/'plugins/image_gen/openai-codex/__init__.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
# Le modèle hôte actuel est celui de cette session, sans modifier Hermes.
module._CODEX_CHAT_MODEL='gpt-6.1-sol'
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--only')
args=parser.parse_args()
provider=module.OpenAICodexImageGenProvider()
if not provider.is_available():
    raise SystemExit('Génération indisponible : authentification Codex ou dépendance manquante.')
briefs=json.loads((DEST/'briefs.json').read_text())
reference=str(ROOT/briefs['reference_image'])
results_path=DEST/'generation-results.json'
lock=threading.Lock()
results={}
if results_path.exists():
    results=json.loads(results_path.read_text())
def generate(item):
    ident=item['id']
    if results.get(ident,{}).get('success') and Path(results[ident]['portrait']).is_file():
        return results[ident]
    print('Génération : '+item['name'],flush=True)
    response=provider.generate(briefs['common_prompt']+'\n\n'+item['brief'],aspect_ratio='portrait',reference_image_urls=[reference])
    record={k:v for k,v in response.items() if k not in {'prompt'}}
    record['name']=item['name']
    if response.get('success'):
        source=Path(response['image'])
        if not source.is_file():
            raise RuntimeError('Sortie du générateur absente : '+str(source))
        raw=DEST/'originaux'/f'{ident}.png'
        raw.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(source,raw)
        target=DEST/'portraits'/f'{ident}.png'
        target.parent.mkdir(parents=True,exist_ok=True)
        with Image.open(raw) as original:
            original.verify()
        with Image.open(raw) as original:
            converted=original.convert('RGB')
            converted.thumbnail((800,1200),Image.Resampling.LANCZOS)
            clean=Image.frombytes('RGB',converted.size,converted.tobytes())
            clean.save(target,format='PNG',optimize=True)
        with Image.open(target) as final:
            assert not final.info and not final.getexif()
            record.update(portrait=str(target),original=str(raw),width=final.width,height=final.height,bytes=target.stat().st_size)
    with lock:
        results[ident]=record
        temp=results_path.with_suffix('.tmp')
        temp.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
        temp.replace(results_path)
    print(json.dumps(record,ensure_ascii=False),flush=True)
    return record
selected=[p for p in briefs['portraits'] if not args.only or p['id']==args.only]
if not selected:
    raise SystemExit('Identifiant de portrait inconnu')
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    list(pool.map(generate,selected))
if args.only:
    raise SystemExit(0 if results[args.only].get('success') else 1)
expected={p['id'] for p in briefs['portraits']}
if set(results)!=expected or any(not results[k].get('success') for k in expected):
    raise SystemExit('Génération incomplète : consulter generation-results.json')
board=Image.new('RGB',(1080,1080),'#232629')
draw=ImageDraw.Draw(board)
for i,item in enumerate(briefs['portraits']):
    im=Image.open(results[item['id']]['portrait'])
    im.thumbnail((340,490),Image.Resampling.LANCZOS)
    x=(i%3)*360+(360-im.width)//2
    y=(i//3)*540
    board.paste(im,(x,y))
    draw.text(((i%3)*360+16,y+505),item['name'],fill='#e8e0d2')
board.save(DEST/'planche-contact.jpg',quality=90)
print('VÉRIFIÉ : six portraits générés, fichiers lisibles sans métadonnées ; planche-contact.jpg créée.',flush=True)
