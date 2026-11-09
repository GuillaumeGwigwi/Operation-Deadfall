"""Capture actual council pages with official typography and image masking."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'sources/site/politique/verification/council-composition'
OUT.mkdir(parents=True,exist_ok=True)
with sync_playwright() as pw:
    exe=next((Path.home()/'.cache/ms-playwright').glob('chromium-*/**/chrome'))
    browser=pw.chromium.launch(executable_path=str(exe),args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1440,'height':1200});page.goto((ROOT/'site/politique-thay.html').as_uri()+'#conseil')
    for i in range(8):
        card=page.locator('.zulkir-card').nth(i);key=card.get_attribute('data-fiche');card.click()
        page.wait_for_function('(key)=>document.querySelector("#reader-frame").contentDocument?.querySelector("[data-portrait]")?.dataset.portrait===key',arg=key)
        review=browser.new_page(viewport={'width':1000,'height':1300})
        review.set_content(page.locator('#reader-frame').evaluate('f=>f.contentDocument.documentElement.outerHTML'))
        review.locator('.page').evaluate('async el=>{await el.ownerDocument.fonts.ready;await Promise.all([...el.querySelectorAll("img")].map(i=>i.decode()))}')
        review.locator('.page').screenshot(path=str(OUT/f'{key}.png'));review.close();page.locator('#reader-close').click()
    browser.close()
print(OUT)
