#!/usr/bin/env python3
"""
Helper script to decode session file from Railway environment variable.
This runs before the main bot to setup the session file.
"""

import os
import base64

def decode_session():
    """Decode base64 session from environment variable"""
    session_base64 = os.getenv('SESSION_BASE64')
    
    if session_base64:
        try:
            session_data = base64.b64decode(session_base64)
            with open('job_tracker_session.session', 'wb') as f:
                f.write(session_data)
            print("✅ Session file decoded successfully")
            return True
        except Exception as e:
            print(f"❌ Error decoding session: {e}")
            return False
    else:
        print("ℹ️  No SESSION_BASE64 environment variable found")
        return False

if __name__ == '__main__':
    decode_session()

