import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

class music_func(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

        self.is_playing=False
        self.is_paused=False

        self.music_queue=[]
        self.YDL_options={'format':'bestaudio','nonplaylist':'True'}
        self.FFMPEG_options={'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options':'-vn'}

        self.vc=None
    def searching_yt(self,video):
        with YoutubeDL(self.YDL_options) as ydl:
            try:
                info=ydl.extract_info("ytsearch:%s"% video,download=False)['entries'][0]
            except Exception:
                return False
        return{'source':info['formats'][0]['url'],'title':info['title']}


    def play_next(self):
        if len(self.music_queue)>0:
            self.is_playing=True

            m_url=self.music_queue[0][0]['source']
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url,**self.FFMPEG_options),after=lambda e: self.play_next())

        else:
            self.is_playing=False


    async def play_music(self,msg):
        if len(self.music_queue)>0:
            self.is_playing=True

            m_url=self.music_queue[0][0]['source']
            if self.vc==None or not self.vc.is_connected():
                self.vc=await self.music_queue[0][1].connect()
                
                if self.vc==None:
                    await msg.send("I can't connect to voice channel")
                    return

            else:
                await self.vc.move_to(self.music_queue[0][1])
            self.music_queue.pop(0)
            self.vc.play(discord.FFmpegPCMAudio(m_url,**self.FFMPEG_options),after=lambda e: self.play_next())

        else:
            self.is_playing=False


    @commands.command(name='play',aliases=['p','playing'],help='play the chosen song ')
    async def play(self,msg,*args):
        query=" ".join(args)


        voicechannel=msg.author.voice.channel
        if voicechannel is None:
            await msg.send("not connected to voice channel")
        elif self.is_paused:
            self.vc.resume()
        else:
            song=self.searching_yt(query)
            if type(song)==type(True):
                await msg.send("try a more specific search")

            else:
                await msg.send("song added")
                self.music_queue.append([song,voicechannel])

                if self.is_playing==False:
                    await self.play_music(msg)


    @commands.command(name='pause',help="pauses the song")
    async def pause(self,msg,*args):
        if self.is_playing:
            self.is_playing=False
            self.is_paused=True
            self.vc.pause()
        elif self.is_paused:
            self.is_paused=False
            self.is_playing=True
            self.vc.resume()
    @commands.command(name='resume',help="resumes the song")
    async def resume(self,msg,*args):
        if self.is_paused:
            self.is_paused=False
            self.is_playing=True
            self.vc.resume()
    @commands.command(name="skip",help="skips the song")
    async def skip (self,msg,*args):
        if self.vc!=None and self.vc:
            self.vc.stop()
            await self.play_music(msg)
    @commands.command(name="leave",help="the bot will leave the channel")
    async def leave(self,msg):
        self.is_playing=False
        self.is_paused=False
        await self.vc.disconnect()
