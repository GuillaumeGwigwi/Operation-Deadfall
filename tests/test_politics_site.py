import asyncio,json,re,shutil,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SITE=ROOT/'site/politique-thay.html'
class PublicPolitics(unittest.TestCase):
 def test_public_content(self):
  self.assertTrue(SITE.is_file(),'Le second HTML autonome doit exister')
  h=SITE.read_text();d=json.loads(re.search(r'<script id="politics-data" type="application/json">(.*?)</script>',h,re.S).group(1))
  self.assertEqual(len(d['council']),8);self.assertEqual(len(d['provinces']),11);self.assertEqual(len(d['roles']),4)
  self.assertEqual(len({x['name'] for x in d['council']}),8)
  self.assertNotRegex(h,r'(?i)arcanaloth|rakshasa|shadowfell|vampir|\blich\b|Hezrexen|Fangbane|sarrukh|Primary Ambition|Stat Block|neutral evil|chaotic evil|dndbeyond|excludedTopics')
  self.assertNotRegex(h,r'(?:src|href)=[\"\'](?:https?://|assets/|\.\./)')
async def browser_test():
 from playwright.async_api import async_playwright
 with tempfile.TemporaryDirectory(prefix='thay-politics-') as t:
  path=Path(t)/'dossier.html';shutil.copy2(SITE,path)
  async with async_playwright() as p:
   exe=next(Path('/home/gwi/.cache/ms-playwright').glob('chromium-*/**/chrome'))
   b=await p.chromium.launch(executable_path=str(exe),headless=True,args=['--no-sandbox'])
   page=await b.new_page(viewport={'width':1440,'height':1000});errors=[];requests=[]
   page.on('pageerror',lambda e:errors.append(str(e)));page.on('request',lambda r:requests.append(r.url))
   await page.goto(path.as_uri());await page.locator('#role-title').wait_for()
   await page.locator('[data-role="autharchs"]').click();assert 'Autharchs' in await page.locator('#role-title').inner_text()
   for role in ['conseil','tharchions','autharchs','rouges']:
    await page.locator(f'[data-role="{role}"]').click()
    assert await page.locator(f'[data-role="{role}"]').get_attribute('aria-pressed')=='true'
    assert await page.locator('#role-body').inner_text()
   for section in ['conseil','provinces','lois','pratique','pouvoir']:
    await page.locator(f'[data-section="{section}"]').click();assert await page.locator('#'+section).is_visible()
   await page.locator('[data-section="conseil"]').click();assert await page.locator('.council-card').count()==8
   await page.locator('.council-card').first.click();assert await page.locator('.council-card').first.get_attribute('aria-expanded')=='true'
   for card in (await page.locator('.council-card').all())[1:]:
    await card.click();assert await card.get_attribute('aria-expanded')=='true'
    assert await card.locator('.detail').is_visible()
   await page.locator('[data-section="provinces"]').click();assert await page.locator('.province-card').count()==11
   await page.locator('#province-search').fill('Xelnene');assert await page.locator('.province-card:visible').count()==1
   await page.locator('#province-search').fill('zzzz');assert await page.locator('#no-results').is_visible()
   await page.locator('#province-search').fill('');assert await page.locator('.province-card:visible').count()==11
   await page.locator('[data-section="pratique"]').click();await page.locator('#situation').select_option('contradiction');assert 'haut placé' in await page.locator('#situation-result').inner_text()
   for id in ['local','peage','contradiction','eltabbar','enclave']:
    await page.locator('#situation').select_option(id)
    assert await page.locator('#situation-result p').inner_text()
   await page.locator('[data-section="pouvoir"]').click();await page.screenshot(path='/tmp/thay-politique-desktop.png',full_page=True)
   await page.set_viewport_size({'width':390,'height':844});await page.locator('[data-section="conseil"]').click();await page.screenshot(path='/tmp/thay-politique-mobile.png',full_page=True)
   for section in ['pouvoir','provinces','lois','pratique','conseil']:
    await page.locator(f'[data-section="{section}"]').click()
    assert await page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),section
   await page.locator('[data-section="pouvoir"]').click();await page.locator('[data-role="rouges"]').focus();await page.keyboard.press('Enter');assert 'Magiciens Rouges' in await page.locator('#role-title').inner_text()
   await page.goto(path.as_uri()+'#lois');assert await page.locator('#lois').is_visible()
   await page.goto(path.as_uri()+'#inconnu');assert await page.locator('#pouvoir').is_visible()
   assert not errors,errors;assert all(u.startswith(path.as_uri()) or u.startswith('data:') for u in requests),requests
   print('PASS : organigramme, 8 zulkirs, 11 provinces, recherche, situations, clavier, mobile, liens profonds ; HTML isolé sans ressources externes ni erreurs JS.')
   await b.close()
if __name__=='__main__':
 result=unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(PublicPolitics))
 if not result.wasSuccessful():raise SystemExit(1)
 asyncio.run(browser_test())
