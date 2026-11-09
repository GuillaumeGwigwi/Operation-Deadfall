from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
def test_late_dialog_close_does_not_steal_search_focus():
 with sync_playwright() as p:
  exe=next(Path('/home/gwi/.cache/ms-playwright').glob('chromium-*/**/chrome'))
  b=p.chromium.launch(headless=True,executable_path=str(exe));page=b.new_page()
  page.goto((ROOT/'site/politique-thay.html').as_uri()+'#provinces')
  page.locator('[data-tharch=alaor]').click()
  page.evaluate("""()=>{const d=document.querySelector('#tharch-reader');window.closeDelivered=false;d.addEventListener('close',()=>window.closeDelivered=true,{once:true});d.close();document.querySelector('#province-search').focus()}""")
  page.wait_for_function('window.closeDelivered')
  assert page.evaluate('document.activeElement.id')=='province-search'
  b.close()
if __name__=='__main__':test_late_dialog_close_does_not_steal_search_focus()
