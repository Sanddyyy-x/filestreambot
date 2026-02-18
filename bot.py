from pyrogram import Client, filters
from database import save_file
import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL")

app = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.document | filters.video | filters.audio)
async def handle_file(client, message):

    if message.document:
        file_id = message.document.file_id
        file_name = message.document.file_name

    elif message.video:
        file_id = message.video.file_id
        file_name = message.video.file_name

    elif message.audio:
        file_id = message.audio.file_id
        file_name = message.audio.file_name

    else:
        return

    unique_id = save_file(file_id, file_name)

    link = f"{BASE_URL}/download/{unique_id}"

    await message.reply_text(
        f"✅ File Stored!\n\n🔗 Download Link:\n{link}"
    )

app.run()

