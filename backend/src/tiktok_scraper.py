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
    
    # Filter links to include only video URLs
    video_links = [h for h in all_links if '/video/' in h]
    
    # Extract video IDs to identify unique videos
    unique_videos = {}
    for link in video_links:
        try:
            # Extract the video ID from the URL
            video_id = link.split('/video/')[1].split('?')[0]
            # Only keep the first URL for each video ID
            if video_id not in unique_videos:
                unique_videos[video_id] = link
        except Exception as e:
            logger.warning(f"Could not extract video ID from URL {link}: {str(e)}")
    
    # Get the list of unique video URLs
    unique_video_urls = list(unique_videos.values())
    
    logger.info(f"Found {len(video_links)} total video URLs, filtered to {len(unique_video_urls)} unique videos for hashtag: {hashtag}")
    return unique_video_urls