#!/usr/bin/env python3
"""Assembler le dossier politique autonome à partir des seules sources publiques."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'sources/site/politique'
def main():
 data=json.loads((SRC/'public-data.json').read_text())
 assert set(data)=={'roles','council','provinces','situations'}
 assert len(data['roles'])==4 and len(data['council'])==8 and len(data['provinces'])==11
 raw=json.dumps(data,ensure_ascii=False,indent=2)
 assert not re.search(r'(?i)arcanaloth|rakshasa|shadowfell|vampir|\blich\b|Hezrexen|Fangbane|sarrukh|stat block|primary ambition|excludedTopics',raw)
 template=(SRC/'index.template.html').read_text()
 assert template.count('{{PUBLIC_DATA}}')==1
 html=template.replace('{{PUBLIC_DATA}}',raw.replace('<','\\u003c'))
 dest=ROOT/'site/politique-thay.html';dest.parent.mkdir(exist_ok=True);dest.write_text(html)
 print(f'HTML généré : {dest} — {dest.stat().st_size} octets ; 8 zulkirs, 11 provinces, 4 rôles, {len(data["situations"])} situations ; aucune ressource externe.')
if __name__=='__main__':main()
