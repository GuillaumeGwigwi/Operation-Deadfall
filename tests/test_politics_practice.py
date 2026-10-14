import asyncio,base64,gzip,hashlib,json,re,shutil,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site/politique-thay.html'
class Practice(unittest.TestCase):
 def test_one_complete_official_page(self):
  h=SITE.read_text()
  d=json.loads(re.search(r'<script id="politics-data" type="application/json">(.*?)</script>',h,re.S).group(1))
  self.assertIn('practice',d)
  self.assertTrue(d['practice']['html'].startswith('<h1>En pratique</h1>'))
  for situation in d['situations']:
   self.assertIn(situation['body'],d['practice']['html'])
  for phrase in ['Guilde du commerce extérieur','Gulga Vull','Sous l’aristocratie des Magiciens Rouges','puis les travailleurs','au-dessus de l’autorité magique']:
   self.assertIn(phrase,d['practice']['html'])
  self.assertEqual(d['practice']['html'].count('<h1>'),1)
  self.assertNotIn('id="situation"',h)
  self.assertIn('id="practice-frame"',h)
  self.assertIn('id="practice-zoom"',h)
  images=json.loads(re.search(r'<script id="politics-images" type="application/json">(.*?)</script>',h,re.S).group(1))
  self.assertTrue(images['pratique'].startswith('data:image/png;base64,'))
  raw=base64.b64decode(images['pratique'].split(',',1)[1]);offset=8
  while offset<len(raw):
   size=int.from_bytes(raw[offset:offset+4],'big')
   self.assertNotIn(raw[offset+4:offset+8],{b'eXIf',b'tEXt',b'iTXt',b'zTXt'})
   offset+=size+12
async def browser():
 from playwright.async_api import async_playwright
 with tempfile.TemporaryDirectory(prefix='practice-alone-') as temp:
  f=Path(temp)/'guide.html';shutil.copy2(SITE,f)
  async with async_playwright() as p:
   exe=next(Path('/home/gwi/.cache/ms-playwright').glob('chromium-*/**/chrome'))
   b=await p.chromium.launch(executable_path=str(exe),headless=True,args=['--no-sandbox'])
   for width,height in [(1440,1100),(390,844)]:
    page=await b.new_page(viewport={'width':width,'height':height});errors=[];requests=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('request',lambda r:requests.append(r.url))
    await page.goto(f.as_uri()+'#pratique')
    body=page.frame_locator('#practice-frame').locator('.page')
    await body.wait_for();assert await body.count()==1
    await body.evaluate('async el=>{await el.ownerDocument.fonts.ready}')
    await page.wait_for_function("document.getElementById('practice-viewport').clientHeight>0")
    assert await body.locator('h1').inner_text()=='En pratique'
    assert await body.locator('img').evaluate('i=>i.complete&&i.naturalWidth>0')
    metrics=await body.evaluate("el=>({font:getComputedStyle(el).fontFamily,columns:getComputedStyle(el).columnCount,width:el.clientWidth,height:el.clientHeight,scrollHeight:el.scrollHeight,scrollWidth:el.scrollWidth,contentBottom:Math.max(...[...el.querySelectorAll('h1,h2,p,img')].map(x=>x.getBoundingClientRect().bottom-el.getBoundingClientRect().top))})")
    assert 'BookInsanity' in metrics['font'] and metrics['columns']=='2',metrics
    assert metrics['scrollWidth']<=metrics['width']+1,metrics
    assert metrics['scrollHeight']<=metrics['height']+1,metrics
    assert metrics['contentBottom']<metrics['height']-40,metrics
    assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
    await page.screenshot(path=f'/tmp/thay-pratique-{width}.png',full_page=True)
    await page.locator('#practice-zoom').click()
    assert await page.locator('#practice-zoom').get_attribute('aria-pressed')=='true'
    assert await page.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),'Le zoom doit défiler dans son cadre, pas élargir le site'
    await page.screenshot(path=f'/tmp/thay-pratique-native-{width}.png',full_page=True)
    await page.locator('#practice-zoom').click()
    await page.locator('[data-section="conseil"]').click()
    await page.locator('[data-section="pratique"]').click()
    assert await page.locator('#practice-frame').is_visible()
    assert not errors,errors
    assert all(u.startswith(f.as_uri()) or u.startswith('data:') for u in requests),requests
    print('PASS En pratique',width,metrics)
    await page.close()
   await b.close()
if __name__=='__main__':
 r=unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(Practice))
 if not r.wasSuccessful():raise SystemExit(1)
 asyncio.run(browser())
