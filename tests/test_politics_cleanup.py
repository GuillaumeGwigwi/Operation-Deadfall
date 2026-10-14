import json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class Cleanup(unittest.TestCase):
 def test_no_editorial_padding(self):
  h=(ROOT/'site/politique-thay.html').read_text()
  for text in ['Explorer les fiches','Ouvrir une fiche pour','Illustration évocatrice','Ces repères aident','Ils ne garantissent','Les illustrations évoquent']:
   self.assertNotIn(text,h)
  d=json.loads(re.search(r'<script id="politics-data" type="application/json">(.*?)</script>',h,re.S).group(1))
  for c in d['council']:
   self.assertNotIn('Au Conseil des zulkirs',c['html'])
 def test_existing_asset_replaces_generated_images(self):
  h=(ROOT/'site/politique-thay.html').read_text()
  images=json.loads(re.search(r'<script id="politics-images" type="application/json">(.*?)</script>',h,re.S).group(1))
  self.assertEqual(set(images),{'embleme','abjuration','invocation','divination','enchantement','evocation','illusion','necromancie','transmutation','pratique'})
  self.assertTrue(images['embleme'].startswith('data:image/png;base64,'))
  self.assertIn('id="politics-emblem"',h)
if __name__=='__main__':unittest.main()
