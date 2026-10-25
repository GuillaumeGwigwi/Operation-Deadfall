"""Retouch only Yelena's tattoos; stage for visual review before applying."""
import argparse,importlib.util,json,os,shutil,sys
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];ART=ROOT/'sources/propositions/preludes-thay/illustrations';EDITS=ART/'retouches';EDITS.mkdir(exist_ok=True)
parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');parser.add_argument('--host-model');args=parser.parse_args()
candidate=EDITS/'yelena-tatouages.png';record_file=EDITS/'yelena-tatouages-result.json';original=ART/'originaux/yelena.png'
if not args.apply:
 if candidate.exists():
  with Image.open(candidate) as im:im.verify()
  print('Candidat existant conservé : '+str(candidate));raise SystemExit(0)
 engine=Path('/home/gwi/.hermes/hermes-agent');os.environ['HERMES_HOME']='/home/gwi/.hermes/profiles/dnd-assistant';os.environ['OPENAI_IMAGE_MODEL']='gpt-image-2-high';sys.path.insert(0,str(engine))
 spec=importlib.util.spec_from_file_location('dnd_yelena_edit',engine/'plugins/image_gen/openai-codex/__init__.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 if args.host_model:module._CODEX_CHAT_MODEL=args.host_model
 provider=module.OpenAICodexImageGenProvider()
 prompt='''Edit the supplied portrait, do not create a different portrait. Keep exactly the same human woman, facial identity, age, shaved head, expression, gaze, pose, anatomy of both hands, red robe, chair, table, window, lighting, painterly rendering, parchment background, soft brush edges and portrait composition. Add the missing distinctive tattoos of a Red Wizard of Thay. Clearly visible refined dark charcoal-black ink tattoos on the shaved scalp and forehead, flowing onto BOTH temples and the visible cheekbones in elegant asymmetric geometric arcane linework. Add related clearly visible tattoo patterns on the backs of BOTH exposed hands and visible skin at the wrists, following anatomy naturally. Her sleeves stay intact: do not expose or invent bare forearms. These are permanent ink markings, not makeup, shadow, jewelry, glowing magic, scars or burns. The marks should be unmistakable at book illustration size while leaving the face recognizable and expressive, the eyes and lips uncovered. Do not use a specific faction emblem, skull, bell, readable text or story-revealing symbol. No added character, object, finger or limb. Only change the bare skin by adding the tattoos. Retain the original image dimensions and all other features.'''
 result=provider.generate(prompt=prompt,aspect_ratio='portrait',image_url=str(original))
 if isinstance(result,str):result=json.loads(result)
 record={k:v for k,v in result.items() if k!='prompt'};record.update(edit_of=str(original),prompt=prompt,host_model=args.host_model or module._CODEX_CHAT_MODEL)
 if result.get('success'):
  shutil.copy2(result['image'],candidate)
  with Image.open(candidate) as im:im.verify()
  record['candidate']=str(candidate)
 record_file.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in record.items() if k!='prompt'},ensure_ascii=False),flush=True)
 if not result.get('success'):raise SystemExit('Retouche échouée ; aucun portrait livré n’a été modifié.')
else:
 record=json.loads(record_file.read_text());assert record.get('success') and candidate.exists()
 backup=EDITS/'yelena-avant-tatouages.png'
 if not backup.exists():shutil.copy2(original,backup)
 manifest=ART/'generation-results-mj.json';records=json.loads(manifest.read_text())
 prior=EDITS/'generation-results-avant-tatouages.json'
 if not prior.exists():shutil.copy2(manifest,prior)
 with Image.open(candidate) as im:
  im.load();assert im.width*3==im.height*2,(im.width,im.height)
  clean=Image.new('RGB',im.size);clean.paste(im.convert('RGB'));public=ROOT/'site/illustrations-cavernes-joueurs/02-portrait.png';clean.save(public,format='PNG')
 shutil.copy2(candidate,original)
 updated={k:v for k,v in record.items() if k!='prompt'};updated.update(id='yelena',label='Yelena Voss',original=str(original),player_image=str(public),width=clean.width,height=clean.height,edit='Ajout des tatouages sur crâne, visage et mains, conformément à la correction du MJ.')
 records['yelena']=updated;manifest.write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 with Image.open(public) as im:assert not im.info and not im.getexif()
 print('Portrait retouché appliqué ; copie joueurs sans métadonnées : '+str(public))
