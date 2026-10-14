import sys
from pathlib import Path
from PIL import Image
src, dest = Path(sys.argv[1]), Path(sys.argv[2])
ids = ['abjuration','invocation','divination','enchantement','evocation','illusion','necromancie','transmutation']
im = Image.open(src).convert('RGB')
w, h = im.size
for i, name in enumerate(ids):
    c, r = i % 4, i // 4
    box = (round(c*w/4)+3, round(r*h/2)+3, round((c+1)*w/4)-3, round((r+1)*h/2)-3)  # 3 px de marge contre les coutures
    tile = im.crop(box)
    tile.save(dest/f'{name}.jpg', 'JPEG', quality=80, optimize=True, progressive=True)  # aucun exif/commentaire transmis
    print(name, box, (dest/f'{name}.jpg').stat().st_size)
