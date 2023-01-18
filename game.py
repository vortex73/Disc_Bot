import os
#import message 
from StringProgressBar import progressBar
from dotenv import load_dotenv
import firebase_admin
from typing import List
import random
import json
import discord
from discord import app_commands
from firebase_admin import credentials
from firebase_admin import db
from discord import Game, embeds
from discord.ext.commands import Bot
BOTPREFIX = "/"
load_dotenv()
intents = discord.Intents.all()
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
            hit_prob = (1-random.random()**self.xp)*self.power
            x_hit_prob = random.random()*x.power
            self.health -= x_hit_prob
            x.health -= hit_prob
            if self.health or x.health == 0:
                break

        print(hit_prob,x_hit_prob)
        print(self.health,x.health)
        if self.health>x.health:
            return True
        else:
            return False
    @app_commands.command() 
    async def caution(self,c): # c is context
        warn = discord.Embed(title = "Warning!")
        warn.set_thumbnail(url="")
        warn.add_field(name="",value="")
        await c.message.reply(embed=warn)
        #def test(msg,user):
         #   return user==b.message.author and   
        #replyy = b.wait_for("reaction_add",check=test)
    def hunt():
        pass
    #async def autoc(interaction:discord.Interaction,msg:str)
    def abandon(self):
        self.xp-=10
        return False
    def get_level(self):
        bar = progressBar.filledBar(6,self.level)[1]
        return bar
    def buy():
        pass
    def inc_level(self):
        self.level+=1
        return f"Congrats! {self.name} your level is now {self.level}"
        
    # Space to add more player actions

class user(chars):    #Class for player
    def __init__(self,id,name,typee="Player",power=None,health=100,xp=0,value=None,level=1,money=0):
        super().__init__(typee,power,health,xp,value)
        self.level = level
        self.id = id
        self.name = name
        self.money = money
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
            await self.bot.change_presence(activity=Game(name="Games"))
            self.bulk_store()
            print("[*] Connected to Discord as: " + self.bot.user.name)
            try:
                s = await self.bot.tree.sync() # syncs the bot slash commands
                print(f"{s}")

            except Exception as e :
                print(e)
       
            
            
        @self.bot.command(name='stats')
        async def stats(context):
           # player = {"join_server_date": "2020:2:2","xp_points":20}
           # await context.message.reply(embeds = embed) 
            #await self.bot.say("So you want stats?")
            u = ref.child("user/player")

            embed = discord.Embed(title = "Player Stats")
            embed.set_author(name=context.author.display_name)
            embed.set_thumbnail(url=context.author.avatar_url)
            embed.add_field(name="",value="""<Write something here>""",inline=True)
            await context.message.reply(embed=embed)

        @self.bot.tree.command()
        #@app_commands.autocomplete(atk=auto_cmd)
        async def attack(interaction :discord.Interaction,item:str):
            #player = user(context.author.id,context.author.display_name,power=10)
            # Opponent definition
            await interaction.response.send_message(f"{item}",ephemeral=True)
            #await context.message.reply(atk)
       #     opponent = evil(power=50)
       #     if opponent.xp-player.xp>10:
       #         await player.caution(context)
       #         if player.combat(opponent):
       #             await context.message.reply("You Won!")
       #             await context.message.reply(player.inc_level())
       #         else:
       #             await context.message.reply("You Lost")
       #                     
                      

        @attack.autocomplete("item") 
        async def auto_cmd(interaction:discord.Interaction,current:str)->List[app_commands.Choice[str]]:
            l = []
            for x in ["powerup","kick","punch"]:
                l.append(app_commands.Choice(name=x,value=x))
            return l
        @self.bot.command(name="weapon",help="Lists out the weapons in the Store.")

        async def weapon(context):
            w = ref.child("weapons")
            #g = w.get()
            #wname = list(g.values())
            shop = discord.Embed(title="Shop")
            shop.set_author(name=context.author.display_name ,icon_url=context.author.avatar_url)
            shop.set_thumbnail(url="https://ak.picdn.net/shutterstock/videos/1059212528/thumb/9.jpg?ip=x480")
            for i in w.get().values():   # i={weapons:[{guns:{}}]}
                for j in i.values():     # j=[{guns:{},melee:{}}] list of categories
                    for k in j:          # k={guns:{}}
                        for l in k:         # l=guns
                            lis = []
                            for m in k[l]:
                                lis.append(f"**{m}** : {k[l][m][0]}")
                            liss = '\n'.join(lis)
                            shop.add_field(name=f"{l}",value=f"{liss}")
            await context.message.reply(embed=shop)
        @self.bot.command(name = "level",help="Your level.")
        async def lvl(context):
            client = user(context.author.id,context.author.display_name)
            lvl = discord.Embed(title="Your Level:")
            lvl.add_field(name="",value=client.get_level())
            await context.message.reply(embed=lvl)

        @self.bot.command(name="buy",help="To buy weapons from Store.")

        async def buy(context,item):
            u = ref.child("users/player")
            for i in u.get():
                for j in u.get().values():
                    for k in j:
                        if int(k)==int(context.message.author.id):
                            j[k]["weapons"].update({"bazooka":2000})  # test code to add(update) one article to the db
                            u.update({i:j})
                            break
                        else:
                            continue
                break

                   


        @self.bot.command(name="hunt")
#           
        async def hunt(context):
           pass 
#
#        @self.bot.command(name="abandon")
#
#        async def abandon(context):
#            pass
#
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
                       "money" : x.money,
                       "power" : x.power,
                       "weapons" : {"Stick":20},
                       "powerups": {}
                    }})
    
    file = open(r"weapons.json","r")
    i=json.load(file)
    armoury = ref.child('weapons')
    armoury.push(i)

        
i=blow(os.getenv("token"))


#i.bot.load_extension(r"message.py") # TBD in final steps.
print(i.run())

