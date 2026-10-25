import json,subprocess,sys
from pathlib import Path
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
soup=BeautifulSoup((ROOT/'site/prelude-cavernes-du-chaos-mj.html').read_text(),'html.parser')
data=json.loads(soup.select_one('#prelude-data').string)
placements=[]
for i,page in enumerate(data['documents'][0]['pages'],1):
 images=BeautifulSoup(page,'html.parser').select('img')
 if images:placements.append({'page':i,'images':[im.get('alt') for im in images]})
print(json.dumps(placements,ensure_ascii=False,indent=2),flush=True)
path=ROOT/'sources/site/preludes/verification/art-placements.json';path.write_text(json.dumps(placements,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
subprocess.run([sys.executable,'/home/gwi/.hermes/profiles/dnd-assistant/skills/productivity/pdf/scripts/pdf_page_image.py',str(ROOT/'site/prelude-cavernes-du-chaos-mj.pdf'),'--pages',','.join(str(x['page']) for x in placements),'--dpi','110','--out-dir',str(ROOT/'sources/site/preludes/verification/pdf-art')],check=True)
