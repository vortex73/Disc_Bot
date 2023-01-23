import os
#import message 
from StringProgressBar import progressBar
from dotenv import load_dotenv
import firebase_admin
from typing import List
import random
from datetime import datetime,timedelta
import json
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from firebase_admin import credentials
from firebase_admin import db
from discord import Game, embeds
from discord.ext.commands import Bot
BOTPREFIX = "!"
load_dotenv()
intents = discord.Intents.all()
intents.members = True
intents.presences = True


class game(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
         
        self.c = credentials.Certificate(r"key.json")
        firebase_admin.initialize_app(self.c, {'databaseURL': 'https://discbot-f50a9-default-rtdb.firebaseio.com/'})

#client = discord.Client(command_prefix = "!",intents = intents)
        self.ref = db.reference("/")
        self.weapon = self.ref.child("weapons")
        self.w = self.ref.child("users")
        self.bulk_store() 
        self.initialize()
    def bulk_store(self):      # Function to store all the members in the server
        for i in self.bot.get_all_members():
            if self.ref.child("users").get()==None or i.id not in self.ref.child('users').get() :
                x=self.user(i.id,i.name)
                self.store(x)

    def store(self,x):         # Function to push given datapoint into DB
            
            users = self.ref.child('users')
            users.update({
                x.id:{"typee":x.typee,
                       "Name" : x.name,
                       "xp" : x.xp,
                       "level" : x.level,
                       "health":x.health,
                       "money" : x.money,
                       "power" : x.power,
                       "weapons" : {"Stick":20},
                       "cooldown":"",
                       "powerups": {},
                      "Villains": {'Boss1': {'health': 100, 'power': 10,'xp':10},
                                   'Boss2': {'health': 100, 'power': 20,'xp':30},
                                   'Boss3': {'health': 100, 'power': 30,'xp':50},
                                   'Boss4': {'health': 100, 'power': 40,'xp':70},
                                   'Boss5': {'health': 100, 'power': 50,'xp':100},
                                   'trainer':{'health':100, 'power': x.power+5,'xp':x.xp+10}
}
                    }})
    
            file = open(r"weapons.json","r")
            i=json.load(file)
            armoury = self.ref.child('weapons')
            armoury.update(i)

    class chars:  #Parent Class for general charachter outline
        def __init__(self,typee,power,health,xp,value):
            self.typee = typee
            self.power = power
            self.health = health
            self.xp = xp 
            self.value = value
        #def get_setting():

        def store_hp(self,id,hp):
            ref = db.reference("/")
            w = ref.child("users")
            for i in w.get():
                if int(i)==int(id):
                    temp=w.get()[i]
                    temp["health"]=hp
                    w.update({i:temp})
        def get_hp(self,id):
            ref = db.reference("/")
            w = ref.child("users")
            for i in w.get():
                if int(i)==int(id):
                    return w.get()[i]["health"]
        def get_op_hp(self,id):
            ref = db.reference("/")
            v = ref.child("users").get()[id]["Villains"][self.name]
            return [v["health"],v["power"]]
        def str_op_hp(self,id,hp):
            ref = db.reference("/")
            v = ref.child("users") 
            temp = v.get()[id]
            temp["Villains"][self.name]["health"]=hp
            v.update({id:temp})
        def combat(self,x,id,atck):
            oppo_hp ,xp= x.get_op_hp(id)
            player_health = self.get_hp(id)
            print(player_health,oppo_hp)
            if "kick" in atck:
                x.block()
                if x.lower_blk==1:
                    return False
                else:
                    hit_prob = (1-random.random()**self.xp)*self.power
                    x_hit_prob = (1-random.random()**x.xp)*x.power
                    player_health-=x_hit_prob
                    oppo_hp-=hit_prob
                    print(hit_prob,x_hit_prob)
                    print(player_health,oppo_hp)
                    self.store_hp(id,player_health)
                    x.str_op_hp(id,oppo_hp)
                    return [player_health,oppo_hp]

            else:
                x.block()
                if x.upper_blk==1:
                    return False
                else:
                    hit_prob = (1-random.random()**self.xp)*self.power
                    x_hit_prob = (1-random.random()**x.xp)*x.power
                    player_health-=x_hit_prob
                    oppo_hp-=hit_prob
                    
                    print(hit_prob,x_hit_prob)
                    print(player_health,oppo_hp)
                    self.store_hp(id,player_health)
                    x.str_op_hp(id,oppo_hp)
                    return [player_health,oppo_hp]
                #hit_prob = (1-random.random()**self.xp)*self.power
                #x_hit_prob = random.random()*x.power
                #self.health -= x_hit_prob
                #x.health -= hit_prob
               # if self.health or x.health == 0:
                #    break

            #if self.health>x.health:
            #    return True
           # else:
            #    return False
        
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
            level = self.w.get()[str(self.id)]["level"]
            bar = progressBar.filledBar(6,level)[0]
            return bar
        def buy():
            pass 
        def inc_level(self,id):
            
            x = self.w.get()[id]
            x["level"] += 1
            self.w.update({id:x})
            with open("story.json") as f:
                d = json.load(f)
            a = d[str(x["level"])]
            level = discord.Embed(title="Level Up")
            level.add_field(name="",value=f"Promoted to level {x['level']}")
            level.set_thumbnail(url="https://img.freepik.com/premium-vector/game-icon-bonus-level-up-icon-new-level-logo-neon-icon-vector-illustration_100456-4960.jpg?w=740")
            stry = discord.Embed(title="Next")
            stry.add_field(name="",value=f"{a['stry']} ")
            stry.set_image(url=f"{a['img']}")
            return level,stry
            
        # Space to add more player actions
     
    class user(chars):    #Class for player
        def __init__(self,id,name,typee="Player",power=10,health=100,xp=1,value=None,level=1,money=0,blck=False):
            super().__init__(typee,power,health,xp,value)
            self.level = level
            self.id = id
            self.name = name
            self.money = money
            self.ref = db.reference("/")
            self.w = self.ref.child("users")
            
    class evil(chars):  #Class for opponents
        def __init__(self,name,power=20, typee="System wardogs", health=100, xp=1000, value=None,lower_blk=0,upper_blk=0):
            super().__init__(typee, power, health, xp, value)
            self.name = name
        def block(self):
            self.lower_blk=random.choice([0,1])
            self.upper_blk=random.choice([0,1])
                

                
    def initialize(self):
        
        @self.bot.event
        async def on_ready():
            await self.bot.change_presence(activity=Game(name="Koala"))
            await self.bot.change_presence(activity=Game(name="Games"))
            self.bulk_store()
            print("[*] Connected to Discord as: " + self.bot.user.name)
            try:
                s = await self.bot.tree.sync() # syncs the bot slash commands
                print(f"{s}")

            except Exception as e :
                print(e)

        @self.bot.event
        async def on_member_join(x):
            self.bulk_store()
            
        def get_villain(x):
            l = x.level
            return "Boss"+str(l) 
         
        async def atk_cmd(i:discord.Interaction,current:str)->list[app_commands.Choice[str]]:
            l = []
            for x in ["powerup","kick","punch"]:
                l.append(app_commands.Choice(name=x,value=x))
            return l
        async def buy_cmd(i:discord.Interaction,current:str)->list[app_commands.Choice[str]]:
            w = self.ref.child("weapons")
            l = []
            for x in w.get():
                l.append(app_commands.Choice(name = x, value=x))
            return l
        async def buy_item(i:discord.Interaction,current:str)->list[app_commands.Choice[str]]:
            w = self.ref.child("weapons")
            
            l = []
            for x in w.get():
                for y in w.get()[x]:
                    l.append(app_commands.Choice(name = y, value=y))
            return l

            
              
        @self.bot.tree.command(name="story",description="The story so far")
        async def story(i:discord.Interaction):
            await i.response.defer() 
            with open("story.json") as f:
                d = json.load(f)
            stry = discord.Embed(title="Story")
            for x in d:
                if int(x)<=int(self.w.get()[str(i.user.id)]["level"]):
                    stry.add_field(name=f"Level {x}",value=f"{d[x]['stry']}")
            stry.set_image(url="https://rukminim1.flixcart.com/image/850/500/kuyf8nk0/poster/t/3/6/medium-the-punisher-frank-castle-marvel-comics-matte-finish-original-imag7ys46cfaurh6.jpeg?q=90")
            await i.followup.send(embed=stry)
                    

            
        @self.bot.tree.command(name="stats",description="Player stats.")
        async def stats(i):
           # player = {"join_server_date": "2020:2:2","xp_points":20}
           # await context.message.reply(embeds = embed) 
            #await self.bot.say("So you want stats?")
            await i.response.defer() 
            embed = discord.Embed(title = "Player Stats")
            embed.set_author(name=i.user.display_name,icon_url=i.user.display_avatar)
            embed.add_field(name="",value="""
                            Wow
                            """,inline=True)

            embed = discord.Embed(title = "")
            embed.set_author(name=i.user.id,icon_url=i.user.display_avatar)
            u = self.ref.child("user/player")

            embed = discord.Embed(title = "Player Stats")
            embed.set_author(name=i.user.display_name)
            embed.set_thumbnail(url=i.user.display_avatar)
            embed.add_field(name="",value="""<Write something here>""",inline=True)

            await i.followup.send(embed=embed)

        @self.bot.tree.command(name="attack",description="Launch an attack on the nearest boss")
        @app_commands.autocomplete(attack=atk_cmd)
        #@app_commands.autocomplete(atk=auto_cmd)
        async def attack(i :discord.InteractionResponse,attack:str)->list[app_commands.Choice[str]]:
            u = self.ref.child("users")
            t = u.get()[str(i.user.id)]["cooldown"]
            if str(datetime.now())>t:

                player = self.user(i.user.id,i.user.display_name,power=10)
                v = get_villain(player)
                x = self.ref.child("users").get()[str(i.user.id)]["Villains"][v]
                oppo = self.evil(name=v,health=x["health"],power=x["power"])
                await i.response.defer()
                fn=player.combat(oppo,str(i.user.id),attack)
                result = discord.Embed(title = "Status")
                result.add_field(name="Match",value=f"{i.user.display_name} vs {v}")
                if fn:
                
                    if fn[0]>0 and fn[1]>0 :
                       
                        result.add_field(name="Your Health",value=progressBar.filledBar(100,int(fn[0]))[0],inline=False)
                        result.add_field(name=f"{v} Health",value=progressBar.filledBar(100,int(fn[1]))[0],inline=False)
                        result.set_footer(text="Use /attack to continue the match. HP resets in 20 minutes of inactivity",icon_url="")
                        await i.followup.send(embed=result)
                    elif fn[0]<=0:
                        result.add_field(name="Defeat",value="Starting 2 hour cooldown")
                        await i.followup.send(f"You lost")
                        for x in u.get():
                            if int(i.user.id)==int(x):
                                temp = u.get()[x]
                                temp["cooldown"] = str(datetime.now()+timedelta(2))
                                u.update({x:temp})

                    else:
                        a,b=player.inc_level(str(i.user.id))
                        await i.followup.send(embeds=[a,b])

                        
                else:
                    await i.followup.send("Your attack was blocked")
            else:
                await i.response.send_message(f"Your on Cooldown till {t}")
        @self.bot.tree.command(name="weapon",description="Lists out the weapons in the Store.")

        async def weapon(i:discord.Interaction):
            await i.response.defer()
            w = self.ref.child("weapons").get()
            #g = w.get()
            #wname = list(g.values())
            
            shop = discord.Embed(title="Shop")
            shop.set_author(name=i.user.display_name ,icon_url=i.user.display_avatar)
            shop.set_image(url="https://ak.picdn.net/shutterstock/videos/1059212528/thumb/9.jpg?ip=x480")
            for x in w:
                l=[]
                for j in w[x]:
                    l.append(j)
                l="\n".join(l)
                shop.add_field(name=x,value=l)
            await i.followup.send(embed=shop,ephemeral=False)

        @self.bot.tree.command(name="level",description="know your level")
        async def lvl(context):
            client = self.user(context.user.id,context.user.display_name)
            lvl = discord.Embed(title="Your Level:")
            lvl.add_field(name="",value=client.get_level())
            await context.response.send_message(embed=lvl)

        @self.bot.tree.command(name="balance",description="Check your Balance.")
        async def balance(i:discord.Interaction):
            await i.response.defer()
            b = discord.Embed()
            b.add_field(name="Balance",value=f"{self.w.get()[str(i.user.id)]['money']}")
            await i.followup.send(embed=b,ephemeral=True)
        @self.bot.tree.command(name="buy",description="Purchase items from the store.")
       # @app_commands.autocomplete(item=buy_item)
        @app_commands.autocomplete(category=buy_cmd,item=buy_item)
        async def buy(i:discord.Interaction,category:str,item:str)->list[app_commands.Choice[str]]:
             await i.response.defer()
             purchase = discord.Embed(title = "Your Purchase")
             x = self.w.get()
             b = x[str(i.user.id)]
             for x in self.weapon.get():
                # for y in self.weapon.get()[x]:
                if item in self.weapon.get()[x] : 
                    if int(b["money"])>int(self.weapon.get()[x][item][0]):
                        purchase.add_field(name="category",value=category)
                        purchase.add_field(name="Item",value=item)
                        purchase.add_field(name="Cost",value=f"{self.weapon.get()[x][item][0]}")
                        purchase.add_field(name="Damage",value=f"{self.weapon.get()[x][item][1]}")
                        b["money"]-=self.weapon.get()[x][item][0]
                        b["weapons"][item]=self.weapon.get()[x][item][1]
                        self.w.update({str(i.user.id):b})
                    else:
                        
                        purchase.add_field(name="You Poor Young Man",value="Insufficient Funds")
             await i.followup.send(embed=purchase,ephemeral=True)
        


        @self.bot.tree.command(name="train",description="Train and gain more xp")
        @app_commands.autocomplete(atck=atk_cmd)
        async def hunt(i:discord.Interaction,atck:str)->list[app_commands.Choice[str]]:
            player = self.user(i.user.id,i.user.display_name,power=10)
            w = self.ref.child("users").get()
            t = w[str(player.id)]["Villains"]["trainer"]
            oppo = self.evil(name="trainer",health=t["health"],power=t["power"],xp=t["xp"])
            await i.response.defer()
            fn = player.combat(oppo,str(player.id),atck)
            if fn:
                if fn[0]>0 and fn[1]>0:
                    await i.followup.send(f"your hp is {fn[0]} and opponent hp is {fn[1]}")
                elif fn[0]<=0: 
                    await i.followup.send(f"you lost")
                else:
                    await i.followup.send("you won")
            else:
                await i.followup.send("Your attack was blocked")
#     def bulk_store(self):      # Function to store all the members in the server
#         for i in self.bot.get_all_members():
#             if self.ref.child("users").get()==None or i.id not in self.ref.child('users').get() :
#                 x=self.user(i.id,i.name)
#                 self.store(x)

#     def store(self,x):         # Function to push given datapoint into DB
            
#             users = self.ref.child('users')
#             users.update({
#                 x.id:{"typee":x.typee,
#                        "Name" : x.name,
#                        "xp" : x.xp,
#                        "level" : x.level,
#                        "health":x.health,
#                        "money" : x.money,
#                        "power" : x.power,
#                        "weapons" : {"Stick":20},
#                        "cooldown":"",
#                        "powerups": {},
#                       "Villains": {'Boss1': {'health': 100, 'power': 10,'xp':10},
#                                    'Boss2': {'health': 100, 'power': 20,'xp':30},
#                                    'Boss3': {'health': 100, 'power': 30,'xp':50},
#                                    'Boss4': {'health': 100, 'power': 40,'xp':70},
#                                    'Boss5': {'health': 100, 'power': 50,'xp':100},
#                                    'trainer':{'health':100, 'power': x.power+5,'xp':x.xp+10}
# }
#                     }})
    
#             file = open(r"weapons.json","r")
#             i=json.load(file)
#             armoury = self.ref.child('weapons')
#             armoury.push(i)

        
#i=blow(os.getenv("token"))


#i.bot.load_extension(r"message.py") # TBD in final steps.
#print(i.run())

