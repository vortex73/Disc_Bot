
import discord
from discord.ext import commands

class help_message(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

        self.message='''
        GENERAL COMMANDS:
        >help- Displays all the required commands
        >play (song name) - Plays the song in the voice channel
        >resume- Resumes playing the song
        >pause- Pauses the currently playing song
        '''
        self.text_channel=[]


    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                self.text_channel_text.append(channel)
        await self.send_to_all(self.help_message)
    async def send_to_all(self,msg):
        for text_channel in self.text_channel_text:
            await text_channel.send(msg)
    @commands.command(name="help",help="Displays all the required commands")
    async def help (self,msg):
        await msg.send(self.message)

    
