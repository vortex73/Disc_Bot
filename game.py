import os
#import message 
from StringProgressBar import progressBar
from dotenv import load_dotenv
import firebase_admin
from typing import List
import random
import json
import asyncio
import discord
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
    #def get_setting():

    def store_hp(self,id,hp):

        w = ref.child("users")
        for i in w.get():
            if int(i)==int(id):
                temp=w.get()[i]
                temp["health"]=hp
                w.update({i:temp})
    def get_hp(self,id):
        w = ref.child("users")
        for i in w.get():
            if int(i)==int(id):
                return w.get()[i]["health"]
    def get_op_hp(self,id):
        v = ref.child("users").get()[id]["Villains"][self.name]
        return [v["health"],v["power"]]
    def str_op_hp(self,id,hp):
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
        bar = progressBar.filledBar(6,self.level)[1]
        return bar
    def buy():
        pass
    def inc_level(self):
        self.level+=1
        return f"Congrats! {self.name} your level is now {self.level}"
        
    # Space to add more player actions

class user(chars):    #Class for player
    def __init__(self,id,name,typee="Player",power=None,health=100,xp=1,value=None,level=1,money=0):
        super().__init__(typee,power,health,xp,value)
        self.level = level
        self.id = id
        self.name = name
        self.money = money
class evil(chars):  #Class for opponents
    def __init__(self,name,power, typee="System wardogs", health=100, xp=1000, value=None,lower_blk=0,upper_blk=0):
        super().__init__(typee, power, health, xp, value)
        self.name = name
    def block(self):
        self.lower_blk=random.choice([0,1])
        self.upper_blk=random.choice([0,1])
            

class blow():
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
        def get(name):
            w = ref.child("weapons")
            for i in w.get().values():   # i={weapons:[{guns:{}}]}
                for j in i.values():  # j=[{guns:{},melee:{}}] list of categories\
                    for k in j:   
                        for l in k:         # l=guns 
                            for m in k[l]:
                                if m==name:
                                    return k[l][m]


         
        async def atk_cmd(i:discord.Interaction,current:str)->list[app_commands.Choice[str]]:
            l = []
            for x in ["powerup","kick","punch"]:
                l.append(app_commands.Choice(name=x,value=x))
            return l
        async def buy_cmd(i:discord.Interaction,current:str)->list[app_commands.Choice[str]]:
            w = ref.child("weapons")
            for i in w.get().values():   # i={weapons:[{guns:{}}]}
                for j in i.values():  # j=[{guns:{},melee:{}}] list of categories\
                    cat = []
                    for k in j:          # k={guns:{}}
                        for l in k:         # l=guns
                            cat.append(app_commands.Choice(name=l,value=l)) 
            return cat 
        async def buy_item(i:discord.Interaction,current:str)->list[app_commands.Choice[str]]:
            w = ref.child("weapons")
            for i in w.get().values():   # i={weapons:[{guns:{}}]}
                print(f"current = {current}") 
                for j in i.values():  # j=[{guns:{},melee:{}}] list of categories\
                    lis=[]
                    for k in j:   
                        for l in k:         # l=guns 
                            
                            for m in k[l]:
                                lis.append(app_commands.Choice(name=m,value=m))
                        
                    #print(dic)
                    return lis

            
              
            
            
        @self.bot.tree.command(name="stats",description="Player stats.")
        async def stats(context):
           # player = {"join_server_date": "2020:2:2","xp_points":20}
           # await context.message.reply(embeds = embed) 
            #await self.bot.say("So you want stats?")

            embed = discord.Embed(title = "Brilliant")
            embed.set_author(name=context.author.display_name,icon_url=context.author.avatar_url)
            embed.add_field(name="Testing",value="""
                            Wow
                            """,inline=True)

            embed = discord.Embed(title = "")
            embed.set_author(name=context.author.display_name,icon_url=context.author.avatar_url)
            u = ref.child("user/player")

            embed = discord.Embed(title = "Player Stats")
            embed.set_author(name=context.author.display_name)
            embed.set_thumbnail(url=context.author.avatar_url)
            embed.add_field(name="",value="""<Write something here>""",inline=True)

            await context.message.reply(embed=embed)

        @self.bot.tree.command(name="attack",description="Launch an attack on the nearest boss")
        @app_commands.autocomplete(attack=atk_cmd)
        #@app_commands.autocomplete(atk=auto_cmd)
        async def attack(i :discord.InteractionResponse,attack:str)->list[app_commands.Choice[str]]:
            player = user(i.user.id,i.user.display_name,power=10)
            v = get_villain(player)
            x = ref.child("users").get()[str(i.user.id)]["Villains"][v]
            oppo = evil(name=v,health=x["health"],power=x["power"])
            await i.response.defer()
            fn=player.combat(oppo,str(i.user.id),attack)
            if fn:
            
                if fn[0]>0 and fn[1]>0 :
                    await i.followup.send(f"Your health is {fn[0]},opponent health is {fn[1]}")
                elif fn[0]<=0:
                    await i.followup.send(f"You lost")
                else:
                    await i.followup.send("you won")
            else:
                await i.followup.send("Your attack was blocked")
        @self.bot.tree.command(name="weapon",description="Lists out the weapons in the Store.")

        async def weapon(interaction):
            w = ref.child("weapons")
            #g = w.get()
            #wname = list(g.values())
            shop = discord.Embed(title="Shop")
            shop.set_author(name=interaction.user.display_name ,icon_url=interaction.user.display_avatar)
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
            await interaction.response.send_message(embed=shop,ephemeral=True)

        @self.bot.tree.command(name="level",description="know your level")
        async def lvl(context):
            client = user(context.user.id,context.user.display_name)
            lvl = discord.Embed(title="Your Level:")
            lvl.add_field(name="",value=client.get_level())
            await context.response.send_message(embed=lvl)

        @self.bot.tree.command(name="buy",description="Purchase items from the store.")
       # @app_commands.autocomplete(item=buy_item)
        @app_commands.autocomplete(category=buy_cmd,item=buy_item)
        async def buy(i:discord.Interaction,category:str,item:str)->list[app_commands.Choice[str]]:
             purchase = discord.Embed(title = "Your Purchase")
             purchase.add_field(name="category",value=category)
             purchase.add_field(name="Item",value=item)
             purchase.add_field(name="Cost",value=get(item)[0])
             purchase.add_field(name="Damage",value=get(item)[1])
             await i.response.send_message(embed=purchase,ephemeral=True)
        
       # @app_commands.autocomplete(item=buy_item)
       # async def buying(i:discord.Interaction,item:str)->list[app_commands.Choice[str]]:

 


