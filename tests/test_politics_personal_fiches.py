import json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class PersonalFiches(unittest.TestCase):
 def test_no_generic_thay_or_city_passages(self):
  h=(ROOT/'site/politique-thay.html').read_text()
  data=json.loads(re.search(r'<script id="politics-data" type="application/json">(.*?)</script>',h,re.S).group(1))
  banned=['Lieu associé','Lieux associés','Repères du commerce','premier centre commercial','plus grand port','pas de commandement militaire unifié','les zulkirs répriment','Le haut plateau central','campagne fertile','Chaque zulkir','des demeures','scribes','les péages des routes','infrastructures, commerce','Infrastructures, commerce']
  for c in data['council']:
   for phrase in banned:
    self.assertFalse(phrase in c['html'],f"{c['name']} contient encore du contexte générique : {phrase}")
 def test_personal_connections_are_preserved(self):
  h=(ROOT/'site/politique-thay.html').read_text()
  data=json.loads(re.search(r'<script id="politics-data" type="application/json">(.*?)</script>',h,re.S).group(1))
  by_id={c['id']:c['html'] for c in data['council']}
  anchors={'abjuration':['garnison','Escalant'],'invocation':['Nevron','invocation'],'divination':['tribunal','choisis'],'enchantement':['taxes','marchands'],'evocation':['palais','famille','Gulga Vull'],'illusion':['Zedivek Mazradash','Tour des Illusions'],'necromancie':['Hall Rouge','Szul'],'transmutation':['armée','Bezantur']}
  self.assertEqual(set(by_id),set(anchors))
  for id,phrases in anchors.items():
   for phrase in phrases:self.assertTrue(phrase in by_id[id],f'{id} : lien personnel perdu ({phrase})')
if __name__=='__main__':unittest.main()
