"""Stage faithful background corrections without changing foreground characters."""
import argparse,concurrent.futures,importlib.util,json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];ART=ROOT/'sources/propositions/preludes-thay/illustrations-alaor';OUT=ART/'retouches-fonds';OUT.mkdir(exist_ok=True)
ENGINE=Path('/home/gwi/.hermes/hermes-agent');os.environ['HERMES_HOME']='/home/gwi/.hermes/profiles/dnd-assistant';os.environ['OPENAI_IMAGE_MODEL']='gpt-image-2-high';sys.path.insert(0,str(ENGINE))
spec=importlib.util.spec_from_file_location('alaor_retouch_provider',ENGINE/'plugins/image_gen/openai-codex/__init__.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);module._CODEX_CHAT_MODEL='gpt-6.1-sol';provider=module.OpenAICodexImageGenProvider()
items=json.loads((ART/'briefs-mj.json').read_text())['images'];byid={i['id']:i for i in items}
parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');args=parser.parse_args()
keys=['ala-ashlyn','ala-devi','ala-anish','ala-atelier','ala-cartes']
if args.apply:
 import shutil
 from PIL import Image
 p=ART/'generation-results-mj.json';records=json.loads(p.read_text());backup=OUT/'avant';backup.mkdir(exist_ok=True)
 for key in keys:
  stage=OUT/(key+'.png');assert stage.is_file()
  original=ART/'originaux'/(key+'.png');saved=backup/(key+'.png')
  if not saved.exists():shutil.copy2(original,saved)
  shutil.copy2(stage,original)
  with Image.open(stage) as im:
   im.load();clean=Image.new('RGB',im.size);clean.paste(im.convert('RGB'));target=ROOT/'site/illustrations-alaor-joueurs'/byid[key]['player_file'];clean.save(target)
  records[key].update(original=str(original),player_image=str(target),width=clean.width,height=clean.height,background_correction='Ouvertures extérieures non décrites fermées, figures conservées')
 p.write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n');print('Cinq fonds corrigés appliqués ; copies joueurs recréées sans métadonnées.')
else:
 def run(key):
  import shutil
  target=OUT/(key+'.png')
  if target.exists():print('Conservé : '+key,flush=True);return
  item=byid[key]
  prompt='Edit the supplied painting in place. This is a precise BACKGROUND-ONLY correction for a faithful tabletop adventure. Preserve the exact foreground character identities, species, age, faces, hair, poses, hands, fingers, clothing, objects, activities, existing brushwork, framing, canvas orientation and parchment-faded edges. Do NOT redesign, recast or beautify the people. The room is an interior carved from solid stone to resemble modest masonry. Remove ALL background openings or windows that show sea, sky, distant cliffs, an outside harbor or distant buildings; these rooms have no such exterior opening in the described adventure. Replace those areas with a continuous plain stone interior wall in the same palette and painterly style, NO new door, window, framed landscape, picture, secret seam or tunnel. Preserve the warm ambient light as artistic illumination and retain any existing hooded lantern. No words, logo, magic, extra person or architectural escape route. Preserve all foreground objects, especially the loom and wool in the workshop, cards and beds in the two-men scene, the snake-headed wooden cane and goat statue in Anish portrait, the sending stone with Devi, and Ashlyn pale blue skin. Keep the same illustration rather than making a new one.'
  result=provider.generate(prompt=prompt,aspect_ratio=item['aspect'],reference_image_urls=[str(ART/'originaux'/(key+'.png'))])
  if isinstance(result,str):result=json.loads(result)
  assert result.get('success'),result
  shutil.copy2(result['image'],target);(OUT/(key+'.json')).write_text(json.dumps({k:v for k,v in result.items() if k!='prompt'},ensure_ascii=False,indent=2)+'\n');print('Retouche prête : '+key,flush=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(run,keys))
