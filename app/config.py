from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

STARLINE_LOGIN = os.getenv("STARLINE_LOGIN")
STARLINE_PASSWORD = os.getenv("STARLINE_PASSWORD")

STARLINE_CLIENT_ID = os.getenv("STARLINE_CLIENT_ID")
STARLINE_CLIENT_SECRET = os.getenv("STARLINE_CLIENT_SECRET")

PROXY_URL = os.getenv("PROXY_URL")