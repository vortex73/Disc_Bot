import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
intents = discord.Intents.all()
intents.members = True
intents.presences = True
load_dotenv()
from help_message import help_message
from music_func import music_func

bot=commands.Bot(command_prefix="!",intents=intents)


@bot.event 
async def on_ready():
    print("I'm ready")


    bot.remove_command("help")

    await bot.add_cog(help_message(bot))
    await bot.add_cog(music_func(bot))


bot.run(os.getenv("token"))


