"""Bake official Homebrewery brush-mask alpha into reviewed portrait derivatives.
No retouching or new image generation; preserve originals. Avoid paying for oversized
CSS mask layers at each modal open. Run with uv run --with pillow python ...
"""
from pathlib import Path
import re,base64,io,json
from PIL import Image,ImageChops,ImageDraw,ImageFilter
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'sources/site/politique'
css=(SRC/'homebrewery-officiel/homebrewery-v3-phb.offline.css').read_text()
rule=next(s for s in css.split('}') if s.startswith('.page .imageMaskCenter6{'))
encoded=rule.split('base64,',1)[1].split('"',1)[0].split(')',1)[0]
mask=Image.open(io.BytesIO(base64.b64decode(encoded))).convert('RGBA').getchannel('A')
mask=mask.crop(mask.point(lambda v:255 if v>6 else 0).getbbox())
OUT=SRC/'assets/portrait-blends';OUT.mkdir(exist_ok=True)
report=[]
for key in ['abjuration','invocation','divination','enchantement','illusion','transmutation']:
    image=Image.open(SRC/f'assets/{key}.png').convert('RGBA')
    image.thumbnail((1100,1500),Image.Resampling.LANCZOS)
    alpha=mask.resize(image.size,Image.Resampling.LANCZOS)
    # These reviewed originals place their heads close to the upper edge.
    # A stock watercolor mask must never erase the skull, horns or hood.
    protect=Image.new('L',image.size,0)
    outline=[(265,105),(305,85),(330,45),(365,22),(435,22),(477,48),(503,100),(510,180),(480,260),(455,340),(345,340),(315,230),(285,180)]
    if key=='invocation': outline=[(245,90),(265,55),(310,35),(365,22),(435,22),(490,60),(520,150),(490,260),(455,340),(345,340),(300,230),(280,155)]
    if key=='transmutation': outline=[(270,225),(285,150),(325,70),(365,22),(400,22),(455,55),(500,140),(540,250),(530,380),(310,380)]
    ImageDraw.Draw(protect).polygon(outline,fill=255)
    # Retain the reviewed painted foreground inside this guard, not a dark polygon
    # of background. These reviewed red/skin subjects sit against a blue field.
    red,green,blue,_=image.split()
    warm=ImageChops.subtract(red,blue)
    if key=='divination': warm=ImageChops.multiply(warm,red.point(lambda v:255 if v>=55 else 0))
    foreground=warm.point(lambda v:min(255,v*64))
    holes=warm.point(lambda v:0 if v>=4 else 255)
    ImageDraw.floodfill(holes,(0,0),128)
    foreground=ImageChops.lighter(foreground,holes.point(lambda v:255 if v==255 else 0))
    guard=protect.filter(ImageFilter.MaxFilter(15)).filter(ImageFilter.GaussianBlur(4))
    alpha=ImageChops.lighter(alpha,ImageChops.multiply(guard,foreground))
    # Fine contours reviewed against original pixels: avoid an oval of cloak
    # around a protected hand, and keep the cool-lit tip of Nevron's horn.
    details={
      'invocation': [[(238,78),(243,87),(251,91),(263,88),(284,62),(310,43),(337,32),(355,33),(376,39),(397,51),(418,60),(430,82),(410,114),(375,92),(355,77),(331,71),(310,77),(286,96),(271,101),(258,102),(247,99),(241,91)],[(247,842),(282,833),(304,858),(324,885),(341,909),(349,959),(342,972),(331,969),(340,1003),(331,1014),(312,994),(300,998),(279,989),(259,977),(249,949),(247,903)]],
      'enchantement': [[(564,780),(594,784),(618,810),(621,846),(624,880),(611,918),(594,938),(561,964),(537,972),(536,958),(549,928),(551,907),(541,918),(521,930),(517,921),(530,889),(530,860),(544,826)]],
      'transmutation': [[(609,818),(625,821),(635,839),(641,870),(636,902),(623,929),(603,946),(588,950),(590,935),(608,919),(614,902),(612,884),(600,905),(591,905),(590,887),(599,866)]]}
    detail=Image.new('L',image.size,0)
    for polygon in details.get(key,[]): ImageDraw.Draw(detail).polygon(polygon,fill=255)
    alpha=ImageChops.lighter(alpha,detail.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(0.6)))
    assert alpha.getpixel((400,120))==255, 'Head must remain fully opaque'
    image.putalpha(ImageChops.multiply(image.getchannel('A'),alpha))
    dest=OUT/f'{key}.webp';image.save(dest,'WEBP',quality=92,method=6)
    report.append({'id':key,'mask':'official imageMaskCenter6, cropped transparent exterior','width':image.width,'height':image.height,'bytes':dest.stat().st_size})
print(json.dumps(report,ensure_ascii=False,indent=2))
