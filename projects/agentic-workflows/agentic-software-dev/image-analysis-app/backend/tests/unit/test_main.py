import pytest
from httpx import AsyncClient
from main import app
from PIL import Image
import io

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_analyze_image_success():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Create a dummy image
        img = Image.new('RGB', (60, 30), color = 'red')
        byte_arr = io.BytesIO()
        img.save(byte_arr, format='PNG')
        byte_arr.seek(0)

        response = await ac.post("/analyze-image/", files={
            "file": ("test_image.png", byte_arr.getvalue(), "image/png")
        })
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["filename"] == "test_image.png"
    assert "explanation" in json_response
    assert "segmented_image" in json_response

@pytest.mark.asyncio
async def test_analyze_image_invalid_file_type():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Create a dummy text file
        response = await ac.post("/analyze-image/", files={
            "file": ("test.txt", b"hello world", "text/plain")
        })
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid file type. Please upload an image."
}
