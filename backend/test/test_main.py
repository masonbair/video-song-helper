import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import status
from unittest.mock import patch, AsyncMock
from backend.src.api import app

@pytest.mark.asyncio
async def test_force_token_refresh_success():
    with patch("src.main.validate_and_refresh_token", new=AsyncMock(return_value=True)):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/api/token/refresh")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "success"
        assert "Token refreshed successfully" in response.json()["message"]

@pytest.mark.asyncio
async def test_force_token_refresh_warning():
    with patch("src.main.validate_and_refresh_token", new=AsyncMock(return_value=False)):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/api/token/refresh")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "warning"
        assert "validation failed" in response.json()["message"]

@pytest.mark.asyncio
async def test_force_token_refresh_exception():
    with patch("src.main.validate_and_refresh_token", new=AsyncMock(side_effect=Exception("fail"))):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.post("/api/token/refresh")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Token refresh failed" in response.json()["detail"]

@pytest.mark.asyncio
async def test_get_token_status():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/token/status")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "has_manual_token" in data
    assert "auto_generation_enabled" in data

@pytest.mark.asyncio
async def test_test_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/test")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Backend is running!"}

@pytest.mark.asyncio
async def test_receive_data():
    payload = {"idea": "Test idea"}
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/data", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["receivedIdea"] == "Test idea"
    assert "timestamp" in data

@pytest.mark.asyncio
async def test_get_recommendations():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/recommendations")
    assert response.status_code == status.HTTP_200_OK
    assert "recommendations" in response.json()
    assert isinstance(response.json()["recommendations"], list)

@pytest.mark.asyncio
async def test_add_recommendation():
    payload = {
        "title": "Song Title",
        "artist": "Artist Name",
        "genre": "Pop",
        "link": "http://example.com"
    }
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/recommendations", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "recommendation" in data
    assert data["recommendation"]["title"] == "Song Title"

@pytest.mark.asyncio
async def test_get_trending_videos_success():
    # Patch both validate_and_refresh_token and trending_videos_with_auto_token
    with patch("src.main.validate_and_refresh_token", new=AsyncMock(return_value=True)), \
         patch("src.main.trending_videos_with_auto_token", new=AsyncMock(return_value=[{"id": 1}, {"id": 2}])):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/api/tiktok/trending")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "videos" in data
        assert data["count"] == 2

@pytest.mark.asyncio
async def test_get_trending_videos_failure():
    with patch("src.main.validate_and_refresh_token", new=AsyncMock(return_value=True)), \
         patch("src.main.trending_videos_with_auto_token", new=AsyncMock(side_effect=Exception("fail"))):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            response = await ac.get("/api/tiktok/trending")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Error fetching trending videos" in response.json()["detail"]