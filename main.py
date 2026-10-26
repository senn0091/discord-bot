import os
from flask import Flask, jsonify, redirect, request

app = Flask(__name__)

CLIENT_ID = "1563561279363489932"
REDIRECT_URI = "https://discord-bot-mafc.onrender.com/callback"


@app.route("/")
def home():
  return """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>Discord Bot Server</title>
        <style>
            body { background-color: #313338; color: #ffffff; font-family: sans-serif; text-align: center; margin-top: 100px; }
            h1 { color: #57f287; }
        </style>
    </head>
    <body>
        <h1>Discord Bot Server is Live!</h1>
        <p>백엔드 서버가 정상적으로 작동 중입니다.</p>
    </body>
    </html>
    """


@app.route("/login")
def login():
  discord_url = (
      "https://discord.com/api/oauth2/authorize"
      f"?client_id={CLIENT_ID}"
      f"&redirect_uri={REDIRECT_URI}"
      "&response_type=code"
      "&scope=identify"
  )
  return redirect(discord_url, code=302)


@app.route("/callback")
def callback():
  code = request.args.get("code")

  if not code:
    return """
        <div style="text-align: center; margin-top: 50px; font-family: sans-serif;">
            <h2 style="color: #ed4245;">⚠️ 잘못된 접근입니다</h2>
            <p>디스코드 봇의 [인증하기] 버튼을 통해 접속해 주세요.</p>
        </div>
        """, 400

  return """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>인증 완료</title>
        <style>
            body {
                background-color: #313338;
                color: #ffffff;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .card {
                background-color: #2b2d31;
                padding: 40px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                max-width: 90%;
                width: 350px;
            }
            .icon { font-size: 50px; margin-bottom: 10px; }
            h1 { color: #57f287; font-size: 24px; margin-bottom: 10px; }
            p { color: #b5bac1; font-size: 14px; line-height: 1.5; }
        </style>
    </head>
    <body>
        <div class="card">
            <div class="icon">✅</div>
            <h1>인증이 완료되었습니다!</h1>
            <p>서버 유저 안전 인증이 성공적으로 처리되었습니다.<br>이 창을 닫으셔도 좋습니다.</p>
        </div>
    </body>
    </html>
    """


@app.route("/api/recover", methods=["GET", "POST"])
def api_recover():
  guild_id = request.args.get("guild_id")
  return jsonify({
      "status": "success",
      "guild_id": guild_id,
      "message": "Recovery successfully executed.",
  })


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
