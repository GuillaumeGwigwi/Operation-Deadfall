import json,unittest
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
class ContinuousBook(unittest.TestCase):
 def test_current_readers_are_one_continuous_book(self):
  for name in ['prelude-cavernes-du-chaos-mj.html','prelude-dragon-d-alaor-mj.html']:
   with self.subTest(name=name):
    soup=BeautifulSoup((ROOT/'site'/name).read_text(),'html.parser')
    data=json.loads(soup.select_one('#prelude-data').string)
    self.assertEqual(len(data['documents']),1,'Le prélude doit former un seul livre, sans fiche isolée par rubrique')
    pages=data['documents'][0]['pages']
    self.assertGreater(len(pages),2)
    for i,p in enumerate(pages[:-1]):
     self.assertGreater(len(BeautifulSoup(p,'html.parser').get_text(' ',strip=True).split()),100,f'Page quasi vide: {i+1}')
if __name__=='__main__':unittest.main()
