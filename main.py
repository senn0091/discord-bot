import os
from flask import Flask, redirect, request

app = Flask(__name__)

CLIENT_ID = "1563561279363489932"
REDIRECT_URI = "https://discord-bot-mafc.onrender.com/callback"


# 👇 이 부분이 있어야 주소만 딱 쳤을 때 404가 안 뜨고 정상 문구가 나옵니다!
@app.route("/")
def home():
  return "Discord Bot Server is Live!"


# 👇 로그인 버튼을 눌렀을 때 작동하는 주소
@app.route("/login")
def login():
  discord_url = f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify"
  return redirect(discord_url)


# 👇 인증 완료 후 돌아오는 주소
@app.route("/callback")
def callback():
  code = request.args.get("code")
  return f"인증이 성공적으로 완료되었습니다! (코드: {code})"


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
