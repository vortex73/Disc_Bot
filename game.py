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

users = ref.child('users')




class chars:
    def __init__(self,typee,power,health,xp,value):
        self.typee = typee
        self.power = power
        self.health = health
        self.xp = xp 
        self.value = value

    def combat():
        pass

class user(chars):
    def __init__(self,typee,power,health,xp,value,level):
        super().__init__(typee,power,health,xp,value)
        self.level = level
class evil(chars):
    def __init__(self, typee, power, health, xp, value):
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
            await self.bot.change_presence(activity=Game(name="Kola Theme"))
            self.bulk_store()
            print("[*] Connected to Discord as: " + self.bot.user.name)
        @self.bot.command(name='stats')
        async def stats(context):
            player = {"join_server_date": "2020:2:2","xp_points":20}
           # await context.message.reply(embeds = embed) 
            #await self.bot.say("So you want stats?")
            embed = discord.Embed(title = "Kola Sampangi Sambaiah")
            embed.set_author(name=context.author.display_name,icon_url=context.author.avatar_url)
            embed.add_field(name="Iconic lines",value="""
                            **Pa**
                            **Shabash**
                            **Mems**
                            **Thereby**
                            **Kindly**
                            **Therefore**
                            **Wattsup**
                            **inSTAgram**
                            """,inline=True)
            await context.message.reply(embed=embed)
                            

    def bulk_store(self):
        for i in self.bot.get_all_members():
            self.store(i.id)
    def store(self,x):
            global users 
            users.push({x : 1})
        
i=blow(os.getenv("token"))
print(i.run())

