import base64,hashlib,io,json,unittest
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
ART=ROOT/'sources/propositions/preludes-thay/illustrations-alaor'
class AlaorArt(unittest.TestCase):
 def test_fourteen_illustrations_are_integrated(self):
  soup=BeautifulSoup((ROOT/'site/prelude-dragon-d-alaor-mj.html').read_text(),'html.parser');data=json.loads(soup.select_one('#prelude-data').string)
  images=BeautifulSoup(' '.join(data['documents'][0]['pages']),'html.parser').select('img');self.assertEqual(len(images),14)
  for im in images:
   self.assertTrue(im['src'].startswith('data:image/webp;base64,'))
   with Image.open(io.BytesIO(base64.b64decode(im['src'].split(',',1)[1]))) as art:
    art.load();self.assertIn('A',art.getbands());self.assertEqual(art.getchannel('A').getextrema(),(0,255));self.assertFalse(art.getexif())
    if im.get('alt')=='Mirel Astafar':self.assertGreater(art.height,art.width,'Le cadrage livre de Mirel doit permettre une présentation en colonne, sans isoler Orso')
 def test_clean_neutral_player_copies(self):
  expected={'01-port.png','02-portrait.png','03-portrait.png','04-scene.png','05-lieu.png','06-portrait.png','07-portrait.png','08-portrait.png','09-portrait.png','10-scene.png','11-lieu.png','12-scene.png','13-portrait.png','14-lieu.png'}
  folder=ROOT/'site/illustrations-alaor-joueurs';self.assertTrue(folder.is_dir());self.assertEqual({p.name for p in folder.iterdir()},expected)
  for name in expected:
   with Image.open(folder/name) as im:im.load();self.assertFalse(im.info);self.assertFalse(im.getexif())
 def test_story_and_first_book_are_preserved(self):
  baseline=json.loads((ART/'archives/avant-illustrations/baseline.json').read_text())
  for name,digest in baseline['cavernes'].items():self.assertEqual(hashlib.sha256((ROOT/'site'/name).read_bytes()).hexdigest(),digest,name)
  spec=next(s for s in json.loads((ROOT/'sources/site/preludes/rendered.json').read_text()) if s['id']=='alaor')
  self.assertEqual(' '.join(BeautifulSoup(spec['html'],'html.parser').stripped_strings),baseline['alaor_text'])
if __name__=='__main__':unittest.main()
