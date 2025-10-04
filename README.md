# 🤖 Telegram Job Tracker Bot

A smart Telegram bot that monitors job postings from channels and notifies you only about jobs that match your profile and skills.
 
## 🌟 Features

- **24-Hour History Scan**: Scans last 24 hours of messages when bot starts (never miss a job!)
- **Real-time Monitoring**: Automatically tracks new messages from any Telegram job channel
- **Smart Filtering**: Matches jobs based on your keywords (skills, technologies, job titles)
- **Database Storage**: Keeps a record of all tracked jobs in SQLite
- **Instant Notifications**: Sends you direct messages when relevant jobs are posted
- **Job Management**: View, search, and analyze tracked jobs
- **Rate Limit Protection**: Built-in safety features to protect your account

## 📋 Prerequisites

1. **Python 3.7+** installed on your system
2. **Telegram Account**
3. **Telegram API Credentials** (we'll get these in setup)

## 🚀 Setup Instructions

### Step 1: Get Telegram API Credentials

1. Visit https://my.telegram.org
2. Log in with your phone number
3. Go to "API Development Tools"
4. Create a new application (you can name it anything)
5. Copy your `API_ID` and `API_HASH`

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure the Bot

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file with your details:
   ```env
   API_ID=your_api_id_from_step_1
   API_HASH=your_api_hash_from_step_1
   YOUR_USER_ID=
   CHANNEL_TO_MONITOR=@jobchannelname
   KEYWORDS=python,javascript,developer,remote,fullstack
   ```
   
   **Note**: You do NOT need a BOT_TOKEN! This bot uses your user account, not a bot account.

3. **Important**: Replace the keywords with your actual skills and preferences!

### Step 4: Find the Channel to Monitor

You need the channel username or ID:
- **Public channels**: Use the username (e.g., `@jobchannel`)
- **Private channels**: You'll need to be a member, and you can use the channel ID

### Step 5: Run the Bot

**First-time authentication:**
```bash
python3 job_tracker_bot.py
```

On first run:
1. You'll be asked to enter your phone number
2. Enter the verification code sent to your Telegram
3. The bot will display your User ID (optional to add to `.env`)
4. Press Ctrl+C after successful authentication

**Then run in background:**
```bash
./start_bot.sh
```

🎉 **That's it!** Bot runs in the background, even if you close the terminal!

**📖 For cloud deployment (24/7) or other options, see [DEPLOYMENT.md](DEPLOYMENT.md)**

## 📱 Usage

### Running the Bot

```bash
python job_tracker_bot.py
```

Keep this running in the background. The bot will:
- Monitor the specified channel(s)
- Match jobs against your keywords
- Send you notifications via Telegram
- Store all matched jobs in the database

### Viewing Tracked Jobs

```bash
python view_jobs.py
```

Options:
1. **View all jobs**: See all tracked jobs with details
2. **Search jobs**: Find jobs by specific keywords
3. **View statistics**: Get insights about tracked jobs

## 🔧 Configuration Options

### Keywords

Edit the `KEYWORDS` in your `.env` file. Use comma-separated values:

```env
# Skills and technologies
KEYWORDS=python,django,fastapi,postgresql,docker,aws

# Job titles
KEYWORDS=senior developer,backend engineer,python developer

# Mix of skills and preferences
KEYWORDS=python,remote,fullstack,react,typescript
```

**Tips**:
- Use specific keywords to reduce false positives
- Include both skills and job titles
- Add location preferences if needed (e.g., "remote", "new york")
- The matching is case-insensitive

### Monitoring Multiple Channels

To monitor multiple channels, you can:
1. Run multiple instances of the bot with different `.env` files
2. Or modify the code to accept a list of channels

## 📊 Database

The bot creates a `jobs_tracker.db` SQLite database with:

- **jobs table**: Stores all matched job postings
- **user_profile table**: Stores your profile and keywords (for future features)

## 🛠️ Troubleshooting

### "Error: Missing required environment variables"
- Check that your `.env` file exists and has all required fields
- Make sure there are no extra spaces around the `=` sign

### "FloodWaitError"
- **This is normal!** Telegram has rate limits to prevent abuse
- The bot automatically waits and retries - no action needed
- This is NOT a ban, just a temporary slowdown
- Rate limits protect YOUR account from being flagged

### Not receiving notifications
- Verify your `YOUR_USER_ID` is correct in `.env`
- Check that your keywords match the job postings
- Ensure the bot has completed the authentication process

### Can't access the channel
- For private channels, your account must be a member
- For public channels, double-check the username format: `@channelname`

## 🔒 Privacy & Security

### Is This Safe? Will I Get Banned?

**NO, you won't get banned!** This bot:
- ✅ Uses Telegram's **official API** (completely legitimate)
- ✅ Only **reads** messages (no spam or automation)
- ✅ **Respects rate limits** (built-in protection)
- ✅ Follows Telegram's **Terms of Service**

### Built-in Safety Features:
- **Automatic rate limit handling** - waits when Telegram asks
- **Flood protection** - never tries to bypass limits
- **Error recovery** - handles network issues gracefully
- **Connection retries** - safe reconnection logic

### Your Data:
- API credentials stored locally in `.env` (never commit this file!)
- Bot only reads messages from channels you specify
- All data stored locally on your machine
- No third-party services involved

**📖 Read [SECURITY.md](SECURITY.md) for complete safety guide and best practices**

## 📝 Notes

- The bot needs to stay running to monitor channels in real-time
- Consider running it on a server or VPS for 24/7 operation
- You can use tools like `screen`, `tmux`, or `systemd` to keep it running
- Rate limits apply: Don't add too many channels at once

## 🎯 Future Enhancements

Potential features to add:
- Web dashboard for job management
- AI-powered job matching using NLP
- Multiple user profiles
- Job application tracking
- Salary filtering
- Company blacklist/whitelist
- Email notifications

## 📜 License

This project is open source and available for personal use.

## 🤝 Contributing

Feel free to fork this project and customize it for your needs!

---

**Happy Job Hunting! 🎉**

