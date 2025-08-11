import asyncio
from playwright.async_api import async_playwright
import logging

logger = logging.getLogger(__name__)

async def get_all_hyperlinks_playwright(url, headless=True):
    logger.info(f"Launching browser for URL: {url} (headless={headless})")
    async with async_playwright() as p:
        browser = await p.webkit.launch(headless=headless)
        page = await browser.new_page()
        await page.goto(url, wait_until="networkidle")
        logger.info(f"Page loaded: {url}")
        links = await page.eval_on_selector_all("a[href]", "elements => elements.map(el => el.href)")
        logger.info(f"Extracted {len(links)} hyperlinks from page.")
        await browser.close()
        return links

async def fetch_hashtag_video_urls(hashtag, headless=True):
    url = f'https://www.tiktok.com/tag/{hashtag}'
    logger.info(f"Fetching video URLs for hashtag: {hashtag}")
    all_links = await get_all_hyperlinks_playwright(url, headless)
    hashtag_links = [h for h in all_links if '/video/' in h]
    logger.info(f"Filtered {len(hashtag_links)} video URLs for hashtag: {hashtag}")
    return hashtag_links