import os
import logging
from datetime import datetime, timedelta
from TikTokApi import TikTokApi

ms_token = os.environ.get("ms_token", None)
last_token_refresh = None
token_refresh_interval = timedelta(hours=6)
logger = logging.getLogger(__name__)

async def validate_and_refresh_token():
    global last_token_refresh
    now = datetime.now()
    logger.info("Checking if token refresh is needed...")
    if (last_token_refresh is None or (now - last_token_refresh) > token_refresh_interval):
        logger.info("Token refresh needed, testing connection...")
        try:
            async with TikTokApi() as api:
                if ms_token:
                    logger.info("Creating session with manual ms_token")
                    await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, browser=os.getenv("TIKTOK_BROWSER", "webkit"))
                else:
                    logger.info("Creating session with auto-generated token")
                    await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, browser=os.getenv("TIKTOK_BROWSER", "webkit"))
                async for video in api.trending.videos(count=1):
                    logger.info("Token test fetch successful")
                    break
                last_token_refresh = now
                logger.info("Token validation successful")
                return True
        except Exception as e:
            logger.warning(f"Token validation failed: {e}", exc_info=True)
            return False
    logger.info("Token refresh not needed")
    return True
