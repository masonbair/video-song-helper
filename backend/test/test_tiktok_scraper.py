import pytest
import asyncio
from src.tiktok_scraper import fetch_hashtag_video_urls

@pytest.mark.asyncio
async def test_fetch_hashtag_video_urls_deduplication():
    """
    Mock test to ensure the deduplication logic works correctly
    """
    # Mock the get_all_hyperlinks_playwright function to return known duplicate URLs
    async def mock_get_all_hyperlinks(url, headless):
        # Return a list of URLs with duplicates (different paths to same video)
        return [
            "https://www.tiktok.com/@user1/video/1234567890123456789?is_copy_url=1&is_from_webapp=v1",
            "https://www.tiktok.com/@user1/video/1234567890123456789", # Same as first
            "https://www.tiktok.com/t/video/1234567890123456789/", # Same ID, different format
            "https://www.tiktok.com/@user2/video/9876543210987654321",
            "https://www.tiktok.com/@user2/video/9876543210987654321?param=test", # Same as fourth
            "https://www.tiktok.com/@user3/video/1122334455667788990",
            "https://www.tiktok.com/tag/somehashtaglink", # Not a video link
            "https://www.tiktok.com/@user4/video/5566778899001122334"
        ]
    
    # Temporarily replace the real function with our mock
    import src.tiktok_scraper
    original_func = src.tiktok_scraper.get_all_hyperlinks_playwright
    src.tiktok_scraper.get_all_hyperlinks_playwright = mock_get_all_hyperlinks
    
    try:
        # Call the function being tested
        result = await fetch_hashtag_video_urls("test")
        
        # Verify that duplicate videos were removed
        assert len(result) == 4, f"Expected 4 unique video URLs, got {len(result)}"
        
        # Verify that all returned URLs contain '/video/'
        for url in result:
            assert '/video/' in url, f"URL does not contain '/video/': {url}"
        
        # Check that we have the expected unique video IDs
        video_ids = set()
        for url in result:
            video_id = url.split('/video/')[1].split('?')[0]
            video_ids.add(video_id)
        
        assert len(video_ids) == 4, f"Expected 4 unique video IDs, got {len(video_ids)}"
        assert "1234567890123456789" in video_ids
        assert "9876543210987654321" in video_ids
        assert "1122334455667788990" in video_ids
        assert "5566778899001122334" in video_ids
        
    finally:
        # Restore the original function
        src.tiktok_scraper.get_all_hyperlinks_playwright = original_func

if __name__ == "__main__":
    asyncio.run(test_fetch_hashtag_video_urls_deduplication())
