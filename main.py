import os
from flask import Flask, jsonify, redirect, request

app = Flask(__name__)

CLIENT_ID = "1563849924146106500"
REDIRECT_URI = "https://discord-bot-mafc.onrender.com/callback"


# 1. 메인 홈 화면 (서버 생존 확인용)
@app.route("/")
def home():
  return "Discord Bot Server is Live!"


# 2. 인증 로그인 주소 (/login)
@app.route("/login")
def login():
  discord_url = f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify"
  return redirect(discord_url)


# 3. 인증 완료 후 돌아오는 주소 (/callback)
@app.route("/callback")
def callback():
  code = request.args.get("code")
  if not code:
    return (
        "잘못된 접근입니다. 디스코드 봇의 [인증하기] 버튼을 통해서만 이용해"
        " 주세요."
    )
  return f"인증이 성공적으로 완료되었습니다! (인증 코드: {code})"


# 4. !복구 명령어가 호출하는 서버 복구 API 주소 (/api/recover)
@app.route("/api/recover", methods=["GET", "POST"])
def api_recover():
  guild_id = request.args.get("guild_id")

  # 이곳에 추후 서버 데이터 복구 처리 로직을 작성할 수 있습니다.
  print(f"🔄 서버 복구 요청 수신됨 - 길드 ID: {guild_id}")

  # BDFD($httpPost)가 결과를 정상적으로 읽을 수 있도록 JSON 응답 반환
  return jsonify({"status": "success", "guild_id": guild_id})


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
