import base64,io,json,unittest
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
class PreludeArt(unittest.TestCase):
 def test_fifteen_integrated_images_are_embedded(self):
  soup=BeautifulSoup((ROOT/'site/prelude-cavernes-du-chaos-mj.html').read_text(),'html.parser')
  data=json.loads(soup.select_one('#prelude-data').string)
  book=BeautifulSoup(' '.join(data['documents'][0]['pages']),'html.parser');images=book.select('img')
  self.assertEqual(len(images),15,'Les quinze illustrations doivent être intégrées au livre, pas seulement enregistrées à côté')
  for im in images:
   self.assertTrue(im['src'].startswith('data:image/webp;base64,'))
   raw=base64.b64decode(im['src'].split(',',1)[1])
   with Image.open(io.BytesIO(raw)) as art:
    art.load();self.assertIn('A',art.getbands());self.assertEqual(art.getchannel('A').getextrema(),(0,255))
    self.assertFalse(any(k in art.info for k in ['exif','xmp','parameters','prompt','comment']))
 def test_player_copies_have_no_embedded_notes(self):
  folder=ROOT/'site/illustrations-cavernes-joueurs'
  expected={'01-village.png','02-portrait.png','03-portrait.png','04-paysage.png','05-portrait.png','06-scene.png','07-lieu.png','08-portrait.png','09-scene.png','10-portrait.png','11-scene.png','12-scene.png','13-lieu.png','14-portrait.png','15-lieu.png'}
  self.assertEqual({p.name for p in folder.iterdir()},expected)
  for name in expected:
   with Image.open(folder/name) as im:
    im.load();self.assertFalse(im.info);self.assertFalse(im.getexif())
if __name__=='__main__':unittest.main()
