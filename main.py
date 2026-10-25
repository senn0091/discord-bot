from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

# [여기 수정하기!] 디스코드 개발자 사이트에서 가져온 정보 넣기
CLIENT_ID = "여기에_디스코드_클라이언트_ID_숫자"
CLIENT_SECRET = "여기에_디스코드_클라이언트_시크릿"
REDIRECT_URI = "https://너의서버이름.onrender.com/callback"  # 나중에 호스팅 주소로 변경!

DB_FILE = "users_db.json"

# 저장된 유저 정보를 불러오고 저장하는 기능
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@app.route('/')
def home():
    return "서버가 아주 잘 작동하고 있어요!"

# 유저가 인증 버튼을 누르고 돌아왔을 때 작동하는 곳
@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "인증 코드가 없어요!", 400

    # 디스코드에 토큰(입장권) 달라고 요청하기
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    response = requests.post('https://discord.com/api/v10/oauth2/token', data=data, headers=headers)
    token_json = response.json()

    if 'access_token' in token_json:
        access_token = token_json['access_token']
        
        # 유저 아이디 확인하기
        user_headers = {'Authorization': f"Bearer {access_token}"}
        user_res = requests.get('https://discord.com/api/v10/users/@me', headers=user_headers).json()
        user_id = user_res['id']
        username = user_res['username']

        # 데이터 파일에 저장하기
        db = load_db()
        db[user_id] = access_token
        save_db(db)

        return f"<h1>인증 성공!</h1><p>{username}님, 이제 디스코드로 돌아가셔도 돼요.</p>"
    else:
        return "인증에 실패했어요. 다시 시도해 주세요!", 400

# BDFD 앱에서 !복구 명령어를 썼을 때 유저들을 다시 불러오는 기능
@app.route('/api/recover', methods=['POST'])
def recover():
    guild_id = request.args.get('guild_id')
    if not guild_id:
        return {"status": "error"}, 400

    db = load_db()
    bot_token = "여기에_내_디스코드_봇_토큰"
    
    success_count = 0
    for user_id, access_token in db.items():
        url = f"https://discord.com/api/v10/guilds/{guild_id}/members/{user_id}"
        headers = {
            "Authorization": f"Bot {bot_token}",
            "Content-Type": "application/json"
        }
        payload = {"access_token": access_token}
        res = requests.put(url, headers=headers, json=payload)
        
        if res.status_code in [201, 204]:
            success_count += 1

    return {"status": "success", "recovered": success_count}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
