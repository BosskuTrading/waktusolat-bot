from flask import Flask, request
import os
import telegram

# Inisialisasi Flask
app = Flask(__name__)

# ✅ Route asas untuk semak status bot
@app.route('/')
def home():
    return "✅ WaktuSolat Bot aktif dan berjalan di Railway", 200


# ✅ Webhook Telegram
@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    try:
        data = request.get_json()
        print("📩 Update Telegram diterima:", data)

        # Proses mesej masuk dari Telegram
        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            text = data["message"].get("text", "")

            # Contoh respons asas
            if text.lower() == "/start":
                message = (
                    "Assalamualaikum 👋\n"
                    "Ini bot *Waktu Solat Malaysia* 🇲🇾\n\n"
                    "📅 Bot ini akan beri peringatan waktu solat harian.\n"
                    "💰 Sokong pembangunan bot ini melalui pautan derma:\n"
                    f"{os.getenv('BILLPLZ_URL')}"
                )
                bot = telegram.Bot(token=os.getenv("TELEGRAM_TOKEN"))
                bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")

        return "ok", 200

    except Exception as e:
        print("❌ Ralat Telegram webhook:", e)
        return "error", 500


# ✅ Webhook Billplz (ucapan terima kasih automatik)
@app.route('/billplz-webhook', methods=['POST'])
def billplz_webhook():
    try:
        data = request.form.to_dict()
        print("💰 Billplz webhook diterima:", data)

        # Contoh: Jika payment berjaya
        if data.get("paid") == "true":
            telegram_chat_id = os.getenv("ADMIN_CHAT_ID")  # optional
            bot = telegram.Bot(token=os.getenv("TELEGRAM_TOKEN"))

            if telegram_chat_id:
                bot.send_message(
                    chat_id=telegram_chat_id,
                    text="🤝 Terima kasih atas sumbangan anda kepada sistem Waktu Solat 🙏"
                )

        return "received", 200

    except Exception as e:
        print("❌ Ralat Billplz webhook:", e)
        return "error", 500


# ✅ Jalankan app Flask
if __name__ == '__main__':
    print("🚀 WaktuSolat Bot sedang berjalan di Railway...")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
