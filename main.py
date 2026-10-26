import os
from flask import Flask, redirect, request

app = Flask(__name__)

# 👇 개발자 센터의 클라이언트 ID와 일치해야 합니다!
CLIENT_ID = "1563849924146106500"
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
  if not code:
    return (
        "잘못된 접근입니다. 디스코드 봇의 [인증하기] 버튼을 통해서만 이용해"
        " 주세요."
    )
  return f"인증이 성공적으로 완료되었습니다! (인증 코드: {code})"


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