#            u = ref.child("users/player")
#            for i in u.get():
#                for j in u.get().values():
#                    for k in j:
#                        if int(k)==int(context.message.author.id):
#                            j[k]["weapons"].update({f"{item}":2000})  # test code to add(update) one article to the db
#                            u.update({i:j})
#                            break
#                        else:
#                            continue
#                break
#
                   


       # @self.bot.tree.command() 
       # async def hunt(context):
       #    pass 
#
#        @self.bot.command(name="abandon")
#
#        async def abandon(context):
#            pass
#
    def bulk_store(self):      # Function to store all the members in the server
        for i in self.bot.get_all_members():
            if ref.child("users").get()==None or i.id not in ref.child('users').get() :
                x=user(i.id,i.name)
                self.store(x)

    def store(self,x):         # Function to push given datapoint into DB
            
            users = ref.child('users')
            users.update({
                x.id:{"typee":x.typee,
                       "Name" : x.name,
                       "xp" : x.xp,
                       "level" : x.level,
                       "health":x.health,
                       "money" : x.money,
                       "power" : x.power,
                       "weapons" : {"Stick":20},
                       "powerups": {},
                      "Villains": {'Boss1': {'health': 100, 'power': 10,'xp':10},
                                   'Boss2': {'health': 100, 'power': 20,'xp':30},
                                   'Boss3': {'health': 100, 'power': 30,'xp':50},
                                   'Boss4': {'health': 100, 'power': 40,'xp':70},
                                   'Boss5': {'health': 100, 'power': 50,'xp':100}
}
                    }})
    
    file = open(r"weapons.json","r")
    i=json.load(file)
    armoury = ref.child('weapons')
    armoury.push(i)

        
i=blow(os.getenv("token"))


#i.bot.load_extension(r"message.py") # TBD in final steps.
print(i.run())

