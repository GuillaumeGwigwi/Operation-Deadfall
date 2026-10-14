import json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ChapterAtlasTest(unittest.TestCase):
 def setUp(self):
  html=(ROOT/'site/atlas-de-thay.html').read_text()
  self.data=json.loads(re.search(r'<script id="atlas-public-data" type="application/json">(.*?)</script>',html,re.S).group(1))
  self.places={x['id']:x for x in self.data['landmarks']}
 def test_eltabbar_includes_public_wards_and_establishments(self):
  body=self.places['eltabbar']['bodyHTML']
  for name in ['Thubbleston','Wrynn','Iskari','Thaylambar','Renatta Vott','Mythrellaa','Syle Gur','Elsa Tor','Vellis Vant','Xulfer','Elton','Nestor','Peri Po']:
   self.assertIn(name,body)
  self.assertIn('1 PA',body); self.assertIn('1 PC',body); self.assertIn('250 PO',body)
  self.assertGreaterEqual(body.count('<h4'),10)
 def test_all_locations_described_are_represented(self):
  self.assertEqual(len(self.places),46)
  for id in ['alaor-major','alaor-minor','denzar','gauros-keep','citadel','ankhur','belizir','delabbar','hurkh','mothur','nuthretos','sekelmur','solzepar','surag','thazrumaros','zolum']:
   self.assertIn(id,self.places)
  self.assertIn('Thay Crossing',self.places['thazalhar']['bodyHTML'])
 def test_country_guide_covers_relief_and_practical_context(self):
  self.assertTrue('guide' in self.data,'Guide de Thay absent')
  body=self.data['guide']['bodyHTML']
  for term in ['Bas-Thay','plateau thayen','Premier Escarpement','Second Escarpement','climat','commerce']:
   self.assertIn(term,body)
 def test_public_payload_has_no_hidden_revelations(self):
  text=json.dumps({k:v for k,v in self.data.items() if k!='embeddedImages'},ensure_ascii=False)
  self.assertNotRegex(text,r'(?i)sarrukh|rakshasa|arcanaloth|Hezrexen|Fangbane|\bVrill\b|\bKrazt\b|magie sauvage|prison souterraine|réseau de contrebande|assassin.*apprenti|malefice|mortum')
if __name__=='__main__': unittest.main()
