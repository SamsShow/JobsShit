# 🚀 Railway Quick Start Guide

## ✅ The Issue is Fixed!

The EOF error has been resolved. The bot now supports non-interactive authentication for Railway deployment.

---

## 🎯 Quick Deployment Steps

### 1️⃣ Generate Session Locally (One-time setup)

```bash
python setup_session.py
```

You'll be prompted to:
- Enter your phone number (with country code, e.g., +1234567890)
- Enter the verification code sent to your Telegram
- Enter 2FA password (if you have one)

This creates `job_tracker_session.session` file.

### 2️⃣ Encode Session for Railway

```bash
python encode_session.py
```

This will display a long base64 string. Copy it!

### 3️⃣ Configure Railway

Go to your Railway project → **Variables** and add:

| Variable Name | Value | Example |
|--------------|-------|---------|
| `SESSION_BASE64` | (paste the encoded string) | `AQAAAAEAaa...` |
| `API_ID` | Your API ID | `12345678` |
| `API_HASH` | Your API hash | `abcdef123...` |
| `YOUR_USER_ID` | Your Telegram User ID | `123456789` |
| `CHANNEL_TO_MONITOR` | Channel to monitor | `@build3dao` |
| `KEYWORDS` | Comma-separated keywords | `python,django,api` |
| `SCAN_HOURS` | Hours to scan back | `48` |

### 4️⃣ Deploy

Railway will automatically deploy with your new configuration.

Check the logs for: **✅ Bot started successfully!**

---

## 🔄 Alternative: Using a Bot Token (No Session Needed)

If you prefer to use a bot instead of your user account:

1. **Create a bot:**
   - Message [@BotFather](https://t.me/BotFather) on Telegram
   - Send `/newbot` and follow instructions
   - Copy the bot token

2. **Add bot to your channel:**
   - Add the bot as admin to the channel
   - Give it "Read Messages" permission

3. **Configure Railway:**
   - Instead of `SESSION_BASE64`, add `BOT_TOKEN`
   - Remove or leave `SESSION_BASE64` empty

**Limitations of Bot Token:**
- Must be added as admin to monitored channel
- Some private channels may not work
- Different rate limits

---

## 🐛 Troubleshooting

### Bot won't start
- ✅ Verify all environment variables are set
- ✅ Check that `SESSION_BASE64` is correctly copied (no spaces/line breaks)
- ✅ Make sure the session hasn't expired (re-run setup if needed)

### "Cannot send message" error
- ✅ Verify `YOUR_USER_ID` is correct
- ✅ For channels, ID should start with `-100`
- ✅ Try sending yourself a test message first

### Session expired
- ✅ Re-run `setup_session.py` locally
- ✅ Re-run `encode_session.py`
- ✅ Update `SESSION_BASE64` in Railway
- ✅ Redeploy

---

## 📝 Files Added

- `setup_session.py` - Generate authenticated session
- `encode_session.py` - Encode session for Railway
- `decode_session.py` - Helper for session decoding
- `DEPLOYMENT_GUIDE.md` - Detailed deployment guide
- `RAILWAY_QUICK_START.md` - This quick start guide

---

## 🔒 Security Notes

- ✅ Session file gives FULL access to your Telegram account
- ✅ Never share your session file or encoded session
- ✅ Use a separate account for bots if possible
- ✅ All sensitive files are in `.gitignore` - don't commit them!
- ✅ Rotate credentials periodically

---

## ✨ What's New in the Bot

The bot now:
- ✅ Supports Railway deployment without interactive prompts
- ✅ Can use either session file OR bot token
- ✅ Automatically decodes session from environment variable
- ✅ Has better error messages for troubleshooting
- ✅ Includes comprehensive deployment guides

---

**Need more help?** Check `DEPLOYMENT_GUIDE.md` for detailed instructions.

