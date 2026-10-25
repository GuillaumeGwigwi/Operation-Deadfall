"""Reuse the supplied Ala Harbor illustration, removing its editorial frame."""
import hashlib,json,shutil
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'sources/propositions/preludes-thay/illustrations-alaor'
item=next(i for i in json.loads((ART/'briefs-mj.json').read_text())['images'] if i['method']=='reuse')
src=ROOT/item['source_asset'];originals=ART/'sources-originales';originals.mkdir(exist_ok=True)
shutil.copy2(src,originals/src.name)
(ART/'originaux').mkdir(exist_ok=True);public=ROOT/'site/illustrations-alaor-joueurs';public.mkdir(exist_ok=True)
with Image.open(src) as source:
 source.load();crop=item['crop'];assert 0<=crop[0]<crop[2]<=source.width and 0<=crop[1]<crop[3]<=source.height
 region=source.crop(crop).convert('RGBA').convert('RGB');clean=Image.new('RGB',region.size);clean.paste(region)
 original=ART/'originaux'/(item['id']+'.png');target=public/item['player_file'];clean.save(original);clean.save(target)
with Image.open(target) as check:check.load();assert not check.info and not check.getexif()
p=ART/'generation-results-mj.json';records=json.loads(p.read_text()) if p.exists() else {}
records[item['id']]={'id':item['id'],'label':item['label'],'success':True,'method':'source-fournie-recadree','source':str(src),'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'crop':crop,'original':str(original),'player_image':str(target),'width':clean.width,'height':clean.height}
p.write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n');print(json.dumps(records[item['id']],ensure_ascii=False))
