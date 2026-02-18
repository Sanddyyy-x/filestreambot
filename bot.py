from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from database import save_file
import os

# ===== Load Environment Variables Safely =====
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Clean BASE_URL safely
BASE_URL = os.getenv("BASE_URL", "").strip().rstrip("/")

# ===== Create Bot Client =====
app = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ===== Handle Files =====
@app.on_message(filters.document | filters.video | filters.audio)
async def handle_file(client, message):

    file_id = None
    file_name = None

    # Detect file type properly
    if message.document:
        file_id = message.document.file_id
        file_name = message.document.file_name

    elif message.video:
        file_id = message.video.file_id
        file_name = message.video.file_name or "video.mp4"

    elif message.audio:
        file_id = message.audio.file_id
        file_name = message.audio.file_name or "audio.mp3"

    if not file_id:
        return

    # Save file in database
    unique_id = save_file(file_id, file_name)

    # Generate clean link
    link = f"{BASE_URL}/download/{unique_id}"

    # Send formatted message (Pyrogram v2 correct way)
    await message.reply_text(
        f"✅ **File Stored Successfully!**\n\n"
        f"📁 **File Name:** `{file_name}`\n\n"
        f"🔗 [Click Here to Download]({link})",
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )

# ===== Run Bot =====
app.run()

