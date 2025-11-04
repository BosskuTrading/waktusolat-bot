import os
def home():
    return "WaktuSolat Bot aktif", 200




@app.route("/payment", methods=["POST"]) # Billplz will POST here
def billplz_payment_webhook():
# Billplz sends form-encoded data. Convert to dict.
data = request.form.to_dict()


# Optional: verify secret if you set one in Billplz dashboard
# Example: Billplz does not by default sign payloads; but you can include a hidden field in the payment form
# that you check here (e.g. a known token). For now we accept the POST.


# Write raw payload to log for debugging (Railway logs)
app.logger.info("Billplz webhook payload: %s", json.dumps(data))


# Billplz sends 'paid' == 'true' when payment confirmed
paid = data.get("paid")
if paid == "true":
# Extract useful fields
payer_name = data.get("name") or "Dermawan"
payer_email = data.get("email") or ""
# Billplz amount is in cents (or sen) - depends on integration; often integer as sen
raw_amount = data.get("amount")
try:
amount = int(raw_amount) / 100.0 if raw_amount is not None else 0.0
except Exception:
# fallback
amount = 0.0


# Message to admin
msg_admin = (
f"💖 Derma diterima!\n\n"
f"Nama: {payer_name}\n"
f"Emel: {payer_email}\n"
f"Jumlah: RM{amount:.2f}\n"
f"Bill ID: {data.get('id')}\n"
)


# Try to thank donor directly via Telegram if they provided telegram_id or telegram_username in the payment form
# You need to add a custom field in your Billplz Payment Form for "telegram_id" or "telegram_username"
telegram_id = data.get("telegram_id") # ideally chat_id
telegram_username = data.get("telegram_username")


try:
if telegram_id:
# send direct thank you to chat id
bot.send_message(chat_id=int(telegram_id), text=f"Terima kasih {payer_name} atas sumbangan RM{amount:.2f}! 🤲")
elif telegram_username:
# try to send by @username (may fail if privacy prevents)
bot.send_message(chat_id=telegram_username, text=f"Terima kasih {payer_name} atas sumbangan RM{amount:.2f}! 🤲")


# also inform admin
if ADMIN_CHAT_ID:
bot.send_message(chat_id=int(ADMIN_CHAT_ID), text=msg_admin)
except Exception as e:
app.logger.error("Gagal hantar mesej Telegram: %s", str(e))
# still notify admin about failure
if ADMIN_CHAT_ID:
bot.send_message(chat_id=int(ADMIN_CHAT_ID), text=msg_admin + "\n(Gagal hantar terus ke donor via Telegram)")


return "OK", 200




# ------------------------- Run (for local dev) -------------------------
if __name__ == "__main__":
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))