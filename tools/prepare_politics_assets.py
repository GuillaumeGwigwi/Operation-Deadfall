#!/usr/bin/env python3
"""Préparer l’emblème public du livre, sans métadonnées, sans génération d’image."""
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'sources/chapters/chapter-01-thay/assets/illustrations/01-002.symbol-of-the-red-wizards.png'
DEST=ROOT/'sources/site/politique/assets/embleme.png'
def main():
    with Image.open(SOURCE) as original:
        image=original.convert('RGBA')
        image.thumbnail((640,640),Image.Resampling.LANCZOS)
        clean=Image.frombytes('RGBA',image.size,image.tobytes())
        DEST.parent.mkdir(parents=True,exist_ok=True)
        clean.save(DEST,format='PNG',optimize=True)
    for key,name in [('evocation','09-005.xelnene-thrul.png'),('necromancie','09-004.szass-tam.png')]:
        source=ROOT/'sources/chapters/appendix-b-bestiary/assets/illustrations'/name
        with Image.open(source) as original:
            image=original.convert('RGBA')
            image.thumbnail((700,1000),Image.Resampling.LANCZOS)
            clean=Image.frombytes('RGBA',image.size,image.tobytes())
            target=DEST.parent/f'{key}.png'
            clean.save(target,format='PNG',optimize=True)
        with Image.open(target) as portrait:
            assert not portrait.info and not portrait.getexif()
            print(f'Portrait préparé : {target} ; {portrait.width} × {portrait.height} ; sans métadonnées')
    with Image.open(ROOT/'sources/chapters/chapter-01-thay/assets/illustrations/01-004.tax-station.png') as original:
        image=original.convert('RGBA')
        image.thumbnail((900,640),Image.Resampling.LANCZOS)
        clean=Image.frombytes('RGBA',image.size,image.tobytes())
        clean.save(DEST.parent/'pratique.png',format='PNG',optimize=True)
    # Six interprétations visuelles générées, validées par le MJ pour les joueurs.
    for school,ident in [('abjuration','yazir-nym'),('invocation','nevron'),('divination','lethnar'),('enchantement','delraz'),('illusion','mythrellaa'),('transmutation','nzas')]:
        source=ROOT/f'sources/propositions/portraits-zulkirs-mj/portraits/{ident}.png'
        with Image.open(source) as original:
            image=original.convert('RGB')
            clean=Image.frombytes('RGB',image.size,image.tobytes())
            target=DEST.parent/f'{school}.png'
            clean.save(target,format='PNG',optimize=True)
        with Image.open(target) as result:
            assert not result.info and not result.getexif()
            print(f'Portrait validé intégré aux assets publics : {school} ; {result.width} × {result.height}')
    with Image.open(DEST) as result:
        assert not result.info and not result.getexif()
        print(f'Asset existant préparé : {DEST} ; {result.width} × {result.height} ; sans métadonnées')
if __name__=='__main__':main()
