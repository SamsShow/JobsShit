#!/usr/bin/env python3
"""
Helper script to encode the session file for Railway deployment.
Run this after setup_session.py to get the base64 encoded session.
"""

import os
import base64

def encode_session():
    """Encode session file to base64 for Railway environment variable"""
    
    session_file = 'job_tracker_session.session'
    
    if not os.path.exists(session_file):
        print(f"❌ Error: {session_file} not found!")
        print("\n📝 Please run 'python setup_session.py' first to create the session file.")
        return
    
    try:
        with open(session_file, 'rb') as f:
            session_data = f.read()
        
        encoded = base64.b64encode(session_data).decode('utf-8')
        
        print("✅ Session file encoded successfully!")
        print("\n" + "=" * 70)
        print("📋 Copy the text below and add it to Railway as SESSION_BASE64:")
        print("=" * 70)
        print("\n" + encoded + "\n")
        print("=" * 70)
        print("\n📌 Steps to deploy:")
        print("   1. Go to your Railway project → Variables")
        print("   2. Click 'New Variable'")
        print("   3. Name: SESSION_BASE64")
        print("   4. Value: (paste the encoded text above)")
        print("   5. Click 'Add'")
        print("   6. Redeploy your application")
        
        # Also save to file for convenience
        output_file = 'session_encoded.txt'
        with open(output_file, 'w') as f:
            f.write(encoded)
        
        print(f"\n💾 Also saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error encoding session: {e}")

if __name__ == '__main__':
    encode_session()

