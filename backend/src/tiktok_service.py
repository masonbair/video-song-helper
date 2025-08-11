import os
import logging
from datetime import datetime, timedelta
from TikTokApi import TikTokApi
from src.tiktok_scraper import fetch_hashtag_video_urls

ms_token = os.environ.get("ms_token", None)
last_token_refresh = None
token_refresh_interval = timedelta(hours=6)
logger = logging.getLogger(__name__)

async def trending_videos_with_auto_token():
    global last_token_refresh
    try:
        if ms_token:
            logger.info("Attempting with manual ms_token ")
            async with TikTokApi() as api:
                await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, browser=os.getenv("TIKTOK_BROWSER", "webkit"))
                videos_data = []
                async for video in api.trending.videos(count=30):
                    logger.info(video)
                    videos_data.append(video.as_dict)
                last_token_refresh = datetime.now()
                logger.info(f"Successfully fetched {len(videos_data)} videos with manual token")
                return videos_data
    except Exception as e:
        logger.warning(f"Manual token failed: {e}. Trying auto-generation...")
    try:
        logger.info("Attempting automatic token generation")
        async with TikTokApi() as api:
            await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, browser=os.getenv("TIKTOK_BROWSER", "webkit"))
            logger.info("Created session with auto-generated token")
            videos_data = []
            async for video in api.trending.videos(count=30):
                logger.info(video)
                videos_data.append(video.as_dict)
            last_token_refresh = datetime.now()
            logger.info(f"Successfully fetched {len(videos_data)} videos with auto-generated token")
            return videos_data
    except Exception as e:
        logger.error(f"Both manual and auto token generation failed: {e}")
        raise

async def get_song_info_from_videos(video_urls):
    """
    Given a list of TikTok video URLs, fetch the associated song info for each video.
    Returns a list of dicts with song metadata.
    """
    song_infos = []
    async with TikTokApi() as api:
        logger.info("Creating TikTokApi session to fetch song info")
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, browser=os.getenv("TIKTOK_BROWSER", "webkit"))
        for url in video_urls:
            try:
                music = await api.sound(id="7487284842980248854").info()
                logger.info(music)
                # music = video.sound
                song_info = {
                    "title": music.title,
                    "author": music.author,
                    "id": music.id,
                    "play_url": music.play_url,
                    "cover_url": music.cover_url,
                    "duration": music.duration,
                    "video_url": url
                }
                song_infos.append(song_info)
            except Exception as e:
                logger.warning(f"Failed to fetch song info for {url}: {e}")
    return song_infos

async def get_songs_by_hashtag(keyword: str, count: int = 10):
    video_urls = await fetch_hashtag_video_urls(keyword)
    song_infos = await get_song_info_from_videos(video_urls)
    if song_infos:
        logger.info(f"Found song: {song_infos[0]['title']} by {song_infos[0]['author']}")
    else:
        logger.warning(f"No songs found for hashtag: {keyword}")
    return song_infos

