from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from datetime import datetime, UTC, timedelta
import logging
import os

from src.models import Recommendation, RecommendationResponse, IdeaData, TokenStatus
from src.tiktok_service import trending_videos_with_auto_token, get_songs_by_hashtag
from src.token_manager import validate_and_refresh_token

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

@app.get("/api/songs/by-hashtag")
async def songs_by_hashtag():
    """
    Get unique songs used in TikTok videos for a given hashtag/keyword.
    """
    keyword: str = "Travel"
    count: int = 30
    logger.info(f"Attempting to fetch songs for hashtag: {keyword} with count: {count}")
    try:
        songs = await get_songs_by_hashtag(keyword, count)
        return {
            "keyword": keyword,
            "count": len(songs),
            "songs": songs,
            "timestamp": datetime.now(UTC).isoformat()
        }
    except Exception as e:
        logger.error(f"Error fetching songs by hashtag: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching songs by hashtag: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)