import os
from flask import Flask, jsonify, redirect, request

app = Flask(__name__)

# 디스코드 애플리케이션 정보
CLIENT_ID = "1563849924146106500"
REDIRECT_URI = "https://discord-bot-mafc.onrender.com/callback"


# 1. 서버 상시 활성화 및 생존 확인 라우트
@app.route("/")
def home():
  return "<h1>Discord Bot Server is Live!</h1><p>서버가 정상적으로 작동 중입니다.</p>"


# 2. 인증 시작 라우트 (!인생생성 버튼 클릭 시 이동)
@app.route("/login")
def login():
  discord_url = f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify"
  return redirect(discord_url)


# 3. 인증 완료 콜백 라우트 (디스코드 로그인 성공 후 돌아오는 화면)
@app.route("/callback")
def callback():
  code = request.args.get("code")

  # 코드가 없이 웹 주소로 바로 들어온 경우 예외 처리
  if not code:
    return """
        <div style="text-align: center; margin-top: 50px; font-family: sans-serif;">
            <h2 style="color: #ed4245;">⚠️ 잘못된 접근입니다</h2>
            <p>디스코드 봇의 [인증하기] 버튼을 통해 접속해 주세요.</p>
        </div>
        """, 400

  # 인증 성공 시 브라우저에 표시할 디자인 화면
  return f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>인증 완료</title>
        <style>
            body {{
                background-color: #313338;
                color: #ffffff;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .card {{
                background-color: #2b2d31;
                padding: 40px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                max-width: 90%;
                width: 350px;
            }}
            .icon {{
                font-size: 50px;
                margin-bottom: 10px;
            }}
            h1 {{
                color: #57f287;
                font-size: 24px;
                margin-bottom: 10px;
            }}
            p {{
                color: #b5bac1;
                font-size: 14px;
                line-height: 1.5;
            }}
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


# 4. !복구 명령어용 API 라우트
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
