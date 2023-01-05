import os
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
import json
import requests
import re

load_dotenv()
intents = discord.Intents.all()
intents.members = True
intents.presences = True     

Bot = commands.Bot(command_prefix=".", intents=intents)


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

@tasks.loop(seconds=10) #checks if new video is uploaded every 10 seconds
async def check():
    with open("youtube.json","r") as file:  
        youtubedata=json.load(file)

    for yt_channel in youtubedata:  
        channel_url = f"https://www.youtube.com/channel/{yt_channel}"   #generates youtube channel's url
        html_link = requests.get(channel+"/videos").text  #generates html link
        try:   #using try and except block to avoid errors incase no video is uploaded 
            video_url = f"https://www.youtube.com/watch?v=" + re.search('(?<="videoId":").*?(?=")', html_link).group()
        except:
            continue

        if str(youtubedata[yt_channel]["video_url"]) != video_url:  #compares the url in json file and that of the chosen video
            youtubedata[str(yt_channel)]["video_url"] == video_url   #makes both equal

            with open("youtube.json","w") as file:
                json.dump(youtubedata,file) #dump is a function to convert python object to json file

            discordchannel_id = youtubedata[str(yt_channel)]["notify"]
            discordchannel = Bot.get_channel(int(discordchannel_id))
            
            display_msg = f"@everyone {youtubedata[str(yt_channel)][channel_name]} just uploaded : {video_url}"
            
            await discordchannel.send(display_msg)
            #notifies server when video is uploaded and the above msg is displayed






        

Bot.run(os.getenv("token"))
