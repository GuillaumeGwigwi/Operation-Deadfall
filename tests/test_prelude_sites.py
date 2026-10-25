import base64,gzip,hashlib,json,re,unittest
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
CASES=[('prelude-cavernes-du-chaos-mj.html','01-les-cavernes-du-chaos.homebrewery.md',r'[A-K]\d+',64),('prelude-dragon-d-alaor-mj.html','02-le-dragon-d-alaor.homebrewery.md',r'M\d+',39)]
class PreludeSites(unittest.TestCase):
 def test_two_standalone_readers_preserve_every_location(self):
  css=(ROOT/'sources/site/politique/homebrewery-officiel/homebrewery-v3-phb.offline.css').read_bytes()
  for filename,source,pattern,count in CASES:
   with self.subTest(site=filename):
    p=ROOT/'site'/filename
    self.assertTrue(p.is_file(),f'Site manquant: {p}')
    soup=BeautifulSoup(p.read_text(),'html.parser')
    data=json.loads(soup.select_one('#prelude-data').string)
    self.assertEqual(data['audience'],'MJ')
    self.assertEqual(data['source_sha256'],hashlib.sha256((ROOT/'sources/propositions/preludes-thay'/source).read_bytes()).hexdigest())
    embedded=gzip.decompress(base64.b64decode(soup.select_one('#official-hb-style').string))
    self.assertEqual(embedded,css)
    ids=[e['key'] for e in data['entries'] if e['kind']=='room']
    self.assertEqual(len(ids),count)
    self.assertEqual(len(set(ids)),count)
    expected=set(re.findall(r'^### .*\(('+pattern+r')\)$',(ROOT/'sources/propositions/preludes-thay'/source).read_text(),re.M))
    self.assertEqual(set(ids),expected)
    self.assertTrue(all(d['pages'] for d in data['documents']))
    self.assertTrue(soup.select_one('#search'))
    self.assertTrue(soup.select_one('#reader'))
    self.assertFalse(soup.select('[src]:not([src^="data:"]),link[rel="stylesheet"]'))
if __name__=='__main__':unittest.main()
