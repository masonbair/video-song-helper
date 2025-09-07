import os
import logging
from datetime import datetime, timedelta
from TikTokApi import TikTokApi
from src.tiktok_scraper import fetch_hashtag_video_urls
import asyncio
from src.cache_manager import cache

# Increased from 2 to allow more concurrency with a reasonable buffer
RATE_LIMIT_DELAY = 1.5
# Cache TTL in seconds (5 minutes)
CACHE_TTL = 300

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
    # Use a semaphore to limit concurrent API requests to avoid rate limiting
    semaphore = asyncio.Semaphore(2)  # Allow 2 concurrent requests to TikTok API
    
    async with TikTokApi() as api:
        logger.info("Creating TikTokApi session to fetch song info")
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, browser=os.getenv("TIKTOK_BROWSER", "webkit"))
        
        async def process_video(url):
            """Inner function to process a single video"""
            try:
                # Use the semaphore to control concurrency
                async with semaphore:
                    # First extract the video ID from the URL
                    video_id = url.split("/video/")[1].split("?")[0]
                    logger.info(f"Processing video ID: {video_id}")
                    
                    # Get video info which contains the music info
                    # We need to set both the ID and the URL according to the error message
                    video_obj = api.video(id=video_id, url=url)
                    video = await video_obj.info()
                    
                    # Log the response structure for debugging
                    logger.debug(f"Video response type: {type(video)}")
                    logger.debug(f"Video response keys: {video.keys() if isinstance(video, dict) else 'Not a dict'}")
                    
                    # Check if the response indicates an error
                    if isinstance(video, dict) and video.get('statusCode') == 100004:
                        logger.warning(f"TikTok API returned status code 100004 for video {video_id}. This likely indicates a rate limit or authentication issue.")
                        return None
                    
                    # Try to access music information based on the API structure
                    if isinstance(video, dict):
                        # Check standard path first
                        if "music" in video:
                            music_data = video["music"]
                        # Check if music might be nested in another field
                        elif "itemInfo" in video and "itemStruct" in video["itemInfo"] and "music" in video["itemInfo"]["itemStruct"]:
                            music_data = video["itemInfo"]["itemStruct"]["music"]
                        else:
                            logger.warning(f"No music data found in expected locations for {url}")
                            return None
                            
                        logger.info(f"Retrieved music data structure: {type(music_data)}")
                        
                        # Safe extraction of music data
                        song_info = {
                            "title": music_data.get("title", "Unknown Title"),
                            "author": music_data.get("authorName", music_data.get("author", "Unknown Artist")),
                            "id": music_data.get("id", ""),
                            "play_url": music_data.get("playUrl", music_data.get("play_url", "")),
                            "cover_url": music_data.get("coverLarge", music_data.get("cover", "")),
                            "duration": music_data.get("duration", 0),
                            "video_url": url
                        }
                        logger.info(f"Successfully processed song: {song_info['title']}")
                        return song_info
                    else:
                        logger.warning(f"Unexpected response type for {url}: {type(video)}")
                        return None
                    
                    # Add a small delay to avoid hitting rate limits
                    await asyncio.sleep(RATE_LIMIT_DELAY)
            except Exception as e:
                logger.warning(f"Failed to fetch song info for {url}: {str(e)}")
                import traceback
                logger.debug(f"Detailed error: {traceback.format_exc()}")
                # Log more details about the error to help diagnose issues
                if "url" in str(e).lower():
                    logger.error(f"URL-related error with video {video_id}. URL format: {url}")
                elif "rate" in str(e).lower() or "limit" in str(e).lower():
                    logger.error(f"Possible rate limiting issue. Consider increasing RATE_LIMIT_DELAY (currently {RATE_LIMIT_DELAY}s)")
                elif "token" in str(e).lower() or "auth" in str(e).lower():
                    logger.error(f"Possible authentication issue. Check your ms_token configuration")
                return None
        
        # Process videos concurrently
        tasks = [process_video(url) for url in video_urls]
        results = await asyncio.gather(*tasks)
        
        # Filter out None results and add valid song infos to the list
        song_infos = [result for result in results if result is not None]
    
    return song_infos

async def get_songs_by_hashtag(keyword: str, count: int = 10, max_videos: int = 5):
    # Create a cache key based on the hashtag and count
    cache_key = f"hashtag_songs_{keyword.lower()}_{max_videos}"
    
    # Try to get from cache first
    cached_result = cache.get(cache_key)
    if cached_result:
        logger.info(f"Using cached song results for hashtag: {keyword}")
        return cached_result
        
    # If not in cache, fetch fresh data
    try:
        video_urls = await fetch_hashtag_video_urls(keyword)
        if not video_urls:
            logger.warning(f"No video URLs found for hashtag: {keyword}")
            return []
            
        # Limit to the first max_videos (default 5) to prevent rate limiting issues
        limited_urls = video_urls[:max_videos]
        logger.info(f"Processing {len(limited_urls)} out of {len(video_urls)} available videos")
        song_infos = await get_song_info_from_videos(limited_urls)
        
        # Store in cache for future requests
        if song_infos and len(song_infos) > 0:
            logger.info(f"Found song: {song_infos[0]['title']} by {song_infos[0]['author']}")
            cache.set(cache_key, song_infos, CACHE_TTL)
            return song_infos
        else:
            logger.warning(f"No song information found for videos with hashtag: {keyword}")
            return []
    except Exception as e:
        logger.error(f"Error in get_songs_by_hashtag: {str(e)}")
        return []
    else:
        logger.warning(f"No songs found for hashtag: {keyword}")
        
    return song_infos

