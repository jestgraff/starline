import httpx
from app.config import (
    STARLINE_LOGIN,
    STARLINE_PASSWORD,
    STARLINE_CLIENT_ID,
    STARLINE_CLIENT_SECRET
)


class StarLineAPI:

    def __init__(self):
        self.access_token = None
        self.refresh_token = None

    async def authenticate(self):

        url = "https://id.starline.ru/realms/starline/protocol/openid-connect/token"

        data = {
            "grant_type": "password",
            "username": STARLINE_LOGIN,
            "password": STARLINE_PASSWORD,
            "client_id": STARLINE_CLIENT_ID,
            "client_secret": STARLINE_CLIENT_SECRET,
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        timeout = httpx.Timeout(30.0)
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                data=data,
                headers=headers
            )

        print(response.text)

        response.raise_for_status()

        result = response.json()

        self.access_token = result["access_token"]
        self.refresh_token = result.get("refresh_token")

    async def get_headers(self):

        if not self.access_token:
            await self.authenticate()

        return {
            "Authorization": f"Bearer {self.access_token}"
        }

    async def get_devices(self):

        headers = await self.get_headers()

        url = "https://developer.starline.ru/json/v2/device"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        response.raise_for_status()

        return response.json()

    async def get_device_data(self, device_id):

        headers = await self.get_headers()

        url = f"https://developer.starline.ru/json/v2/device/{device_id}/data"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

        response.raise_for_status()

        return response.json()