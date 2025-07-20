from flask import Flask, request, jsonify
from pywebpush import webpush, WebPushException
import json

app = Flask(__name__)

# VAPID 키는 본인의 키로 교체하세요
VAPID_PUBLIC_KEY = "YOUR_PUBLIC_VAPID_KEY"
VAPID_PRIVATE_KEY = "YOUR_PRIVATE_VAPID_KEY"
VAPID_CLAIMS = {"sub": "mailto:your@email.com"}

subscriptions = []

@app.route("/save-subscription", methods=["POST"])
def save_subscription():
    sub = request.get_json()
    subscriptions.append(sub)
    print("✅ 새 구독 저장됨:", sub)
    return jsonify({"status": "saved"}), 201

@app.route("/send-push", methods=["POST"])
def send_push():
    payload = {
        "title": "📢 월드잡 공지",
        "body": "새로운 공지사항이 등록되었습니다!"
    }

    for sub in subscriptions:
        try:
            webpush(
                subscription_info=sub,
                data=json.dumps(payload),
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims=VAPID_CLAIMS
            )
            print("✅ 알림 전송 완료")
        except WebPushException as e:
            print("❌ 푸시 실패:", e)

    return jsonify({"status": "sent"}), 200

if __name__ == "__main__":
    app.run(port=5000)
