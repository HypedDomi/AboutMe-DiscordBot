import base64
import discord
import json
import requests
from discord.ext.commands.bot import Bot

intents = discord.Intents.default()
intents.members = True
intents.presences = True

USER_ID = 1234567890
TOKEN = "token"
API_PASSWORD = "password"
API_URL = ""

bot = Bot(intents=intents)


@bot.event
async def on_ready():
    print()
    print(f"{bot.user.name} is ready!")
    print()


@bot.event
async def on_presence_update(before: discord.Member, after: discord.Member) -> None:
    if after.id == USER_ID:
        activities = []
        for activity in after.activities:
            if activity.type != discord.ActivityType.custom:
                if isinstance(activity, discord.Spotify):
                    activity: discord.Spotify = activity
                    data = {
                        "type": activity.type.value,
                        "song": activity.title,
                        "artists": activity.artists,
                        "album": activity.album,
                        "cover": activity.album_cover_url,
                        "track_url": activity.track_url,
                        "duration": int(activity.duration.total_seconds()),
                        "party_id": activity.party_id
                    }
                    activities.append(data)
                elif isinstance(activity, discord.Activity):
                    activity: discord.Activity = activity
                    data = {
                        "type": activity.type.value,
                        "assets": activity.assets,
                        "buttons": activity.buttons,
                        "aplication_id": activity.application_id,
                        "created_at": int(activity.created_at.timestamp()),
                        "name": activity.name,
                        "details": activity.details,
                        "state": activity.state,
                        "timestamps": activity.timestamps,
                        "party": activity.party
                    }
                    activities.append(data)
        data = json.dumps(
            {"status": after.status.value, "activities": activities})
        headers = {'Content-type': 'application/json',
                   "authorization": base64.b64encode(API_PASSWORD.encode("utf-8")).decode("utf-8")}
        requests.post(API_URL, headers=headers, data=data)

bot.run(TOKEN)
