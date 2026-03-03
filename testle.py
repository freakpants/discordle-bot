import discord
import requests
import json
import time
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

LEADERBOARD_URL = "https://duotrigordle.com/api/leaderboard?game_mode=daily-normal&type=daily&exclude_solve_assist=false&sort_by=guesses&game_id=1462&user_id=30468df5-8647-4c24-9ada-11ab28cb8f1a&guild_id=4eae2fd7-e961-4809-8a42-fc6dab3e4de8"

HEADERS = {
    "Authorization": "Bearer " + BEARER_TOKEN,
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(LEADERBOARD_URL, headers=HEADERS)

print(response.status_code)
print(response.text)
