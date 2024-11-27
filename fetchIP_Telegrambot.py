import asyncio
import signal
import sys
import requests

async def get_public_ip():
    try:
        response = requests.get("https://ifconfig.me", timeout=5)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return None
    except Exception:
        return None

async def send_telegram_message(bot_token, chat_id, current_ip):
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': f"New Public IP: {current_ip}"
        }
        response = requests.post(url, data=payload)
        return response.status_code == 200
    except Exception:
        return False

async def main():
    BOT_TOKEN = '<YOUR BOT TOKEN>'
    CHAT_ID = '<YOUR USER ID>'

    last_ip = None

    # Signal handler for graceful shutdown
    def handle_exit_signal(signal, frame):
        sys.exit(0)

    signal.signal(signal.SIGTERM, handle_exit_signal)
    signal.signal(signal.SIGINT, handle_exit_signal)

    while True:
        current_ip = await get_public_ip()
        if current_ip and current_ip != last_ip:
            last_ip = current_ip
            await send_telegram_message(BOT_TOKEN, CHAT_ID, current_ip)
        await asyncio.sleep(1800)  # Wait for 30 minutes before checking again

if __name__ == '__main__':
    asyncio.run(main()) 
