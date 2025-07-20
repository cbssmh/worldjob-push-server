from flask import Flask, request, jsonify
from pywebpush import webpush, WebPushException
import json

app = Flask(__name__)

# VAPID 키는 본인의 키로 교체하세요
VAPID_PUBLIC_KEY = "BMK1KKzPuYH2DOWZzOiTxzrSTksoDwffyOLNBkJMEFLDx7L0LdY3Ktny7jY4xMUGU55mV95sA7O82hXerWBf0Ho"
VAPID_PRIVATE_KEY = "KJw3k_Hz4Kxv_FX7ZfTzZTj8UQ5HRr1mFow1vBDwEos"
VAPID_CLAIMS = {"sub": "mailto:cbssmh@email.com"}


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
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
