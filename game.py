import os
from dotenv import load_dotenv
import firebase_admin
import discord
from firebase_admin import credentials
from firebase_admin import db
from discord import Game, embeds
from discord.ext.commands import Bot
BOTPREFIX = "?"
load_dotenv()
intents = discord.Intents.default()
intents.members = True
intents.presences = True
c = credentials.Certificate(r"key.json")
firebase_admin.initialize_app(c, {'databaseURL': 'https://discbot-f50a9-default-rtdb.firebaseio.com/'})

#client = discord.Client(command_prefix = "!",intents = intents)
ref = db.reference("/")





class chars:  #Parent Class for general charachter outline
    def __init__(self,typee,power,health,xp,value):
        self.typee = typee
        self.power = power
        self.health = health
        self.xp = xp 
        self.value = value

    def combat():
        pass
    def hunt():
        pass
    def abandon():
        pass
    def level():
        pass
    def buy():
        pass
    
    # Space to add more player actions

class user(chars):    #Class for player
    def __init__(self,id,name,typee="Player",power=None,health=100,xp=0,value=None,level=1):
        super().__init__(typee,power,health,xp,value)
        self.level = level
        self.id = id
        self.name = name
class evil(chars):  #Class for opponents
    def __init__(self,power, typee="System wardogs", health=100, xp=1000, value=None):
        super().__init__(typee, power, health, xp, value)

class blow:


    def __init__(self,token):
        self.token = token
        self.bot = Bot(command_prefix = BOTPREFIX , intents = intents)
        self.initialize()
    def run(self):
        self.bot.run(self.token)
 #       ref = db.reference("/")
       # # print(ref.get ())
#        users = ref.child('users')
       # users.set({
       #     
       # users.push() # test code for firebase
     
    def initialize(self):
        
        @self.bot.event
        async def on_ready():
            await self.bot.change_presence(activity=Game(name="Koala"))
            self.bulk_store()
            print("[*] Connected to Discord as: " + self.bot.user.name)
        @self.bot.command(name='stats')
        async def stats(context):
            player = {"join_server_date": "2020:2:2","xp_points":20}
           # await context.message.reply(embeds = embed) 
            #await self.bot.say("So you want stats?")

            embed = discord.Embed(title = "Brilliant")
            embed.set_author(name=context.author.display_name,icon_url=context.author.avatar_url)
            embed.add_field(name="Testing",value="""
                            Wow
                            """,inline=True)

            embed = discord.Embed(title = "")
            embed.set_author(name=context.author.display_name,icon_url=context.author.avatar_url)
            embed.add_field(name="",value="""<Write something here>""",inline=True)

            await context.message.reply(embed=embed)
                            

    def bulk_store(self):      # Function to store all the members in the server
        for i in self.bot.get_all_members():
            x=user(i.id,i.name)
            self.store(x)
    def store(self,x):         # Function to push given datapoint into DB
            
            users = ref.child('users/player') 
            users.push({
                x.id:{"typee":x.typee,
                       "Name" : x.name,
                       "xp" : x.xp,
                       "level" : x.level,
                       "health":x.health,
                       "power" : x.power}
                    })
        
i=blow(os.getenv("token"))
print(i.run())

