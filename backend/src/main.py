from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from datetime import datetime, timedelta, UTC
from TikTokApi import TikTokApi
import asyncio
import os
import logging
from typing import Optional

load_dotenv()

app = FastAPI(title="Song Recommendation API")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Token management
ms_token = os.environ.get("ms_token", None)
last_token_refresh = None
token_refresh_interval = timedelta(hours=6)  # Refresh every 6 hours

# Pydantic models
class Recommendation(BaseModel):
    title: str
    artist: str
    genre: str
    link: str

class RecommendationResponse(BaseModel):
    recommendation: Recommendation

class IdeaData(BaseModel):
    idea: str

class TokenStatus(BaseModel):
    has_manual_token: bool
    auto_generation_enabled: bool
    last_refresh: Optional[str] = None
    next_refresh: Optional[str] = None

# Enhanced TikTok function with automatic token management
async def trending_videos_with_auto_token():
    """
    Fetch trending videos with automatic token management
    Falls back to auto-generation if manual token fails
    """
    global last_token_refresh

    

    try:
        # First try with manual token if available
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
    
    # Fallback to automatic token generation
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

# Token validation function
async def validate_and_refresh_token():
    """
    Validate current token and refresh if needed
    """
    global last_token_refresh
    
    now = datetime.now()
    logger.info("Checking if token refresh is needed...")
    
    # Check if we need to refresh based on time
    if (last_token_refresh is None or 
        (now - last_token_refresh) > token_refresh_interval):
        
        logger.info("Token refresh needed, testing connection...")
        try:
            # Test with a small request
            async with TikTokApi() as api:
                if ms_token:
                    logger.info("Creating session with manual ms_token")
                    await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, browser=os.getenv("TIKTOK_BROWSER", "webkit"))
                else:
                    logger.info("Creating session with auto-generated token")
                    await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3, browser=os.getenv("TIKTOK_BROWSER", "webkit"))
                
                # Try to fetch just 1 video to test
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

@app.get("/api/token/status")
async def get_token_status():
    """Get current token status and refresh information"""
    global last_token_refresh
    
    next_refresh = None
    if last_token_refresh:
        next_refresh = (last_token_refresh + token_refresh_interval).isoformat()
    
    return TokenStatus(
        has_manual_token=ms_token is not None,
        auto_generation_enabled=True,
        last_refresh=last_token_refresh.isoformat() if last_token_refresh else None,
        next_refresh=next_refresh
    )

@app.post("/api/token/refresh")
async def force_token_refresh():
    """Force a token refresh and validation"""
    try:
        is_valid = await validate_and_refresh_token()
        if is_valid:
            return {"status": "success", "message": "Token refreshed successfully"}
        else:
            return {"status": "warning", "message": "Token refresh attempted but validation failed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Token refresh failed: {str(e)}")

@app.get("/api/test")
async def test_endpoint():
    return {"message": "Backend is running!"}

@app.post("/api/data")
async def receive_data(data: IdeaData):
    return {
        "receivedIdea": data.idea,
        "timestamp": datetime.now(UTC).isoformat() + "Z"
    }

@app.get("/api/tiktok/trending")
async def get_trending_videos():
    """Get trending TikTok videos with automatic token management"""
    logger.info("Received request for trending TikTok videos")
    try:
        # Validate token before making request
        logger.info("Validating and refreshing token if needed...")
        await validate_and_refresh_token()
        
        logger.info("Fetching trending videos from TikTokApi...")
        videos_data = await trending_videos_with_auto_token()
        logger.info(f"Fetched {len(videos_data)} trending videos successfully")
        
        try:
            # Clean up videos_data before returning
            recommendations = [
                {
                    "title": video.get("music", {}).get("title") or video.get("desc", "No Title"),
                    "artist": video.get("music", {}).get("authorName", "Unknown Artist"),
                    "genre": video.get("music", {}).get("genre", "Unknown Genre"),
                    "link": f"https://www.tiktok.com/@{video.get('author', {}).get('uniqueId', '')}/video/{video.get('id', '')}"
                }
                for video in videos_data
            ]
        except Exception as e:
            logger.error(f"Error processing recommendations: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Error processing recommendations: {str(e)}")
        return {
            "recommendations": recommendations,
            "count": len(recommendations),
            "token_status": "auto-managed",
            "timestamp": datetime.now(UTC).isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching trending videos: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching trending videos: {str(e)}")

@app.get("/api/recommendations")
async def get_recommendations():
    """Get song recommendations - placeholder for now"""
    try:
        # TODO: Implement recommendation logic using TikTok data
        recommendations = []
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error fetching recommendations")

@app.post("/api/recommendations", response_model=RecommendationResponse)
async def add_recommendation(recommendation: Recommendation):
    try:
        # TODO: Implement recommendation storage logic (database, etc.)
        return {"recommendation": recommendation}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error adding recommendation")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)