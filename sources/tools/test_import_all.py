import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

MODULE = Path(__file__).with_name('import_all.py')

class BatchImportTests(unittest.TestCase):
    def test_report_exposes_missing_original_anchors(self):
        spec = importlib.util.spec_from_file_location('import_all', MODULE)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            raw = root / 'raw'
            raw.mkdir()
            (raw / 'chapter-1-one.html').write_text('<div class="p-article-content"><h1>Chapter 1: One</h1><a href="#Missing">Missing reference</a></div>')
            report = module.import_directory(raw, root)
            self.assertIn('link_warnings', report['files'][0], 'Missing source anchors are not reported yet')
            self.assertEqual(report['counts']['link_warnings'], 1)
            self.assertEqual(report['files'][0]['link_warnings'][0]['href'], '#Missing')
            self.assertEqual(report['counts']['images_pending'], 0)

    def test_windows_line_endings_are_preserved_byte_for_byte(self):
        spec = importlib.util.spec_from_file_location('import_all', MODULE)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            raw = root / 'raw'
            raw.mkdir()
            supplied = b'<div class="p-article-content">\r\n<h1>Chapter 1: One</h1>\r\n<p>Facts.</p>\r\n</div>\r\n'
            source = raw / 'chapter-1-one.html'
            source.write_bytes(supplied)
            report = module.import_directory(raw, root)
            self.assertEqual(report['counts']['errors'], 0)
            original = root / 'chapters/chapter-01-one/original.html'
            self.assertEqual(original.read_bytes(), supplied)
            self.assertEqual(source.read_bytes(), supplied)

    def test_appendix_reference_uses_title_and_index_orders_chapters_first(self):
        spec = importlib.util.spec_from_file_location('import_all', MODULE)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            raw = root / 'raw'
            raw.mkdir()
            (raw / 'appendix-a-magic-item.html').write_text('<div class="p-article-content"><h1>Appendix A: Magic Items</h1><h2 id="Item">Magic item</h2><p>An item.</p></div>')
            (raw / 'chapter-1-one.html').write_text('<div class="p-article-content"><h1>Chapter 1: One</h1><p>A chapter.</p></div>')
            report = module.import_directory(raw, root)
            self.assertEqual(report['files'][0]['title'], 'Chapter 1: One')
            appendix = next(i for i in report['files'] if i['title'].startswith('Appendix'))
            self.assertEqual(appendix['source_url'], 'https://www.dndbeyond.com/sources/dnd/aud/appendix-a-magic-items')

    def test_batch_imports_all_local_pages_and_reports_empty_input(self):
        self.assertTrue(MODULE.exists(), 'Batch importer is not implemented yet')
        spec = importlib.util.spec_from_file_location('import_all', MODULE)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            raw = root / 'raw'
            raw.mkdir()
            (raw / 'chapter-1-one.html').write_text('<div class="p-article-content"><h1>Chapter 1: One</h1><h2 id="First">First section</h2><h3 id="Person">A person</h3><p>Local facts.</p><a href="/sources/dnd/aud/chapter-2-two#Second">Next chapter</a></div>')
            (raw / 'chapter-2-two.html').write_text('<div class="p-article-content"><h1>Chapter 2: Two</h1><h2 id="Second">Second section</h2><p>Other facts.</p></div>')
            (raw / 'chapter-3-empty.html').write_text('')
            report = module.import_directory(raw, root, download=False)
            self.assertEqual(report['counts']['inputs'], 3)
            self.assertEqual(report['counts']['imported'], 2)
            self.assertEqual(report['counts']['skipped'], 1)
            self.assertEqual(report['counts']['errors'], 0)
            self.assertTrue((root / 'index.html').exists())
            first = root / 'chapters/chapter-01-one'
            self.assertIn('../chapter-02-two/chapter.md#Second', (first / 'chapter.md').read_text())
            self.assertTrue(list((first / 'entries').glob('*Person.md')))
            catalog = json.loads((root / 'catalog.json').read_text())
            self.assertTrue(any(entry['anchor'] == 'Person' for entry in catalog))
            again = module.import_directory(raw, root, download=False)
            self.assertEqual(again['counts']['imported'], 2)
            self.assertEqual((raw / 'chapter-3-empty.html').read_text(), '')

if __name__ == '__main__':
    unittest.main()
