import os
from dotenv import load_dotenv
import discord

from discord.ext import commands, tasks
import scrapetube


# load_dotenv()
# intents = discord.Intents.all()
# intents.members = True
# intents.presences = True     

#Bot = commands.Bot(command_prefix=".", intents=intents)

class msg(commands.Cog):
    def __init__(self,Bot) -> None:
        self.Bot = Bot
        self.initialize()
    def initialize(self):    
        @self.Bot.event
        async def on_ready():
            print("I am online")   #For bot to tell when it's online

        @self.Bot.event
        async def on_member_join(member):
            await self.Bot.get_channel(1044294754818609216).send("Welcome {}".format(member.mention)) # Welcome msg 

        @self.Bot.tree.command(name="clear",description = "Deletes given number of messages")
        async def clear(msgs:discord.Interaction,amount:int):
            await msgs.response.defer()
            await msgs.channel.purge(limit=amount+1)
            await msgs.followup.send("Deleted {amount} messages")
        @self.Bot.tree.command(name="nuke",description = "Bulk deletion of messages(100)")
        async def clear(msgs:discord.Interaction):
            await msgs.response.defer()
            await msgs.channel.purge()
            await msgs.followup.send("Messages Nuke'd")
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


        def setup(self):
            self.Bot.add_Cog(Youtube(self.Bot))



        @self.Bot.tree.command(name="start-yt",description = "Begin looking for youtube notifications")  #function to tell the bot to start otifying
        async def start_notifications(notify:discord.Interaction):
            await notify.response.defer()
            Youtube(self.Bot).check.start()
            await notify.followup.send("Now notifying")

        @self.Bot.tree.command(name="stop-yt",description = "Stop looking for youtube notifications")  #function to tell the bot to stop notifying
        async def stop_notifications(notify:discord.Interaction):
            await notify.response.defer()
            Youtube(self.Bot).check.stop()
            await notify.followup.send("Stopped notifying")

#Bot.run(os.getenv("token"))
from discord.ext import commands
load_dotenv()
intents = discord.Intents.default()
intents.members = True
intents.presences = True     

Bot = commands.Bot(command_prefix="%", intents=intents)


@Bot.event
async def on_ready():
    print("I am online")

@Bot.event
async def on_member_join(member):
    await Bot.get_channel(1044294754818609216).send("Welcome {}".format(member.mention)) # Welcome msg 

@Bot.command(name="clear")
async def clear(ctx,amount=5):
    await ctx.channel.purge(limit=amount)

@Bot.command(name="nuke")
async def clear(ctx):
    await ctx.channel.purge()

Bot.run(os.getenv("token"))

