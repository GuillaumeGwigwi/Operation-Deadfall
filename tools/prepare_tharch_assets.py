#!/usr/bin/env python3
"""Préparation reproductible des seules illustrations régionales revues.

Revue interne (jamais embarquée) : images 01-007 à 01-013 inspectées sur
planche contact. Scènes publiques : port, danger rural, paysage, mine,
troupes mortes-vivantes, pont douanier et extérieur de forteresse. Aucune
annotation de scénario ou identité cachée. Carte joueurs d’Eltabbar revue
et autorisée séparément : géographie publique, sans labels secrets.
Référence : chapitre 1,
10-TharchDescriptions.md ; Eltabbar : 11-EltabbarThaysCapital.md.
Les crédits sont transcrits exactement, casse comprise. Les droits du livre
ne sont pas transférés : partage de campagne, pas licence de republication.
"""
import json
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'sources/site/politique'
SELECTION = [
 ('alaor','01-007.ala-harbor-merchants.png','Kevin Glint, Álvaro Calvo Escudero','Des marchands déchargent leur cargaison au port d’Ala sous le regard d’un Magicien Rouge.'),
 ('delhumide','01-008.vrock-terrorizing-farmer.png','ÁLVARO CALVO ESCUDERO','Un vrock terrorise un fermier de Delhumide.'),
 ('gauros','01-009.tharch-of-gauros.png','David Frasheski','Le paysage rocheux et peu peuplé de Gauros.'),
 ('pyarados','01-010.xorn-in-pyarados-mine.png','LOÏC CANAVAGGIA','Un xorn dans une mine de Pyarados.'),
 ('thaymount','01-011.dread-legion.png','Loïc Canavaggia, Helge C. Balzer','Un ogre zombie dans les rangs de la Légion de l’Effroi.'),
 ('thazalhar','01-012.the-thay-crossing-bridge.png','Andrey Kuzinskiy','Deux marchands mulhorandis sur le pont de Thay Crossing, sous la surveillance d’un Magicien Rouge.'),
 ('eltabbar','01-013.fortress-eltab.png','Sylvain Sarrailh','La forteresse Eltab domine la capitale.'),
]
def main():
    dest = SRC / 'assets/regions'
    dest.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for key, filename, credit, caption in SELECTION:
        image = Image.open(ROOT / 'sources/chapters/chapter-01-thay/assets/illustrations' / filename).convert('RGBA')
        image.thumbnail((1100, 900), Image.Resampling.LANCZOS)
        # Fresh pixels deliberately discard EXIF, XMP, ICC and text metadata.
        clean = Image.frombytes('RGBA', image.size, image.tobytes())
        # The smaller bottom/right compositions meet parchment only on the left.
        # Localized alpha, not blur: preserve foreground, signatures and original
        # painted lower edges. The upper raccord uses HB's official imageMaskEdge.
        if key in {'delhumide', 'pyarados', 'thaymount', 'eltabbar'}:
            alpha = clean.getchannel('A')
            pixels = alpha.load()
            fade = round(clean.width * .09)
            for x in range(fade):
                t = x / fade
                opacity = t*t*(3-2*t)
                for y in range(clean.height):
                    pixels[x, y] = round(pixels[x, y] * opacity)
            clean.putalpha(alpha)
        clean.save(dest / f'{key}.webp', 'WEBP', quality=84, method=6)
        manifest[key] = {'file': f'assets/regions/{key}.webp', 'credit': credit, 'caption': caption, 'width': clean.width, 'height': clean.height}
    # Public player map reviewed separately; keep its original cartographic frame.
    image = Image.open(ROOT / 'sources/chapters/chapter-01-thay/assets/maps/players/map-01-02.eltabbar-player.png').convert('RGBA')
    image.thumbnail((1600, 1200), Image.Resampling.LANCZOS)
    clean = Image.frombytes('RGBA', image.size, image.tobytes())
    clean.save(dest / 'eltabbar-map.webp', 'WEBP', quality=90, method=6)
    manifest['eltabbar-map'] = {'file': 'assets/regions/eltabbar-map.webp', 'credit': 'Gerralt Landman', 'caption': 'Eltabbar, ses canaux et les rives du lac Thaylambar.', 'width': clean.width, 'height': clean.height}
    (SRC / 'region-images.public.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    print(f'{len(manifest)} illustrations WebP préparées sans métadonnées.')
if __name__ == '__main__':
    main()
