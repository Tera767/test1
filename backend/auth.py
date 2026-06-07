from fastapi import APIRouter
from fastapi.responses import RedirectResponse
import httpx, os
from dotenv import load_dotenv
from jose import jwt
from datetime import datetime, timedelta

load_dotenv()

router = APIRouter()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
JWT_SECRET = os.getenv("JWT_SECRET")

@router.get("/auth/login")
def login():
    url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        "&response_type=code"
        "&scope=openid email profile"
    )
    return RedirectResponse(url)

@router.get("/auth/callback")
async def callback(code: str):
    async with httpx.AsyncClient() as client:
        # แลก code → token
        token_res = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": REDIRECT_URI,
                "grant_type": "authorization_code",
            }
        )
        tokens = token_res.json()

        # ดึงข้อมูล user
        user_res = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {tokens['access_token']}"}
        )
        user = user_res.json()

    # สร้าง JWT ของตัวเอง
    payload = {
        "sub": user["id"],
        "email": user["email"],
        "name": user["name"],
        "picture": user["picture"],
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    # ส่ง token กลับไป React
    return RedirectResponse(f"https://test1-v6lz.vercel.app/dashboard?token={token}")