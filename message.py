import os
from dotenv import load_dotenv
import discord
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
