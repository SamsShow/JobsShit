# 🚀 Deployment Guide

## Running Without Keeping Terminal Open

You have three options to run the bot automatically:

---

## ✅ Option 1: Quick Start - Background Scripts (Mac/Linux)

### First Time Setup:
1. **Authenticate first** (one-time only):
   ```bash
   python3 job_tracker_bot.py
   ```
   - Enter your phone number
   - Enter verification code
   - Press Ctrl+C to stop after authentication

2. **Start the bot in background**:
   ```bash
   ./start_bot.sh
   ```

### Managing the Bot:

**Start bot:**
```bash
./start_bot.sh
```

**Stop bot:**
```bash
./stop_bot.sh
```

**Check status:**
```bash
./status_bot.sh
```

**View live logs:**
```bash
tail -f bot.log
```

**✨ That's it!** The bot runs in the background even if you close the terminal!

---

## ☁️ Option 2: Deploy to Cloud (Free, 24/7 Running)

### **Railway.app** (Recommended - Easiest)

1. **Sign up**: https://railway.app (free with GitHub)

2. **Authenticate locally first**:
   ```bash
   python3 job_tracker_bot.py
   ```
   After authentication, press Ctrl+C

3. **Initialize Git** (if not already):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

4. **Push to GitHub**:
   - Create a new repo on GitHub
   - Push your code:
   ```bash
   git remote add origin https://github.com/yourusername/telegram-job-bot.git
   git push -u origin main
   ```

5. **Deploy on Railway**:
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Add environment variables:
     - `API_ID`
     - `API_HASH`
     - `YOUR_USER_ID`
     - `CHANNEL_TO_MONITOR`
     - `KEYWORDS`

6. **Upload session file**:
   - Railway Dashboard → Your Project → Variables
   - Upload `job_tracker_session.session` file
   
7. **Deploy!** Railway will start your bot automatically

**⚠️ Important:** 
- Copy your `.session` file to Railway after first authentication
- Don't commit `.env` or `.session` files to GitHub (they're in `.gitignore`)

---

### **Render.com** (Alternative)

1. Sign up: https://render.com
2. Create "Background Worker"
3. Connect your GitHub repo
4. Set environment variables
5. Deploy

---

### **Fly.io** (Alternative)

1. Install Fly CLI: https://fly.io/docs/getting-started/
2. Run:
   ```bash
   fly launch
   fly deploy
   ```

---

## 🖥️ Option 3: macOS LaunchAgent (Auto-start on Login)

### Create a system service that starts automatically:

1. Create launch agent file:
   ```bash
   nano ~/Library/LaunchAgents/com.telegram.jobtracker.plist
   ```

2. Paste this content (update paths):
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.telegram.jobtracker</string>
       <key>ProgramArguments</key>
       <array>
           <string>/usr/local/bin/python3</string>
           <string>/Users/samshow/Desktop/JobsShit/job_tracker_bot.py</string>
       </array>
       <key>RunAtLoad</key>
       <true/>
       <key>KeepAlive</key>
       <true/>
       <key>StandardOutPath</key>
       <string>/Users/samshow/Desktop/JobsShit/bot.log</string>
       <key>StandardErrorPath</key>
       <string>/Users/samshow/Desktop/JobsShit/bot.error.log</string>
       <key>WorkingDirectory</key>
       <string>/Users/samshow/Desktop/JobsShit</string>
   </dict>
   </plist>
   ```

3. Load the service:
   ```bash
   launchctl load ~/Library/LaunchAgents/com.telegram.jobtracker.plist
   ```

4. Start the service:
   ```bash
   launchctl start com.telegram.jobtracker
   ```

**Manage the service:**
- Start: `launchctl start com.telegram.jobtracker`
- Stop: `launchctl stop com.telegram.jobtracker`
- Unload: `launchctl unload ~/Library/LaunchAgents/com.telegram.jobtracker.plist`

---

## 📊 Comparison

| Method | Difficulty | Cost | Reliability | Auto-restart |
|--------|------------|------|-------------|--------------|
| Background Scripts | ⭐ Easy | Free | Good | Manual |
| Railway/Render | ⭐⭐ Medium | Free | Excellent | Automatic |
| macOS LaunchAgent | ⭐⭐⭐ Advanced | Free | Excellent | Automatic |

---

## 🔧 Troubleshooting

### Bot stops unexpectedly
- Check logs: `tail -f bot.log`
- Check if session expired
- Verify internet connection

### "Session file not found" on cloud
- You need to upload the `.session` file after authenticating locally
- Authenticate on your computer first, then upload the session file

### Can't connect to Telegram
- Verify API credentials
- Check firewall settings
- Try re-authenticating

---

## 💡 Recommendations

**For quick testing:** Use background scripts (`./start_bot.sh`)

**For 24/7 monitoring:** Deploy to Railway or Render

**For local persistent running:** Use macOS LaunchAgent

---

**Need help?** Check the logs in `bot.log` for error messages.


