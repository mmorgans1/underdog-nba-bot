import os
import discord
from discord.ext import commands, tasks
import requests
import asyncio
import datetime
import pytz

# ----------------------------------------------------------
# ENVIRONMENT VARIABLES (Render)
# ----------------------------------------------------------
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

if not DISCORD_TOKEN:
    raise Exception("DISCORD_TOKEN not found in environment variables.")
if not CHANNEL_ID:
    raise Exception("CHANNEL_ID not found in environment variables.")

# ----------------------------------------------------------
# CONSTANTS
# ----------------------------------------------------------
UNDERDOG_URL = "https://api.underdogfantasy.com/beta/news/nba"
PLAYER_IMG = "https://nba-players.familyds.com/players/{}/{}"  # last/first


# ----------------------------------------------------------
# DISCORD BOT SETUP
# ----------------------------------------------------------
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
seen_ids = set()


# ----------------------------------------------------------
# FETCH UNDERDOG NEWS
# ----------------------------------------------------------
def fetch_underdog_news():
    try:
        resp = requests.get(UNDERDOG_URL, timeout=10)
        return resp.json().get("news", [])
    except Exception:
        return []


# ----------------------------------------------------------
# TIMESTAMP CONVERSION TO EST
# ----------------------------------------------------------
def est_time(timestamp):
    dt = datetime.datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    est = dt.astimezone(pytz.timezone("US/Eastern"))
    return est.strftime("%I:%M %p EST")


# ----------------------------------------------------------
# BUILD FANCY EMBED
# ----------------------------------------------------------
def build_embed(item):
    title = item.get("title", "")
    created = item.get("created_at", "")

    # Color logic
    title_upper = title.upper()
    color = (
        0xD93030 if "OUT" in title_upper else
        0xE67E22 if "DOUBTFUL" in title_upper else
        0xF1C40F if "QUESTIONABLE" in title_upper else
        0x2ECC71
    )

    # Try to extract a player name
    parts = title.split(" ")
    first = parts[0]
    last = parts[1] if len(parts) > 1 else ""

    # Fallback player image
    player_url = PLAYER_IMG.format(last, first)

    embed = discord.Embed(
        title=title,
        color=color,
        timestamp=datetime.datetime.utcnow()
    )
    embed.add_field(name="Reported", value=est_time(created), inline=False)
    embed.set_thumbnail(url=player_url)

    return embed


# ----------------------------------------------------------
# BACKGROUND TASK: REAL-TIME INJURY ALERTS
# ----------------------------------------------------------
@tasks.loop(seconds=20)
async def injury_listener():
    channel = bot.get_channel(CHANNEL_ID)
    news_list = fetch_underdog_news()

    for item in reversed(news_list):  # oldest → newest
        news_id = item.get("id")

        if news_id not in seen_ids:
            seen_ids.add(news_id)

            embed = build_embed(item)
            await channel.send(embed=embed)


# ----------------------------------------------------------
# BACKGROUND TASK: DAILY INJURY SUMMARY (10 AM EST)
# ----------------------------------------------------------
@tasks.loop(minutes=1)
async def daily_summary():
    now = datetime.datetime.now(pytz.timezone("US/Eastern"))

    if now.hour == 10 and now.minute == 0:
        channel = bot.get_channel(CHANNEL_ID)

        news = fetch_underdog_news()
        today = now.date()

        summary_items = []
        for item in news:
            dt = datetime.datetime.fromisoformat(
                item["created_at"].replace("Z", "+00:00")
            ).astimezone(pytz.timezone("US/Eastern"))

            if dt.date() == today:
                summary_items.append(f"• {item['title']}")

        embed = discord.Embed(
            title="📝 Daily NBA Injury Summary",
            description="\n".join(summary_items) if summary_items else "No injuries reported today.",
            color=0x3498DB
        )

        await channel.send(embed=embed)


# ----------------------------------------------------------
# SLASH COMMAND: /latest_injuries
# ----------------------------------------------------------
@bot.tree.command(
    name="latest_injuries",
    description="Show the last 10 NBA injury updates."
)
async def latest_injuries(interaction: discord.Interaction):
    news = fetch_underdog_news()[:10]

    embed = discord.Embed(
        title="🔔 Latest NBA Injury Updates",
        color=0x9B59B6
    )

    if not news:
        embed.description = "No injury updates found."
    else:
        for item in news:
            embed.add_field(
                name=item["title"],
                value=est_time(item["created_at"]),
                inline=False,
            )

    await interaction.response.send_message(embed=embed)


# ----------------------------------------------------------
# SLASH COMMAND: /team_injuries [team]
# ----------------------------------------------------------
@bot.tree.command(
    name="team_injuries",
    description="Show injury reports for a specific team."
)
async def team_injuries(interaction: discord.Interaction, team: str):
    news = fetch_underdog_news()
    team = team.lower()

    filtered = [
        item for item in news
        if team in item['title'].lower()
    ]

    embed = discord.Embed(
        title=f"🛡️ Injury Report — {team.title()}",
        color=0x1ABC9C
    )

    if not filtered:
        embed.description = "No team-specific injuries found."
    else:
        for item in filtered:
            embed.add_field(
                name=item["title"],
                value=est_time(item["created_at"]),
                inline=False,
            )

    await interaction.response.send_message(embed=embed)


# ----------------------------------------------------------
# SLASH COMMAND: /injuries_today
# ----------------------------------------------------------
@bot.tree.command(
    name="injuries_today",
    description="Show all injuries reported today."
)
async def injuries_today(interaction: discord.Interaction):
    news = fetch_underdog_news()
    today = datetime.datetime.now(pytz.timezone("US/Eastern")).date()

    todays_items = []
    for item in news:
        dt = datetime.datetime.fromisoformat(
            item["created_at"].replace("Z", "+00:00")
        ).astimezone(pytz.timezone("US/Eastern"))

        if dt.date() == today:
            todays_items.append(item)

    embed = discord.Embed(
        title="📅 Today's NBA Injuries",
        color=0xE74C3C
    )

    if not todays_items:
        embed.description = "No injuries reported yet today."
    else:
        for item in todays_items:
            embed.add_field(
                name=item["title"],
                value=est_time(item["created_at"]),
                inline=False,
            )

    await interaction.response.send_message(embed=embed)


# ----------------------------------------------------------
# ON READY
# ----------------------------------------------------------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()
    injury_listener.start()
    daily_summary.start()


# ----------------------------------------------------------
# RUN BOT
# ----------------------------------------------------------
bot.run(DISCORD_TOKEN)
