import unittest
from pathlib import Path
from html.parser import HTMLParser
ROOT=Path(__file__).resolve().parents[1]
class ResourceParser(HTMLParser):
    def __init__(self): super().__init__(); self.external=[]; self.images=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='script' and attrs.get('src'): self.external.append(attrs['src'])
        if tag=='link' and attrs.get('href') and attrs.get('rel')!='canonical': self.external.append(attrs['href'])
        if tag=='img':
            self.images.append(attrs.get('src',''))
            if not attrs.get('src','').startswith('data:image/'): self.external.append(attrs.get('src',''))
class StandaloneTest(unittest.TestCase):
    def test_html_contains_every_resource(self):
        text=(ROOT/'site/index.html').read_text()
        parser=ResourceParser(); parser.feed(text)
        self.assertEqual(parser.external,[], 'Le HTML dépend encore de fichiers voisins ou de ressources distantes')
        self.assertTrue(parser.images)
        self.assertIn('<style',text)
        self.assertIn('window.THAY_ATLAS',text)
if __name__=='__main__': unittest.main()
