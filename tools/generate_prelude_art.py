"""Generate requested prelude artwork using the existing Hermes provider.
Never modifies provider code or Hermes configuration. Original outputs stay MJ-only.
"""
import argparse,concurrent.futures,importlib.util,json,os,shutil,sys,threading
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
PROFILE=Path('/home/gwi/.hermes/profiles/dnd-assistant')
ENGINE=Path('/home/gwi/.hermes/hermes-agent')
parser=argparse.ArgumentParser();parser.add_argument('--only');parser.add_argument('--host-model');parser.add_argument('--art-dir',default='sources/propositions/preludes-thay/illustrations');parser.add_argument('--player-dir',default='site/illustrations-cavernes-joueurs');parser.add_argument('--brief-file',default='briefs-mj.json');parser.add_argument('--quality',choices=['low','medium','high'],default='high');args=parser.parse_args()
ART=(ROOT/args.art_dir).resolve();PUBLIC=(ROOT/args.player_dir).resolve()
if not ART.is_relative_to(ROOT/'sources/propositions/preludes-thay') or not PUBLIC.is_relative_to(ROOT/'site'):raise ValueError('Répertoires privés et de livraison hors périmètre')
os.environ['HERMES_HOME']=str(PROFILE)
os.environ['OPENAI_IMAGE_MODEL']='gpt-image-2-'+args.quality
sys.path.insert(0,str(ENGINE))
spec=importlib.util.spec_from_file_location('dnd_codex_image_provider',ENGINE/'plugins/image_gen/openai-codex/__init__.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
if args.host_model:module._CODEX_CHAT_MODEL=args.host_model
provider=module.OpenAICodexImageGenProvider()
if not provider.is_available():raise SystemExit('Fournisseur Codex indisponible : vérifier authentification existante ou dépendances, sans créer de nouvelle configuration.')
briefs=json.loads((ART/args.brief_file).read_text());manifest=ART/'generation-results-mj.json'
results=json.loads(manifest.read_text()) if manifest.exists() else {}
lock=threading.Lock();PUBLIC.mkdir(parents=True,exist_ok=True);(ART/'originaux').mkdir(exist_ok=True)
PUBLIC_NAMES={'village':'01-village.png','yelena':'02-portrait.png','vinx':'03-portrait.png','ravin':'04-paysage.png','oggdug':'05-portrait.png'}
def verify(path):
 if not path.exists():return False
 try:
  with Image.open(path) as im:im.verify()
  return True
 except Exception:return False
def run(item):
 key=item['id'];previous=results.get(key,{})
 if previous.get('success') and verify(Path(previous.get('original',''))) and verify(Path(previous.get('player_image',''))):
  print('Conservé : '+item['label'],flush=True);return previous
 if item.get('method')=='reuse':raise ValueError('Préparer cette illustration fournie avant le lot : '+item['label'])
 public_name=item.get('player_file',PUBLIC_NAMES.get(key))
 if not public_name or Path(public_name).name!=public_name or not public_name.endswith('.png'):raise ValueError('Nom de copie joueurs invalide')
 print('Génération : '+item['label'],flush=True)
 canvas='VERTICAL 2:3 character portrait canvas, not a horizontal scene.' if item['aspect']=='portrait' else 'HORIZONTAL panoramic scene canvas.'
 result=provider.generate(prompt=briefs['common']+'\n\n'+canvas+'\n\n'+item['prompt'],aspect_ratio=item['aspect'],reference_image_urls=[str(ROOT/item['reference'])])
 if isinstance(result,str):result=json.loads(result)
 record={k:v for k,v in result.items() if k!='prompt'};record['id']=key;record['label']=item['label'];record['host_model']=args.host_model or module._CODEX_CHAT_MODEL
 if result.get('success'):
  src=Path(result['image']);original=ART/'originaux'/(key+'.png');shutil.copy2(src,original)
  with Image.open(src) as im:
   im.load();clean=Image.new('RGB',im.size);clean.paste(im.convert('RGB'))
   target=PUBLIC/public_name;clean.save(target,format='PNG')
   record.update(original=str(original),player_image=str(target),width=clean.width,height=clean.height)
  with Image.open(target) as im:assert not im.info and not im.getexif()
 with lock:
  results[key]=record;tmp=manifest.with_suffix('.tmp');tmp.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');tmp.replace(manifest)
 print(json.dumps(record,ensure_ascii=False),flush=True);return record
selected=[x for x in briefs['images'] if not args.only or x['id']==args.only]
if not selected:raise SystemExit('Illustration inconnue')
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(run,selected))
if any(not results[x['id']].get('success') for x in selected):raise SystemExit('Génération incomplète ; résultats réels conservés dans generation-results-mj.json')
print('VÉRIFIÉ : '+str(len(selected))+' illustration(s), fichiers lisibles et copies joueurs sans métadonnées.',flush=True)
