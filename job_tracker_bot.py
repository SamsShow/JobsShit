import os
import re
import asyncio
import sqlite3
from datetime import datetime, timedelta
from telethon import TelegramClient, events
from telethon.tl.types import Channel
from telethon.errors import FloodWaitError, ChatWriteForbiddenError
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Configuration
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
YOUR_USER_ID = os.getenv('YOUR_USER_ID')
CHANNEL_TO_MONITOR = os.getenv('CHANNEL_TO_MONITOR')
KEYWORDS = [k.strip().lower() for k in os.getenv('KEYWORDS', '').split(',') if k.strip()]

# Database setup
DB_NAME = 'jobs_tracker.db'

def init_database():
    """Initialize the SQLite database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id INTEGER UNIQUE,
            channel_id INTEGER,
            content TEXT,
            matched_keywords TEXT,
            posted_date TIMESTAMP,
            notified BOOLEAN DEFAULT 0
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT UNIQUE,
            keywords TEXT,
            updated_date TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def save_job(message_id, channel_id, content, matched_keywords):
    """Save a job posting to the database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO jobs (message_id, channel_id, content, matched_keywords, posted_date, notified)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (message_id, channel_id, content, ','.join(matched_keywords), datetime.now(), True))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Job already exists
        return False
    finally:
        conn.close()

def check_job_match(text):
    """Check if job posting matches user's keywords"""
    if not text or not KEYWORDS:
        return []
    
    text_lower = text.lower()
    matched = []
    
    for keyword in KEYWORDS:
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(keyword) + r'\b'
        if re.search(pattern, text_lower):
            matched.append(keyword)
    
    return matched

def format_job_notification(content, matched_keywords, message_link):
    """Format the job notification message"""
    message = "🎯 **New Job Match!**\n\n"
    message += f"**Matched Keywords:** {', '.join(matched_keywords)}\n\n"
    message += "**Job Details:**\n"
    message += f"{content[:500]}{'...' if len(content) > 500 else ''}\n\n"
    message += f"🔗 [View Full Post]({message_link})"
    return message

async def get_user_id(client):
    """Get the user's Telegram ID"""
    me = await client.get_me()
    return me.id

