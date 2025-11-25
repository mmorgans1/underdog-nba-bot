# 🏀 Underdog NBA Injury Discord Bot

A fully automated Discord bot that listens for **real-time NBA injury updates** from the **Underdog Fantasy NBA News API** and posts them into a Discord channel using **rich embed messages**.

Includes:

- 🔔 Real-time injury alerts (checked every 20 seconds)
- 📝 Daily injury summary at 10 AM EST
- 🧩 Player images automatically added to every embed
- ⚡ Slash commands:
  - `/latest_injuries`
  - `/team_injuries [team]`
  - `/injuries_today`
- 🌐 Fully optimized for **Render Free Tier**
- 🔐 Uses environment variables for secure token handling

---

## 📦 Folder Structure

underdog-nba-bot/
│── underdog_bot.py # main bot script
│── requirements.txt # Python dependencies
│── start.sh # Render start script
└── README.md # project documentation

markdown
Copy code

---

## 🚀 Deployment (Render WITHOUT GitHub)

### 1. Prepare your files
Make sure your folder contains:

- `underdog_bot.py`
- `requirements.txt`
- `start.sh`
- `README.md`

### 2. Go to Render
https://dashboard.render.com

### 3. Create a new Web Service
- Click **New → Web Service**
- Choose **Deploy from Local Folder**
- Upload your `underdog-nba-bot` folder

### 4. Set environment variables

**Environment Variables → Add:**
DISCORD_TOKEN = your_discord_bot_token
CHANNEL_ID = your_discord_channel_id

markdown
Copy code

### 5. Set Build & Start commands

**Build Command**
pip install -r requirements.txt

markdown
Copy code

**Start Command**
./start.sh

yaml
Copy code

Render will automatically build and run your bot.

---

## 🛠 Requirements

Install via `requirements.txt`:
discord.py
requests
pytz

yaml
Copy code

---

## 🔧 Start Script

The `start.sh` file required by Render:

```bash
#!/bin/bash
python underdog_bot.py
🔐 Security Notes
Your bot token must not be hard-coded in the script.

Always store DISCORD_TOKEN and CHANNEL_ID as Render environment variables.

If your bot token is ever exposed, reset it immediately.

🧪 Slash Commands
/latest_injuries
Shows the 10 most recent injury updates.

/team_injuries [team]
Filters injury updates for a specific NBA team name.

/injuries_today
Lists all injuries reported today (EST).

📝 Features
🔥 Real-time Alerts
Bot checks Underdog every 20 seconds and posts:

OUT

Questionable

Doubtful

Upgraded to Available

Game-Time Decision

🕒 Daily Injury Summary (10 AM EST)
Automatically posts a daily roundup of all injuries so far.

📡 Data Source
Underdog Fantasy NBA News API (no API key required)

ruby
Copy code
https://api.underdogfantasy.com/beta/news/nba
🤝 Contributing
This bot is fully private and optimized for personal or server-based use.
You are free to add:

Role-based pings

Team routing channels

Google Sheets logging

Better player photo sources

Cloud database caching

📬 Support / Assistance
Need additional features?

Team-specific alert channels

Role pings (e.g., @HeatAlerts)

Logging all injuries into a Google Sheet

100% uptime hosting via Railway

Just ask!

🎉 Enjoy Your Real-Time NBA Injury Bot!
This bot provides live, reliable injury updates faster than 99% of apps.

Never miss a Q/OUT/Doubtful update again!