from flask import Flask, send_file
from database import get_file
from pyrogram import Client
import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)

bot = Client(
    "server_session",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Start bot once when server starts
bot.start()

@app.route("/download/<unique_id>")
def download(unique_id):
    file_data = get_file(unique_id)

    if not file_data:
        return "File not found"

    file_id = file_data["file_id"]
    original_name = file_data["file_name"]

    # Download file with original filename in /tmp
    file_path = bot.download_media(
        file_id,
        file_name=f"/tmp/{original_name}"
    )

    return send_file(
        file_path,
        as_attachment=True,
        download_name=original_name
    )

