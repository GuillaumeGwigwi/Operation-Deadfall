"""Public source coverage, without testing word-count padding."""
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
class PublicDepth(unittest.TestCase):
    def test_public_personal_information_not_reduced_to_office(self):
        expected = {
            'abjuration': ['frontière', 'soins'],
            'invocation': ['tieffelin', 'invocateur'],
            'divination': ['étendre', 'tribunal'],
            'enchantement': ['privilèges', 'marchands'],
            'evocation': ['évocation', 'Gulga Vull'],
            'illusion': ['revenue', 'Tour des Illusions'],
            'necromancie': ['régence', 'Hall Rouge'],
            'transmutation': ['transformations', 'Bezantur'],
        }
        for key, terms in expected.items():
            text = (ROOT / 'sources/site/politique/fiches' / (key+'.md')).read_text()
            for term in terms:
                with self.subTest(key=key, term=term): self.assertIn(term, text)
    def test_no_private_plans_in_personal_fiches(self):
        text = '\n'.join(p.read_text() for p in (ROOT/'sources/site/politique/fiches').glob('*.md'))
        for term in ['Malefice Mortum', 'Hezrexen', 'Shadowfell', 'Abyss', 'phylactère']:
            self.assertNotIn(term, text)
if __name__ == '__main__': unittest.main()
