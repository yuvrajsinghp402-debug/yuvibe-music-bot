import os
import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls, idle

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]

app = Client(
    "yuvibe",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

calls = PyTgCalls(app)

@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text(
        "𓆩 𝖄𝖀𝖁𝕴𝕭𝕰 𓆪 🖤\n"
        "Welcome to YUVIBE MUSIC 🎧\n"
        "Use /play <audio_url> to start music."
    )

@app.on_message(filters.command("play"))
async def play(_, message):
    if len(message.command) < 2:
        await message.reply_text(
            "Usage: /play <direct_audio_url>"
        )
        return

    url = message.text.split(maxsplit=1)[1]

    try:
        await calls.play(message.chat.id, url)
        await message.reply_text("🎶 YUVIBE is playing!")
    except Exception as e:
        await message.reply_text(
            f"Playback failed: {type(e).__name__}\n"
            "Make sure a group voice chat is active and "
            "the URL is a supported direct audio stream."
        )

@app.on_message(filters.command("pause"))
async def pause(_, message):
    try:
        await calls.pause(message.chat.id)
        await message.reply_text("⏸️ Music paused.")
    except Exception as e:
        await message.reply_text(f"Pause failed: {type(e).__name__}")

@app.on_message(filters.command("resume"))
async def resume(_, message):
    try:
        await calls.resume(message.chat.id)
        await message.reply_text("▶️ Music resumed.")
    except Exception as e:
        await message.reply_text(f"Resume failed: {type(e).__name__}")

@app.on_message(filters.command("stop"))
async def stop(_, message):
    try:
        await calls.leave_call(message.chat.id)
        await message.reply_text("⏹️ Music stopped.")
    except Exception as e:
        await message.reply_text(f"Stop failed: {type(e).__name__}")

async def main():
    await app.start()
    calls.start()
    print("YUVIBE is online!")
    await idle()
    await calls.stop()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
