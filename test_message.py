import os
import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
YOUR_USER_ID = os.getenv('YOUR_USER_ID')

async def test_message():
    client = TelegramClient('job_tracker_session', API_ID, API_HASH)
    await client.start()
    
    # Get your actual user
    me = await client.get_me()
    print(f"📱 Logged in as: {me.first_name} (ID: {me.id})")
    print(f"📝 Username: @{me.username if me.username else 'N/A'}")
    print(f"\n🔍 YOUR_USER_ID in .env: {YOUR_USER_ID}")
    
    # Try sending a test message
    target_id = int(YOUR_USER_ID) if YOUR_USER_ID and YOUR_USER_ID.isdigit() else me.id
    
    print(f"\n📤 Attempting to send test message to ID: {target_id}")
    
    try:
        await client.send_message(target_id, "🧪 **Test Message**\n\nIf you see this, notifications are working! ✅")
        print("✅ Message sent successfully!")
        print("\n💡 Check your Telegram now - you should see the test message")
    except Exception as e:
        print(f"❌ Failed to send message: {e}")
        print("\nTrying to send to 'Saved Messages' instead...")
        try:
            await client.send_message('me', "🧪 **Test Message**\n\nIf you see this, notifications are working! ✅")
            print("✅ Message sent to Saved Messages!")
        except Exception as e2:
            print(f"❌ That also failed: {e2}")
    
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(test_message())

