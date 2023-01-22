import discord
from discord.ext import commands, tasks
import scrapetube


class Youtube(commands.Cog):
    def __init__(self,Bot):
        self.Bot = Bot
        self.channels = {
                "kdb123":"https://www.youtube.com/channel/UCiQUBoO5P2wCubsTAVrR4Fg"


                }
        self.videos = {}
        self.initialize()

    def initialize(self): 
        @commands.Cog.listener()
        async def on_ready(self):
            print("I am online")   #For bot to tell when it's online
            await self.Bot.tree.sync()
            self.check.start()
        @commands.Cog.listener()
        async def on_member_join(self,member):
            await self.Bot.get_channel(1044294754818609216).send("Welcome {}".format(member.mention)) # Welcome msg 
        async def amt(i:discord.Interaction,current:str)->list[discord.app_commands.Choice[str]]:
            l=[]
            for i in [1,5,10,20,30,50]:
                l.append(discord.app_commands.Choice(name=i,value=i))
            return l
        @self.Bot.tree.command(name="clear")
        @discord.app_commands.autocomplete(amount=amt)
        async def clear(i:discord.Interaction,amount:int)->list[discord.app_commands.Choice[str]]:
            await i.channel.purge(limit=amount+1)
            

        @self.Bot.tree.command(name="nuke")
        async def clear(i:discord.Interaction):
            await i.response.send_message("Deleting...")
            await i.channel.purge()

        
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




        @self.Bot.tree.command(name="start-yt")  #function to tell the bot to start otifying
        async def start_notifications(i:discord.Interaction):
            Youtube(self.Bot).check.start()
            await i.response.send_message("Now notifying")

        @self.Bot.tree.command(name="stop-yt")  #function to tell the bot to stop notifying
        async def stop_notifications(i:discord.Interaction):
            Youtube(self.Bot).check.stop()
            await i.response.send_message("Stopped notifying")

#bot.run(os.getenv("token"))

