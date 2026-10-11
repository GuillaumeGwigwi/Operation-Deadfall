import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

MODULE = Path(__file__).with_name('import_source.py')

class ImportTests(unittest.TestCase):
    def test_local_import_preserves_text_tables_and_classifies_assets(self):
        self.assertTrue(MODULE.exists(), 'Local HTML importer is not implemented yet')
        spec = importlib.util.spec_from_file_location('import_source', MODULE)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        supplied = '''<div class="p-article-content"><h1 id="Title">Test Chapter</h1>
        <p>Opening paragraph.</p><h2 id="CouncilOfZulkirs">Council</h2>
        <h3 id="ZulkirDescriptions">Descriptions</h3><h4 id="Delraz">Delraz</h4>
        <p>Enchantment &amp; ambition.</p><aside><p>Secret timeline.</p></aside>
        <table><caption><h4 id="ExampleTable">Example</h4></caption><thead><tr><th>Die</th><th>Effect</th></tr></thead><tbody><tr><td>1</td><td>Important effect.</td></tr></tbody></table>
        <figure><span class="artist-credit">Artist A</span><a href="https://media.dndbeyond.com/test/map.jpg"><img src="https://media.dndbeyond.com/test/map.jpg"></a><figcaption>Map <a href="https://media.dndbeyond.com/test/map-player.jpg">View Player Version</a></figcaption></figure>
        <p><a href="/monsters/123-example">Creature</a></p><script>alert(1)</script></div>'''
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / 'input.html'
            source.write_text(supplied, encoding='utf-8')
            result = module.import_html(source, root / 'output', 'https://www.dndbeyond.com/sources/test', download=False)
            self.assertEqual(result['counts']['assets'], 2)
            self.assertEqual(result['counts']['tables'], 1)
            self.assertEqual(result['counts']['zulkirs'], 1)
            chapter = (root / 'output/chapter.md').read_text()
            for text in ['Opening paragraph.', 'Enchantment & ambition.', 'Secret timeline.', 'Important effect.']:
                self.assertIn(text, chapter)
            self.assertNotIn('alert(1)', chapter)
            self.assertIn('https://www.dndbeyond.com/monsters/123-example', chapter)
            manifest = json.loads((root / 'output/manifest.json').read_text())
            self.assertEqual({a['audience'] for a in manifest['assets']}, {'mj', 'players'})
            self.assertTrue(all(a['status'] == 'not_downloaded' for a in manifest['assets']))
            self.assertEqual(manifest['assets'][0]['artist'], 'Artist A')
            self.assertEqual(len(list((root / 'output/tables').glob('*.csv'))), 1)
            self.assertEqual((root / 'output/original.html').read_text(), supplied)
            self.assertTrue((root / 'output/entities/zulkirs/Delraz.md').exists())

class ImageTests(unittest.TestCase):
    def load_module(self):
        spec = importlib.util.spec_from_file_location('import_source', MODULE)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_local_saved_images_are_copied_and_cached_cdn_images_stay_local(self):
        module = self.load_module()
        from PIL import Image
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            raw = root / 'raw'
            raw.mkdir()
            saved = raw / 'page_files'
            saved.mkdir()
            Image.new('RGB', (4, 5), 'blue').save(saved / 'map-local-player.png')
            source = raw / 'input.html'
            source.write_text('<div class="p-article-content"><h1>Local page</h1><img src="page_files/map-local-player.png"></div>')
            result = module.import_html(source, root / 'out', 'https://www.dndbeyond.com/sources/test', download=False)
            self.assertEqual(result['counts']['assets'], 1, 'Saved local image was not discovered')
            self.assertEqual(result['assets'][0]['status'], 'copied')
            self.assertEqual(result['assets'][0]['audience'], 'players')
            self.assertTrue((root / 'out' / result['assets'][0]['path']).exists())
            self.assertNotIn('https://www.dndbeyond.com/sources/page_files', (root / 'out/chapter.md').read_text())
            source.write_text('<div class="p-article-content"><h1>Cached page</h1><img src="https://media.dndbeyond.com/test/cached.png"></div>')
            cached = root / 'out2/assets/illustrations/cached.png'
            cached.parent.mkdir(parents=True)
            Image.new('RGB', (6, 7), 'green').save(cached)
            second = module.import_html(source, root / 'out2', 'https://www.dndbeyond.com/sources/test', download=False)
            self.assertEqual(second['assets'][0]['status'], 'cached')
            self.assertIn('assets/illustrations/cached.png', (root / 'out2/chapter.md').read_text())

    def test_download_layer_rejects_html_and_reuses_valid_local_image(self):
        module = self.load_module()
        self.assertTrue(hasattr(module, 'validate_image'), 'Image validation is not implemented yet')
        with self.assertRaises(ValueError):
            module.validate_image(b'<html>Access denied</html>')
        from PIL import Image
        import io
        stream = io.BytesIO()
        Image.new('RGB', (2, 3), 'red').save(stream, format='PNG')
        data = stream.getvalue()
        self.assertEqual(module.validate_image(data)['width'], 2)
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            image = root / 'assets/illustrations/test.png'
            image.parent.mkdir(parents=True)
            image.write_bytes(data)
            asset = {'url': 'https://media.dndbeyond.com/test.png', 'path': 'assets/illustrations/test.png', 'status': 'not_downloaded'}
            module.download_asset(asset, root)
            self.assertEqual(asset['status'], 'cached')
            self.assertEqual(asset['height'], 3)
            self.assertEqual(asset['bytes'], len(data))
            self.assertEqual(len(asset['sha256']), 64)

if __name__ == '__main__':
    unittest.main()
