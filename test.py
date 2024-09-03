import asyncio
from io import BytesIO
from httpx import AsyncClient

async def main():
    files = [
        ("files", ("newfile.txt", BytesIO(b"secret omlette recipe"), "text/plain")),
    ]
    async with AsyncClient() as client:
        response = await client.post("http://localhost:8000/api/v1/uploadfiles/", files=files)
        print(response.status_code)
        print(response.text)

# Run the asynchronous function
asyncio.run(main())