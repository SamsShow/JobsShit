#!/usr/bin/env python3
"""
Setup script to authenticate and create a Telegram session file.
Run this locally BEFORE deploying to Railway.

This will create 'job_tracker_session.session' file that contains
your authentication. You'll need to upload this to Railway.
"""

import os
import asyncio
from telethon import TelegramClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

async def create_session():
    """Create and authenticate a Telegram session"""
    
    if not API_ID or not API_HASH:
        print("❌ Error: API_ID and API_HASH must be set in .env file")
        return
    
    print("🔧 Telegram Session Setup")
    print("=" * 50)
    print("\nThis will create an authenticated session file.")
    print("You'll need to:")
    print("  1. Enter your phone number")
    print("  2. Enter the code sent to your Telegram")
    print("  3. Optionally enter 2FA password if enabled\n")
    
    client = TelegramClient('job_tracker_session', API_ID, API_HASH)
    
    try:
        await client.start()
        
        # Get user info
        me = await client.get_me()
        print(f"\n✅ Successfully authenticated!")
        print(f"   User: {me.first_name} {me.last_name or ''}")
        print(f"   Username: @{me.username}")
        print(f"   User ID: {me.id}")
        print(f"\n📝 Session file created: job_tracker_session.session")
        print("\n⚠️  IMPORTANT:")
        print("   1. Add this User ID to YOUR_USER_ID in .env if not already set")
        print("   2. Upload 'job_tracker_session.session' to Railway")
        print("   3. Keep this file secure - it contains your authentication!")
        
    except Exception as e:
        print(f"\n❌ Error during authentication: {e}")
    finally:
        await client.disconnect()

if __name__ == '__main__':
    try:
        asyncio.run(create_session())
    except KeyboardInterrupt:
        print("\n\n👋 Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