async def scan_last_24_hours(client, channel, target_user_id):
    """Scan the last 24 hours of messages from the channel"""
    print("\n🔍 Scanning last 24 hours of messages...")
    
    # Calculate time 24 hours ago
    time_24h_ago = datetime.now() - timedelta(hours=24)
    
    matched_count = 0
    total_scanned = 0
    
    try:
        # Get the channel entity
        channel_entity = await client.get_entity(channel)
        
        # Iterate through messages from the last 24 hours
        async for message in client.iter_messages(channel_entity, limit=None, offset_date=datetime.now()):
            # Stop if message is older than 24 hours
            if message.date < time_24h_ago:
                break
            
            total_scanned += 1
            text = message.text or ""
            
            # Check if job matches user's profile
            matched_keywords = check_job_match(text)
            
            if matched_keywords:
                # Create message link
                if hasattr(channel_entity, 'username') and channel_entity.username:
                    message_link = f"https://t.me/{channel_entity.username}/{message.id}"
                else:
                    # For private channels
                    channel_id = str(channel_entity.id).replace('-100', '')
                    message_link = f"https://t.me/c/{channel_id}/{message.id}"
                
                # Save to database
                saved = save_job(message.id, channel_entity.id, text, matched_keywords)
                
                if saved:
                    matched_count += 1
                    # Send notification
                    try:
                        notification = format_job_notification(text, matched_keywords, message_link)
                        await client.send_message(target_user_id, notification, parse_mode='markdown')
                        print(f"  ✅ Found match: {', '.join(matched_keywords)}")
                        
                        # Small delay to avoid rate limits
                        await asyncio.sleep(1)
                        
                    except FloodWaitError as e:
                        print(f"  ⚠️  Rate limit hit. Waiting {e.seconds} seconds...")
                        await asyncio.sleep(e.seconds)
                        await client.send_message(target_user_id, notification, parse_mode='markdown')
                        
                    except ChatWriteForbiddenError:
                        print(f"  ❌ Cannot send message. Check bot permissions.")
        
        print(f"\n📊 Scan complete!")
        print(f"   📥 Scanned: {total_scanned} messages")
        print(f"   ✅ Matched: {matched_count} jobs")
        print(f"   💾 New jobs saved: {matched_count}")
        
        if matched_count > 0:
            summary = f"\n🎯 **Scan Complete!**\n\nFound **{matched_count}** matching jobs from the last 24 hours!\n\n🤖 Now monitoring for new jobs..."
            await client.send_message(target_user_id, summary, parse_mode='markdown')
        
    except FloodWaitError as e:
        print(f"⚠️  Rate limit during scan. Waiting {e.seconds} seconds...")
        await asyncio.sleep(e.seconds)
        # Retry scan
        await scan_last_24_hours(client, channel, target_user_id)
        
    except Exception as e:
        print(f"❌ Error during 24-hour scan: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Main bot function"""
    # Validate configuration
    if not all([API_ID, API_HASH, CHANNEL_TO_MONITOR]):
        print("❌ Error: Missing required environment variables!")
        print("Please check your .env file and ensure API_ID, API_HASH, and CHANNEL_TO_MONITOR are set.")
        return
    
    if not KEYWORDS:
        print("⚠️  Warning: No keywords configured. Bot will not match any jobs.")
        print("Please add keywords to your .env file.")
    
    # Initialize database
    init_database()
    
    # Create the client with connection pool limits for safety
    client = TelegramClient(
        'job_tracker_session', 
        API_ID, 
        API_HASH,
        connection_retries=5,
        retry_delay=1
    )
    
    await client.start()
    print("✅ Bot started successfully!")
    print("🔒 Running with built-in rate limit protection")
    
    # Get your user ID
    user_id = await get_user_id(client)
    print(f"📱 Your Telegram User ID: {user_id}")
    
    if not YOUR_USER_ID:
        print(f"⚠️  Please add YOUR_USER_ID={user_id} to your .env file")
    
    target_user_id = int(YOUR_USER_ID) if YOUR_USER_ID and YOUR_USER_ID.isdigit() else user_id
    
    print(f"👀 Monitoring channel: {CHANNEL_TO_MONITOR}")
    print(f"🔍 Keywords: {', '.join(KEYWORDS)}")
    print(f"📬 Notifications will be sent to User ID: {target_user_id}")
    
    # Scan last 24 hours of messages
    await scan_last_24_hours(client, CHANNEL_TO_MONITOR, target_user_id)
    
    print("\n🤖 Bot is now monitoring for new jobs... Press Ctrl+C to stop.\n")
    
    # Event handler for new messages in the channel
    @client.on(events.NewMessage(chats=CHANNEL_TO_MONITOR))
    async def handle_new_message(event):
        try:
            message = event.message
            text = message.text or ""
            
            # Check if job matches user's profile
            matched_keywords = check_job_match(text)
            
            if matched_keywords:
                # Get channel info
                channel = await event.get_chat()
                
                # Create message link
                if hasattr(channel, 'username') and channel.username:
                    message_link = f"https://t.me/{channel.username}/{message.id}"
                else:
                    # For private channels, use the channel ID
                    channel_id = str(channel.id).replace('-100', '')
                    message_link = f"https://t.me/c/{channel_id}/{message.id}"
                
                # Save to database
                saved = save_job(message.id, event.chat_id, text, matched_keywords)
                
                if saved:
                    # Send notification with rate limit handling
                    try:
                        notification = format_job_notification(text, matched_keywords, message_link)
                        await client.send_message(target_user_id, notification, parse_mode='markdown')
                        print(f"✅ Notified about new job (matched: {', '.join(matched_keywords)})")
                        
                        # Small delay to avoid rate limits (good practice)
                        await asyncio.sleep(1)
                        
                    except FloodWaitError as e:
                        # Telegram is asking us to wait - respect the rate limit
                        print(f"⚠️  Rate limit hit. Waiting {e.seconds} seconds...")
                        await asyncio.sleep(e.seconds)
                        # Retry sending
                        await client.send_message(target_user_id, notification, parse_mode='markdown')
                        print(f"✅ Notified after wait (matched: {', '.join(matched_keywords)})")
                        
                    except ChatWriteForbiddenError:
                        print(f"❌ Cannot send message. Check bot permissions.")
                        
                else:
                    print(f"ℹ️  Job already tracked (Message ID: {message.id})")
            
        except FloodWaitError as e:
            # Rate limit on reading messages
            print(f"⚠️  Rate limit hit on reading. Waiting {e.seconds} seconds...")
            await asyncio.sleep(e.seconds)
            
        except Exception as e:
            print(f"❌ Error processing message: {e}")
    
    # Keep the bot running
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")

