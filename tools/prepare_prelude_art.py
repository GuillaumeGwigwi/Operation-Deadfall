"""Prepare feathered, transparent book vignettes; never modify player originals."""
import argparse,hashlib,json,math
from pathlib import Path
from PIL import Image,ImageFilter,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--art-dir',default='sources/propositions/preludes-thay/illustrations');args=parser.parse_args()
ART=(ROOT/args.art_dir).resolve()
if not ART.is_relative_to(ROOT/'sources/propositions/preludes-thay'):raise ValueError('Répertoire d’illustrations hors périmètre')
OUT=ART/'incrustees';OUT.mkdir(exist_ok=True)
records=[];hashes=set()
brief_files=[ART/'briefs-mj.json']
if (ART/'briefs-complements-mj.json').exists():brief_files.append(ART/'briefs-complements-mj.json')
items=[item for path in brief_files for item in json.loads(path.read_text())['images']]
keys=[item['id'] for item in items];by_id={item['id']:item for item in items}
assert len(keys)==len(set(keys)), 'Identifiant d’illustration dupliqué'
for key in keys:
 src=ART/'originaux'/(key+'.png')
 with Image.open(src) as opened:
  opened.load();im=opened.convert('RGBA')
 crop=by_id[key].get('book_crop')
 if crop:
  assert 0<=crop[0]<crop[2]<=im.width and 0<=crop[1]<crop[3]<=im.height, 'Cadrage livre hors image'
  im=im.crop(crop)
 landscape=im.width>im.height
 im.thumbnail((1600,1000) if landscape else (768,1152),Image.Resampling.LANCZOS)
 mask=Image.new('L',(320,320));px=mask.load()
 for y in range(320):
  ny=y/319
  for x in range(320):
   nx=x/319
   border=min(nx/(.065 if landscape else .10),(1-nx)/(.065 if landscape else .10),ny/.07,(1-ny)/(.12 if landscape else .14))
   ripple=.11*math.sin(nx*41)*math.sin(ny*37)+.05*math.sin((nx+ny)*71)
   t=max(0,min(1,border+ripple));px[x,y]=round(255*t*t*(3-2*t))
 mask=mask.resize(im.size,Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(1))
 draw=ImageDraw.Draw(mask);draw.rectangle((0,0,im.width-1,im.height-1),outline=0,width=2)
 im.putalpha(mask);target=OUT/(key+'.webp');im.save(target,format='WEBP',quality=94,method=6)
 with Image.open(target) as check:
  check.load();assert check.getchannel('A').getextrema()==(0,255)
 digest=hashlib.sha256(target.read_bytes()).hexdigest();assert digest not in hashes;hashes.add(digest)
 record={'id':key,'image':str(target),'width':im.width,'height':im.height,'bytes':target.stat().st_size,'sha256':digest,'true_transparency':True};records.append(record);print(json.dumps(record),flush=True)
(ART/'integration-mj.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
