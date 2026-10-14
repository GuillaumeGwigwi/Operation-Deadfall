import asyncio,base64,json,re,shutil,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SITE=ROOT/'site/politique-thay.html'
FICHES=[('abjuration','Yazir Nym','Escalant'),('invocation','Nevron','invocation'),('divination','Lethnar','tribunal'),('enchantement','Delraz','taxes'),('evocation','Xelnene Thrul','Priador'),('illusion','Mythrellaa','Tour des Illusions'),('necromancie','Szass Tam','Szul'),('transmutation','Nzas','armée')]
class PublicPolitics(unittest.TestCase):
 def test_public_content(self):
  self.assertTrue(SITE.is_file(),'Le second HTML autonome doit exister')
  h=SITE.read_text();d=json.loads(re.search(r'<script id="politics-data" type="application/json">(.*?)</script>',h,re.S).group(1))
  # Le bloc CSS compressé est du binaire opaque ; son intégrité est contrôlée séparément.
  h=re.sub(r'(<script id="official-hb-style" type="text/plain">).*?(</script>)',r'\1OFFICIAL_STYLES\2',h,flags=re.S)
  self.assertEqual(len(d['council']),8);self.assertEqual(len(d['provinces']),11);self.assertEqual(len(d['roles']),4)
  self.assertEqual(len({x['name'] for x in d['council']}),8)
  self.assertNotRegex(h,r'(?i)arcanaloth|rakshasa|shadowfell|vampir|\blich\b|Hezrexen|Fangbane|sarrukh|Primary Ambition|Stat Block|neutral evil|chaotic evil|dndbeyond|excludedTopics')
  self.assertNotRegex(h,r'(?:src|href)=[\"\'](?:https?://|assets/|\.\./)')
  self.assertNotRegex(h,r'(?i)https?://|@import|url\((?!data:)|<link|tiefling|tieffelin|gnome|abysse?|démon|démoniaque|shadowfell|alignement|neutre bon|loyal mauvais|Dread Legion|secret|caché')
 def test_fiches_and_images(self):
  h=SITE.read_text();d=json.loads(re.search(r'<script id="politics-data" type="application/json">(.*?)</script>',h,re.S).group(1))
  # Le bloc CSS compressé est du binaire opaque ; son intégrité est contrôlée séparément.
  h=re.sub(r'(<script id="official-hb-style" type="text/plain">).*?(</script>)',r'\1OFFICIAL_STYLES\2',h,flags=re.S)
  imgs=json.loads(re.search(r'<script id="politics-images" type="application/json">(.*?)</script>',h,re.S).group(1))
  self.assertEqual([c['id'] for c in d['council']],[f[0] for f in FICHES])
  self.assertEqual(set(imgs),{'embleme','abjuration','invocation','divination','enchantement','evocation','illusion','necromancie','transmutation','pratique'})
  for (id,name,anchor),c in zip(FICHES,d['council']):
   with self.subTest(fiche=id):
    self.assertEqual(c['name'],name)
    self.assertTrue(c['html'].startswith(f'<h1>{name}</h1>'));self.assertIn(anchor,c['html'])
    self.assertEqual('class="block note"' in c['html'],id!='invocation')
  self.assertEqual(h.count(imgs['embleme']),1)
  self.assertEqual(h.count('data:image/'),10)
  for key in [f[0] for f in FICHES]+['pratique']:
   self.assertTrue(imgs[key].startswith('data:image/png;base64,'))
   portrait=base64.b64decode(imgs[key].split(',',1)[1])
   self.assertEqual(portrait,(ROOT/f'sources/site/politique/assets/{key}.png').read_bytes())
   offset=8
   while offset<len(portrait):
    size=int.from_bytes(portrait[offset:offset+4],'big')
    self.assertNotIn(portrait[offset+4:offset+8],{b'eXIf',b'tEXt',b'iTXt',b'zTXt'})
    offset+=size+12
  self.assertTrue(imgs['embleme'].startswith('data:image/png;base64,'))
  png=base64.b64decode(imgs['embleme'].split(',',1)[1])
  self.assertEqual(png,(ROOT/'sources/site/politique/assets/embleme.png').read_bytes())
  self.assertEqual(png[:8],b'\x89PNG\r\n\x1a\n')
  offset=8
  while offset<len(png):
   size=int.from_bytes(png[offset:offset+4],'big')
   self.assertNotIn(png[offset+4:offset+8],{b'eXIf',b'tEXt',b'iTXt',b'zTXt'})
   offset+=size+12
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
   await page.locator('[data-section="conseil"]').click();cards=page.locator('.zulkir-card');assert await cards.count()==8
   for id in ['politics-emblem','council-emblem']:
    assert await page.locator('#'+id).evaluate('i=>i.complete&&i.naturalWidth>400')
   reader=page.locator('#reader');is_open=lambda:reader.evaluate('d=>d.open')
   in_dialog="document.getElementById('reader').contains(document.activeElement)"
   for i,(id,name,anchor) in enumerate(FICHES):
    card=cards.nth(i);assert await card.get_attribute('data-fiche')==id
    assert await card.locator('img').count()==1,'Un portrait approuvé par zulkir'
    assert await card.locator('img').evaluate('i=>i.complete&&i.naturalWidth>0')
    assert name in await card.inner_text()
    await card.click();assert await is_open(),id
    assert await page.locator('#reader-title').inner_text()==name
    assert await page.evaluate("document.activeElement.id")=='reader-title'
    assert anchor in await page.locator('#reader-body').inner_text()
    assert await page.locator('#reader-pos').inner_text()==f'{i+1} / 8'
    assert await page.locator('#reader-body img').count()==1
    assert await page.locator('#reader-body img').evaluate('i=>i.complete&&i.naturalWidth>0')
    await page.screenshot(path=f'/tmp/thay-portrait-{id}.png')
    if id!='invocation':assert await page.locator('#reader-body .note').is_visible()
    else:assert await page.locator('#reader-body .note').count()==0
    await page.keyboard.press('Escape');assert not await is_open(),id
    await page.wait_for_function('(id)=>document.activeElement.dataset.fiche===id',arg=id)
    assert await page.evaluate("document.activeElement.dataset.fiche")==id,'retour du focus'
   # Navigation précédent/suivant, boucle et flèches
   await cards.first.click();await page.locator('#reader-prev').click();assert await page.locator('#reader-title').inner_text()=='Nzas'
   await page.locator('#reader-next').click();assert await page.locator('#reader-title').inner_text()=='Yazir Nym'
   await page.locator('#reader-next').click();assert await page.locator('#reader-title').inner_text()=='Nevron'
   await page.keyboard.press('ArrowRight');assert await page.locator('#reader-title').inner_text()=='Lethnar'
   await page.keyboard.press('ArrowLeft');assert await page.locator('#reader-title').inner_text()=='Nevron'
   # Piège du focus : Tab et Maj+Tab restent dans le lecteur ; Entrée active les boutons
   for key in ['Tab']*7+['Shift+Tab']*7:
    await page.keyboard.press(key);assert await page.evaluate(in_dialog),key
   await page.locator('#reader-next').focus();await page.keyboard.press('Enter');assert await page.locator('#reader-title').inner_text()=='Lethnar'
   assert await page.evaluate("getComputedStyle(document.querySelector('#reader-body')).columnCount")=='2'
   assert await page.evaluate("document.querySelector('#reader-body h1').getBoundingClientRect().width>=document.querySelector('#reader-body').getBoundingClientRect().width-1"),'titre sur deux colonnes'
   await page.locator('#reader-body h1').hover();await page.screenshot(path='/tmp/thay-zulkir-desktop.png')
   await page.locator('#reader-close').focus();await page.keyboard.press('Enter');assert not await is_open()
   # L’événement natif close est asynchrone : attendre le retour du focus prévu par le lecteur.
   await page.wait_for_function("document.activeElement.dataset.fiche==='divination'")
   assert await page.evaluate("document.activeElement.dataset.fiche")=='divination'
   await page.screenshot(path='/tmp/thay-zulkir-galerie-desktop.png',full_page=True)
   await page.locator('[data-section="provinces"]').click();assert await page.locator('.province-card').count()==11
   await page.locator('#province-search').fill('Xelnene');assert await page.locator('.province-card:visible').count()==1
   await page.locator('#province-search').fill('zzzz');assert await page.locator('#no-results').is_visible()
   await page.locator('#province-search').fill('');assert await page.locator('.province-card:visible').count()==11
   await page.locator('[data-section="pratique"]').click()
   practice=page.frame_locator('#practice-frame').locator('.page')
   await practice.wait_for()
   assert 'haut placé' in await practice.inner_text()
   assert await practice.locator('h2').count()==7
   await page.locator('[data-section="pouvoir"]').click();await page.screenshot(path='/tmp/thay-politique-desktop.png',full_page=True)
   await page.set_viewport_size({'width':390,'height':844});await page.locator('[data-section="conseil"]').click();await page.screenshot(path='/tmp/thay-politique-mobile.png',full_page=True)
   assert await page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),'galerie mobile'
   for i in range(8):
    await page.locator('.zulkir-card').nth(i).click();assert await page.locator('#reader').evaluate('d=>d.open')
    assert await page.evaluate("getComputedStyle(document.querySelector('#reader-body')).columnCount")=='1'
    assert await page.evaluate("(()=>{const s=document.getElementById('reader-scroll'),r=document.getElementById('reader').getBoundingClientRect();return s.scrollWidth<=s.clientWidth+1&&r.right<=innerWidth+1&&r.left>=-1})()"),i
    assert await page.evaluate("[...document.querySelectorAll('#reader .reader-bar button')].every(b=>{const r=b.getBoundingClientRect();return r.right<=innerWidth+1&&r.height>=44})"),i
    assert await page.locator('#reader-body img').count()==1
    assert await page.locator('#reader-body img').evaluate('i=>i.complete&&i.naturalWidth>0')
    await page.screenshot(path=f'/tmp/thay-zulkir-mobile-{i}.png')
    if i==0:await page.screenshot(path='/tmp/thay-zulkir-mobile.png')
    await page.locator('#reader-close').click()
   for section in ['pouvoir','provinces','lois','pratique','conseil']:
    await page.locator(f'[data-section="{section}"]').click()
    assert await page.evaluate('document.documentElement.scrollWidth <= innerWidth+1'),section
   await page.locator('[data-section="pouvoir"]').click();await page.locator('[data-role="rouges"]').focus();await page.keyboard.press('Enter');assert 'Magiciens Rouges' in await page.locator('#role-title').inner_text()
   await page.goto(path.as_uri()+'#lois');assert await page.locator('#lois').is_visible()
   await page.goto(path.as_uri()+'#inconnu');assert await page.locator('#pouvoir').is_visible()
   assert not errors,errors;assert all(u.startswith(path.as_uri()) or u.startswith('data:') for u in requests),requests
   print('PASS : organigramme, 8 fiches zulkirs (galerie, lecteur, Échap, retour du focus, piège Tab, précédent/suivant, colonnes), 8 zulkirs, 11 provinces, recherche, situations, clavier, mobile, liens profonds ; HTML isolé sans ressources externes ni erreurs JS.')
   await b.close()
if __name__=='__main__':
 result=unittest.TextTestRunner().run(unittest.defaultTestLoader.loadTestsFromTestCase(PublicPolitics))
 if not result.wasSuccessful():raise SystemExit(1)
 asyncio.run(browser_test())
