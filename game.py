import os
from dotenv import load_dotenv
import firebase_admin
import discord
from firebase_admin import credentials
from firebase_admin import db
from discord import Game
from discord.ext.commands import Bot
BOTPREFIX = "?"
load_dotenv()
intents = discord.Intents.default()
intents.members = True
intents.presences = True
c = credentials.Certificate(r"key.json")
firebase_admin.initialize_app(c, {'databaseURL': 'https://discbot-f50a9-default-rtdb.firebaseio.com/'})


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
    def __init__(self,typee,power,health,xp,value):
        self.typee = typee
        self.power = power
        self.health = health
        self.xp = xp 
        self.value = value

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
        first_login = True
        @self.bot.event
        async def on_ready():
            await self.bot.change_presence(activity=Game(name="Fun Games"))
            self.bulk_store()
            print("[*] Connected to Discord as: " + self.bot.user.name)
    def bulk_store(self):
        for i in self.bot.get_all_members():
            self.store(i.id)
    def store(self,x):
            global users 
            users.push({x : 1})
        
i=blow(os.getenv("token"))
print(i.run())

