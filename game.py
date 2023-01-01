import os
from dotenv import load_dotenv
import firebase_admin
import random
import json
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
    
    def combat(self,x):
        while True:
            hit_prob = random.random()*self.power
            x_hit_prob = random.random()*x.power
            self.health -= x_hit_prob
            x.health -= hit_prob
            if self.health or x.health == 0:
                break

        print(hit_prob,x_hit_prob)
        print(self.health,x.health)
        if self.health>x.health:
            return "You Won!"
        else:
            return "You lost."

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
       # users.push() # test code for firebase
     
    def initialize(self):
        
        @self.bot.event
        async def on_ready():
            await self.bot.change_presence(activity=Game(name="Kola Theme"))
            self.bulk_store()
            print("[*] Connected to Discord as: " + self.bot.user.name)

        @self.bot.command(name='stats')

        async def stats(context):
            player = {"join_server_date": "2020:2:2","xp_points":20}
           # await context.message.reply(embeds = embed) 
            #await self.bot.say("So you want stats?")
            embed = discord.Embed(title = "")
            embed.set_author(name=context.author.display_name,icon_url=context.author.avatar_url)
            embed.add_field(name="",value="""<Write something here>""",inline=True)
            await context.message.reply(embed=embed)

        @self.bot.command(name="attack")
        
        async def atck(context):
            player = user(context.author.id,context.author.display_name,power=10)
            # Opponent definition
            opponent = evil(power=50)
            # TODO : dependence of attack on XP points
            await context.message.reply(str(player.combat(opponent)))
        
        @self.bot.command(name="buy")

        async def buy(context):
            shop = discord.Embed(title="Armoury")
            shop.set_author(name=context.author.display_name,icon_url=context.author.avatar_url)
            shop.addfield(name="Buy:",value=f"""
                                {}
                          """)
        @self.bot.command(name="hunt")
        
        async def hunt(context):
            pass

        @self.bot.command(name="abandon")

        async def abandon(context):
            pass

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
                       "power" : x.power,
                       "weapons" : [],
                       "powerups": {}
                    }})
    
    file = open(r"weapons.json","r")
    i=json.load(file)
    armoury = ref.child('weapons')
    armoury.push(i)

        
i=blow(os.getenv("token"))
print(i.run())

