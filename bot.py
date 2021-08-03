import discord
from discord.ext import commands, tasks

import aiohttp
import logging
import datetime
import traceback
import gc
import json

import config

class Bot(commands.Bot):
    
    def __init__(self):
        self.command_prefix = config.PREFIX
        self.status = discord.Status.idle
        self.owner_id = config.OWNER_ID
        self.config = config
        self.http.token = config.BOT_TOKEN
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.logging = logging.getLogger("discord")
        self.jsondata = None
        self.uptime = None
        self._ext = list()
        self._is_ready = False
        self.intents = discord.Intents.all()
        
        logging.basicConfig(level=logging.WARNING, format="[DebugLog] %(levelname)-8s: %(message)s")
    
    @tasks.loop(minutes=10.0)
    async def gc_loop():
        print("[System] auto gc start")
        
        try:
            f = gc.collect()
            s = gc.collect()
            
            print(f"[System] auto gc end → {f} - {s}")
        except Exception as exc:
            print(f"[Error] auto gc failed → {exc}")
    
    async def on_ready(self):
        print("[System] enabling...")
        
        self._ext = ["cogs.mido_mod", "cogs.mido_info", "cogs.mido_role_panel", "cogs.mido_music", "cogs.mido_vote", "cogs.mido_help"]
        
        for ext in self._ext:
            try:
                self.load_extension(ext)
                print(f"[System] {ext} load")
            except Exception as exc:
                print(f"[Error] {ext} load failed → {exc}")
       
        try:
            self.gc_loop.start()
            print(f"[System] auto gc loop start")
        except Exception as exc:
            print(f"[Error] auto gc loop start failed → {exc}")
        
        self.uptime = datetime.datetime.now()
        
        try:
            with open("./lib/jsondata.json", "r", encoding="utf-8") as f:
                self.jsondata = json.load(f)
            
            print("[System] jsondata load")
        except Exception as exc:
            print(f"[Error] jsondata load failed → {exc}")
        
        if not self._is_ready:
            try:
                self.remove_command("help")
                print("[System] Command 'help' removed")
            except:
                print("[Error] Command 'help' remove failed")
            
            self._is_ready = True
        
        await self.change_presence(status=discord.Status.online, activity=discord.Game(name=f"{self.command_prefix}help"))
        print("[System] on_ready!")
    
    async def on_connect(self):
        print("[System] on_connect!")
    
    async def on_command(self, ctx):
        if isinstance(ctx.message.channel, discord.DMChannel):
            print(f"[Log] {ctx.author} ({ctx.author.id}) → {ctx.message.content} @{ctx.channel} ({ctx.channel.id})")
        else:
            print(f"[Log] {ctx.author} ({ctx.author.id}) → {ctx.message.content} @{ctx.channel} ({ctx.channel.id})")
    
    async def reply_or_send(self, ctx, *, content):
        try:
            await ctx.reply(content)
        except:
            await ctx.send(content)

    async def on_command_error(self, ctx, exc):
        traceback_exc = f"```{''.join(traceback.TracebackException.from_exception(exc).format())}```"
        
        if len(str(traceback_exc)) >= 1024:
            exc = exc
        else:
            exc = traceback_exc
        
        if isinstance(exc, commands.NotOwner):
            await self.reply_or_send(ctx, "> Botオーナーのみが使用できます")
        elif isinstance(exc, commands.CommandNotFound):
            await self.reply_or_send(ctx, "> そのコマンドは存在しません")
        elif isinstance(exc, commands.MemberNotFound):
            await self.reply_or_send(ctx, "> そのメンバーは見つかりませんでした")
        elif isinstance(exc, commands.UserNotFound):
            await self.reply_or_send(ctx, "> そのユーザーは見つかりませんでした")
        elif isinstance(exc, commands.MissingPermissions):
            p = ", ".join([self.jsondata["roles"].get(i) for i in exc.missing_perms])
            await self.reply_or_send(ctx, f"> 権限が不足してます\n{p}")
        elif isinstance(exc, commands.BotMissingPermissions):
            p = ", ".join([self.jsondata["roles"].get(i) for i in exc.missing_perms])
            await self.reply_or_send(ctx, f"> Botの権限が不足してます\n{p}")
        else:
            await self.reply_or_send(ctx, f"> エラー \n```py\n{exc}\n```")
        
        print(f"[Error] {exc}")

    def run(self):
        self.run(self.http.token)
    
    async def close(self):
        try:
            self.session.close()
            print("[System] Session closed")
        except Exception as exc:
            print("[Error] Session close failed → {exc}")
        
        await super().close()

bot = Bot()
bot.run()