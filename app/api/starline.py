import hashlib
import httpx

from app.config import (
    STARLINE_LOGIN,
    STARLINE_PASSWORD,
    STARLINE_CLIENT_ID,
    STARLINE_CLIENT_SECRET,
)


class StarLineAPI:
    BASE_ID = "https://id.starline.ru/apiV3"
    BASE_API = "https://developer.starline.ru/json"

    def __init__(self):
        self.slnet_token = None
        self.user_id = None

    async def _client(self):
        return httpx.AsyncClient(timeout=httpx.Timeout(30.0))

    async def get_app_code(self) -> str:
        url = f"{self.BASE_ID}/application/getCode/"
        params = {
            "appId": STARLINE_CLIENT_ID,
            "secret": hashlib.md5(
                STARLINE_CLIENT_SECRET.encode("utf-8")
            ).hexdigest(),
        }

        async with await self._client() as client:
            r = await client.get(url, params=params)

        r.raise_for_status()
        data = r.json()

        if int(data["state"]) != 1:
            raise RuntimeError(data)

        return data["desc"]["code"]

    async def get_app_token(self, app_code: str) -> str:
        url = f"{self.BASE_ID}/application/getToken/"
        params = {
            "appId": STARLINE_CLIENT_ID,
            "secret": hashlib.md5(
                (STARLINE_CLIENT_SECRET + app_code).encode("utf-8")
            ).hexdigest(),
        }

        async with await self._client() as client:
            r = await client.get(url, params=params)

        r.raise_for_status()
        data = r.json()

        if int(data["state"]) != 1:
            raise RuntimeError(data)

        return data["desc"]["token"]

    async def get_slid_user_token(self, app_token: str) -> str:
        url = f"{self.BASE_ID}/user/login/"
        params = {"token": app_token}
        form = {
            "login": STARLINE_LOGIN,
            "pass": hashlib.sha1(
                STARLINE_PASSWORD.encode("utf-8")
            ).hexdigest(),
        }

        async with await self._client() as client:
            r = await client.post(url, params=params, data=form)

        r.raise_for_status()
        data = r.json()

        if int(data["state"]) != 1:
            raise RuntimeError(data)

        return data["desc"]["user_token"]

    async def get_slnet_token_and_user_id(self, slid_token: str):
        url = f"{self.BASE_API}/v2/auth.slid"
        payload = {"slid_token": slid_token}

        async with await self._client() as client:
            r = await client.post(url, json=payload)

        r.raise_for_status()
        data = r.json()

        slnet = r.cookies.get("slnet")
        if not slnet:
            raise RuntimeError(f"No slnet cookie. Response: {data}")

        self.slnet_token = slnet
        self.user_id = data["user_id"]

    async def authenticate(self):
        app_code = await self.get_app_code()
        app_token = await self.get_app_token(app_code)
        slid_token = await self.get_slid_user_token(app_token)
        await self.get_slnet_token_and_user_id(slid_token)

    async def ensure_auth(self):
        if not self.slnet_token or not self.user_id:
            await self.authenticate()

    async def get_user_data(self):
        await self.ensure_auth()

        url = f"{self.BASE_API}/v3/user/{self.user_id}/data"
        headers = {"Cookie": f"slnet={self.slnet_token}"}

        async with await self._client() as client:
            r = await client.get(url, headers=headers)

        r.raise_for_status()
        return r.json()

    async def get_device_data(self, device_id: int | str):
        await self.ensure_auth()

        url = f"{self.BASE_API}/v3/device/{device_id}/data"
        headers = {"Cookie": f"slnet={self.slnet_token}"}

        async with await self._client() as client:
            r = await client.get(url, headers=headers)

        r.raise_for_status()
        return r.json()