import discord
import requests
import json
import time
import asyncio
import os
from dotenv import load_dotenv

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

LEADERBOARD_URL = "https://duotrigordle.com/api/leaderboard?game_mode=daily-normal&type=daily&exclude_solve_assist=false&sort_by=guesses&game_id=1462&user_id=30468df5-8647-4c24-9ada-11ab28cb8f1a&guild_id=4eae2fd7-e961-4809-8a42-fc6dab3e4de8"

HEADERS = {
    "Authorization": BEARER_TOKEN,
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0"
}

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def fetch_leaderboard():
    response = requests.get(LEADERBOARD_URL, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code)
        return None

def load_previous():
    try:
        with open("leaderboard.json", "r") as f:
            return json.load(f)
    except:
        return None

def save_current(data):
    with open("leaderboard.json", "w") as f:
        json.dump(data, f)

def leaderboard_changed(old, new):
    return old != new

async def leaderboard_loop():
    await client.wait_until_ready()
    channel = await client.fetch_channel(CHANNEL_ID)
    previous_data = load_previous()
    loop = asyncio.get_event_loop()

    while not client.is_closed():
        # Run blocking fetch_leaderboard in a thread executor
        new_data = await loop.run_in_executor(None, fetch_leaderboard)

        if new_data:
            if previous_data is None:
                save_current(new_data)
                previous_data = new_data

            elif leaderboard_changed(previous_data, new_data):
                await channel.send("🚨 Leaderboard updated!")
                save_current(new_data)
                previous_data = new_data

        await asyncio.sleep(60)

client.loop.create_task(leaderboard_loop())
client.run(BOT_TOKEN)
