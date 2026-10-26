import os
from flask import Flask, redirect, request

app = Flask(__name__)

CLIENT_ID = "1563561279363489932"
REDIRECT_URI = "https://discord-bot-mafc.onrender.com/callback"


@app.route("/")
def home():
  return "Discord Bot Server is Live!"


@app.route("/login")
def login():
  discord_url = f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify"
  return redirect(discord_url)


@app.route("/callback")
def callback():
  code = request.args.get("code")
  # 코드가 없이 그냥 들어온 경우의 안전장치
  if not code:
    return (
        "잘못된 접근입니다. 디스코드 봇의 [인증하기] 버튼을 통해서만 이용해"
        " 주세요."
    )
  return f"인증이 성공적으로 완료되었습니다! (인증 코드: {code})"


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
