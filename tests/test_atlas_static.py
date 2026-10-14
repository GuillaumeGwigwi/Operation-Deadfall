import base64
import json
import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

class AtlasPublicTest(unittest.TestCase):
    def setUp(self):
        self.html=(ROOT/'site/atlas-de-thay.html').read_text()
        match=re.search(r'<script id="atlas-public-data" type="application/json">(.*?)</script>',self.html,re.S)
        self.assertIsNotNone(match,'Données publiques embarquées absentes')
        self.data=json.loads(match.group(1))

    def test_public_data_is_complete_and_has_unique_identifiers(self):
        points=self.data['landmarks']
        self.assertEqual(len(points),46)
        self.assertEqual(len({p['id'] for p in points}),46)
        self.assertEqual(sum(p['kind']=='province' for p in points),11)
        for p in points:
            self.assertTrue(0<=p['x']<=100 and 0<=p['y']<=100)
            self.assertIn('class="block note"',p['bodyHTML'])
            if p['image']: self.assertIn(p['image'],self.data['embeddedImages'])

    def test_site_does_not_reference_mj_sources_or_network(self):
        # Exclure les octets encodés des images : scanner les données et le code, pas de fausses chaînes aléatoires.
        text=re.sub(r'data:image/jpeg;base64,[A-Za-z0-9+/=]+','IMAGE_EMBARQUEE',self.html)
        self.assertNotRegex(text,r'(?i)https?://|sources/|\.\./|fetch\s*\(|assets/')
        # Les noms publics de la carte et des autorités ne sont pas des révélations.
        self.assertNotRegex(text,r'(?i)malefice|mortum|sarrukh|rakshasa|arcanaloth|Hezrexen|Fangbane|\bVrill\b|\bKrazt\b|magie sauvage|prison souterraine')

    def test_only_reviewed_illustrations_are_embedded(self):
        images=self.data['embeddedImages']
        self.assertEqual(set(images),{'gauros','port-ala','pont-frontiere','eltabbar-plan'})
        for uri in images.values():
            self.assertTrue(uri.startswith('data:image/jpeg;base64,'))
            decoded=base64.b64decode(uri.split(',',1)[1],validate=True)
            self.assertTrue(decoded.startswith(b'\xff\xd8') and decoded.endswith(b'\xff\xd9'))
        self.assertIn('id="map-image"',self.html)
        self.assertIn('src="data:image/jpeg;base64,',self.html)

    def test_delivery_directory_contains_only_standalone_html(self):
        files=list((ROOT/'site').iterdir())
        self.assertIn('atlas-de-thay.html',{p.name for p in files})
        self.assertTrue(all(p.is_file() and p.suffix=='.html' for p in files),'Le dossier de livraison ne doit contenir que des sites HTML autonomes')

if __name__=='__main__': unittest.main()
