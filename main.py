import os
from flask import Flask, redirect, request

app = Flask(__name__)

# 디스코드 개발자 센터에 등록한 클라이언트 ID
CLIENT_ID = "1563561279363489932"
REDIRECT_URI = "https://discord-bot-mafc.onrender.com/callback"


@app.route("/")
def home():
  return "Discord Bot Server is Live!"


# 👇 버튼을 눌렀을 때 디스코드 로그인 페이지로 보내주는 역할
@app.route("/login")
def login():
  discord_url = f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify"
  return redirect(discord_url)


# 👇 로그인이 끝나고 돌아오는 곳
@app.route("/callback")
def callback():
  code = request.args.get("code")
  return f"인증이 성공적으로 완료되었습니다! (코드: {code})"


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
