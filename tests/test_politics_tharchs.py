import asyncio,json,re,tempfile,shutil,unittest,base64,gzip,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
IDS=['alaor','delhumide','eltabbar','gauros','lapendrar','priador','pyarados','surthay','thaymount','thazalhar','tyraturos']
class TharchData(unittest.TestCase):
 def test_official_homebrewery_styles_are_preserved(self):
  h=(ROOT/'site/politique-thay.html').read_text()
  encoded=re.search(r'<script id="official-hb-style" type="text/plain">(.*?)</script>',h,re.S).group(1)
  css=gzip.decompress(base64.b64decode(encoded))
  self.assertEqual(hashlib.sha256(css).hexdigest(),'3f001e220c7c10385d65ab9b741077e15f9dd624162814d0b8897aeee1156e5e')
  self.assertTrue(css==(ROOT/'sources/site/politique/homebrewery-officiel/homebrewery-v3-phb.offline.css').read_bytes())
 def test_all_provinces_have_specific_fiches(self):
  h=(ROOT/'site/politique-thay.html').read_text()
  d=json.loads(re.search(r'<script id="politics-data" type="application/json">(.*?)</script>',h,re.S).group(1))
  self.assertEqual([p.get('id') for p in d['provinces']],IDS)
  for p in d['provinces']:
   self.assertRegex(p['html'],r'^(?:<div class="wide">)?<h1>'+re.escape(p['name'])+r'</h1>')
   self.assertTrue(p['ruler'] in p['html'] and p['capital'] in p['html'],p['name'])
   self.assertFalse('Le Conseil nomme' in p['html'],p['name'])
   public_text=re.sub(r'data:image/[^;]+;base64,[A-Za-z0-9+/=]+','',p['html'])
   self.assertFalse(re.search(r'(?i)Fangbane|Vrill|sarrukh|Malefice Mortum|Hezrexen|pots-de-vin|brib|vampir|attaque prochaine',public_text),p['name'])
async def browser():
 from playwright.async_api import async_playwright
 with tempfile.TemporaryDirectory(prefix='tharchs-') as tmp:
  f=Path(tmp)/'dossier.html';shutil.copy2(ROOT/'site/politique-thay.html',f)
  async with async_playwright() as p:
   exe=next(Path('/home/gwi/.cache/ms-playwright').glob('chromium-*/**/chrome'))
   b=await p.chromium.launch(executable_path=str(exe),headless=True,args=['--no-sandbox'])
   for width,height in [(1440,1000),(390,844)]:
    page=await b.new_page(viewport={'width':width,'height':height});errors=[];requests=[]
    page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:requests.append(r.url))
    await page.goto(f.as_uri()+'#provinces')
    cards=page.locator('button.province-card');assert await cards.count()==11
    for i,id in enumerate(IDS):
     card=cards.nth(i);assert await card.get_attribute('data-tharch')==id
     name=await card.locator('h3').inner_text();await card.click()
     assert await page.locator('#tharch-reader').evaluate('d=>d.open')
     assert await page.locator('#tharch-title').inner_text()==name
     assert await page.locator('#tharch-pos').inner_text()==f'{i+1} / 11'
     body=page.frame_locator('#tharch-frame').locator('.page').first;await body.wait_for()
     await page.wait_for_function('(name)=>document.getElementById("tharch-frame").contentDocument?.querySelector(".page h1")?.textContent===name',arg=name)
     assert name in await body.inner_text()
     assert await body.locator('.note').count()==0
     assert await body.locator('table').count()==1
     assert await body.locator('table tbody tr').count()==3
     computed=await body.evaluate("async el=>{await el.ownerDocument.fonts.ready;return {font:getComputedStyle(el).fontFamily,columns:getComputedStyle(el).columnCount,fonts:[...el.ownerDocument.fonts].filter(f=>f.status==='loaded').length}}")
     assert 'BookInsanity' in computed['font'] and computed['columns']=='2' and computed['fonts']>=2,computed
     await page.keyboard.press('Escape');await page.wait_for_function('(id)=>document.activeElement.dataset.tharch===id',arg=id)
    await page.locator('#province-search').fill('Ozgund');assert await page.locator('button.province-card:visible').count()==1
    await page.locator('button.province-card:visible').click();await page.locator('#tharch-next').click()
    assert await page.locator('#tharch-title').inner_text()=='Lapendrar'
    await page.locator('#tharch-close').click();await page.wait_for_function("!document.getElementById('tharch-reader').open && document.activeElement.dataset.tharch==='gauros'")
    await page.locator('#province-search').fill('');await cards.first.click()
    await page.locator('#tharch-prev').click();assert await page.locator('#tharch-title').inner_text()=='Tyraturos'
    await page.locator('#tharch-next').click();assert await page.locator('#tharch-title').inner_text()=='Alaor'
    body=page.frame_locator('#tharch-frame').locator('.page').first
    await page.wait_for_function("document.getElementById('tharch-frame').contentDocument?.querySelector('.page h1')?.textContent==='Alaor'")
    await body.evaluate('async el=>{await el.ownerDocument.fonts.ready}')
    await page.wait_for_function("document.getElementById('tharch-viewport').getBoundingClientRect().width<=document.getElementById('tharch-scroll').clientWidth+1")
    assert await page.locator('#tharch-scroll').evaluate('el=>el.scrollWidth<=el.clientWidth+1')
    await page.locator('#tharch-zoom').click();assert await page.locator('#tharch-zoom').get_attribute('aria-pressed')=='true'
    await page.locator('#tharch-zoom').click();assert await page.locator('#tharch-zoom').get_attribute('aria-pressed')=='false'
    assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
    for key in ['Tab']*7+['Shift+Tab']*7:
     await page.keyboard.press(key)
     assert await page.evaluate("document.getElementById('tharch-reader').contains(document.activeElement)")
    await page.screenshot(path=f'/tmp/thay-tharch-reader-{width}.png')
    await page.locator('#tharch-close').click();await page.locator('#province-search').fill('')
    await page.screenshot(path=f'/tmp/thay-tharch-gallery-{width}.png',full_page=True)
    assert not errors,errors;assert all(u.startswith(f.as_uri()) or u.startswith('data:') for u in requests),requests
    await page.close()
   await b.close();print('PASS : 11 fiches provinciales PC/mobile, contenu spécifique, recherche, navigation, clavier, retour du focus et HTML isolé sans réseau.')
if __name__=='__main__':
 r=unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(TharchData))
 if not r.wasSuccessful():raise SystemExit(1)
 asyncio.run(browser())
