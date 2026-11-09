"""Private visual specimens: book / native engine / actual guide."""
from pathlib import Path
import shutil,json,hashlib
from PIL import Image,ImageDraw
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'sources/propositions/politique-thay-mj/recherche-style/typographie';OUT.mkdir(exist_ok=True)
for n in [10,43,53]:shutil.copy2(f'/tmp/dnd-table-page-{n}.png',OUT/f'wotc-basic2014-p{n}.png')
with sync_playwright() as p:
 exe=next(Path('/home/gwi/.cache/ms-playwright').glob('chromium-*/**/chrome'))
 b=p.chromium.launch(headless=True,executable_path=str(exe));page=b.new_page(viewport={'width':1100,'height':1250})
 page.goto((OUT/'homebrewery-composants.html').as_uri());page.evaluate('document.fonts.ready');page.locator('.page').screenshot(path=str(OUT/'homebrewery-composants.png'));b.close()
# Compare actual typography, not differently scaled entire pages.
source=Image.open(OUT/'wotc-basic2014-p43.png');hb=Image.open(OUT/'homebrewery-composants.png')
guide=Image.open(ROOT/'sources/site/politique/verification/council-composition/abjuration.png')
examples=[('Wizards 2014 - p.43',source.crop((90,650,440,790))),('Homebrewery - composant natif',hb.crop((68,48,398,190))),('Guide Thay - tableau corrige',guide.crop((68,115,398,210)))]
canvas=Image.new('RGB',(1320,300),'white');draw=ImageDraw.Draw(canvas)
for i,(label,im) in enumerate(examples):
 draw.text((i*440+12,12),label,fill='black');im.thumbnail((418,240));canvas.paste(im,(i*440+12,45))
canvas.save(OUT/'comparaison-tableaux.png')
manifest={'book':'https://media.wizards.com/2014/downloads/dnd/PlayerDnDBasicRules_v0.2.pdf','pdf_pages_inspected':[10,43,53],'native_component':'https://github.com/naturalcrit/homebrewery/blob/master/themes/V3/Blank/snippets.js','notes':'Table title h5; distinct th; text left, numeric columns according to semantics. Book and engine are distinct sources.','official_css_sha256':hashlib.sha256((ROOT/'sources/site/politique/homebrewery-officiel/homebrewery-v3-phb.offline.css').read_bytes()).hexdigest()}
(OUT/'sources.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(OUT/'comparaison-tableaux.png')
