import discord
from discord.ext import commands

import youtube_dl
import random
import asyncio

options = dict(format="bestaudio/best", 
               extractaudio=True, 
               audioformat="mp3", 
               outtmpl="musics/%(extractor)s-%(id)s-%(title)s.%(ext)s",
               restrictfilenames=True,
               noplaylist=True,
               nocheckcertificate=True,
               ignoreerrors=False,
               logtostderr=True,
               quiet=True,
               no_warnings=True,
               default_search="auto",
               source_address="0.0.0.0",
               verbose=True
              )

ffmpeg_options = dict(before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", options="-vn")
    
ytdl = youtube_dl.YoutubeDL(options)

class YTDLSource(discord.PCMVolumeTransformer):
    
    def __init__(self, src, *, data, vol=0.5):
        super().__init__(src, vol)
        
        self.data = data
        self.title = data.get("title")
        self.url = data.get("url")
    
    @classmethod
    async def create(cls, ctx, url, *, loop=None, q=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        
        if "entries" in data:
            data = data["entries"][0]
            
        if q:
            await ctx.send(f"> キューに {data['title']} を追加しました")
        
        return dict(data=data, url=data["webpage_url"], author=ctx.author, title=data["title"])

    @classmethod
    async def create_source(cls, data, *, loop=None):
        loop = loop or asyncio.get_event_loop()
        who = data["author"]
        
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
        return cls(discord.FFmpegPCMAudio(data['url'], **ffmpeg_options), data=data, author=who)
    
    @classmethod
    async def create_entry(query, *, loop=None):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False, process=False))
        ret = list()
        
        if "entries" not in data:
            ret.append(data["webpage_url"])
        else:
            for e in data["entries"]:
                url = f"https://youtube.com/watch?v={e['url']}"
                ret.append(url)
        
        return ret

class MusicQueue(asyncio.Queue):
    
    def __aiter__(self):
        return self._queue.__iter__()
    
    def __len__(self):
        return self.qsize()
    
    def random(self):
        random.shuffle(self._queue)
    
    def remove(self, index:int):
        del self._queue[index]
    
class mido_music(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(mido_music(bot))
