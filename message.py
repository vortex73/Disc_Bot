import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
import scrapetube


load_dotenv()
intents = discord.Intents.all()
intents.members = True
intents.presences = True     

bot = commands.Bot(command_prefix=".", intents=intents)


@bot.event
async def on_ready():
    print("I am online")   #For bot to tell when it's online

@bot.event
async def on_member_join(member):
    await Bot.get_channel(1044294754818609216).send("Welcome {}".format(member.mention)) # Welcome msg 

@bot.command(name="clear")
async def clear(msgs,amount=5):
    await msgs.channel.purge(limit=amount+1)
    

@bot.command(name="nuke")
async def clear(msgs):
    await msgs.channel.purge()

class Youtube(commands.Cog):
    def __init__(self,Bot):
        self.Bot = Bot
        self.channels = {
                "kdb123":"https://www.youtube.com/channel/UCiQUBoO5P2wCubsTAVrR4Fg"


                }
        self.videos = {}

    @commands.Cog.listener()
    async def on_ready(self):
        self.check.start()

    @tasks.loop(seconds=60)
    async def check(self):
        discord_channel = self.Bot.get_channel(1044294754818609216)

        for channel_name in self.channels:
            videos = scrapetube.get_channel(channel_url = self.channels[channel_name])
            video_ids = [video["videoId"] for video in videos]

            if self.check.current_loop == 0 :
                self.videos[channel_name] = video_ids
                continue

            for video_id in video_ids:
                if video_id not in self.videos[channel_name]:
                    url = f"https://youtube.com/{video_id}"
                    await discord_channel.send(f"{channel_name} has uploaded a new video\n{url}")


            self.videos[channel_name] = video_ids

@bot.event
async def on_ready():
    print("I'm on")
    await bot.add_cog(Youtube(bot))



@bot.command(name="start-yt")  #function to tell the bot to start otifying
async def start_notifications(notify):
    Youtube(bot).check.start()
    await notify.send("Now notifying")

@bot.command(name="stop-yt")  #function to tell the bot to stop notifying
async def stop_notifications(notify):
    Youtube(bot).check.stop()
    await notify.send("Stopped notifying")

bot.run(os.getenv("token"))

