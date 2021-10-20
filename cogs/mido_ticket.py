import discord
from discord.ext import commands

class mido_ticket(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
        self.bot.db.execute("CREATE TABLE IF NOT EXISTS tickets(channel_id int, panel_id int, author_id int, status int)")
        self.bot.db.execute("CREATE TABLE IF NOT EXISTS ticketconfig(guild_id int, category_id int, admin_role_id int, mention int)")
        self.bot.db.execute("CREATE TABLE IF NOT EXISTS ticketpanel(panel_id int, channel_id int, guild_id int, author_id int)")
        
    #is_mod
    def is_mod(ctx):
        if ctx.guild:
            return ctx.author.guild_permissions.manage_guild
        return False
    
    #gen_help
    def gen_help(self, ctx, cmd=None):
        if cmd:
            e = discord.Embed(title=f"Ticket Help - {cmd.name}", color=self.bot.color, timestamp=ctx.message.created_at)
            e.add_field(name="説明", value=cmd.description or "なし")
            e.add_field(name="使用法", value=cmd.usage or "なし")
            e.add_field(name="エイリアス", value=", ".join([f"`{row}`" for row in cmd.aliases]) or "なし")
            return e
        e = discord.Embed(title="Ticket Help", color=self.bot.color, timestamp=ctx.message.created_at)
        
        for i in self.ticket.commands:
            e.add_field(name=i.name, value=i.description or "なし")
        return e
    
    #create_ticket
    async def create_ticket(self, ctx, author, *, reason=None):
        db = self.bot.db.execute("SELECT * FROM ticketconfig WHERE guild_id=?", (ctx.guild.id, )).fetchone()
        
        if db:
            e = discord.Embed(title=f"{author} Ticket", description=f"```\n{reason or '理由なし'}\n```", color=self.bot.color)
            chs = [i for i in ctx.guild.channels if str(author.id) in i.name]
            
            ow = {
                ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                ctx.guild.get_role(db["role_id"]): discord.PermissionOverwrite(read_messages=True, add_reactions=True, view_channel=True, send_messages=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
                author: discord.PermissionOverwrite(read_messages=True, add_reactions=True, view_channel=True, send_messages=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
            }
            ch = await ctx.guild.get_channel(db["category_id"]).create_text_channel(name=f"ticket-{author.id}-{len(chs)}", overwrites=ow)
            
            if db["mention"]:
                m = await ch.send(content=f"{author.mention} {ctx.guild.get_role(db['admin_role_id']).mention} →", embed=e)
            else:
                m = await ch.send(content=f"{author.mention} →", embed=e)
            await m.add_reaction("🔒")
            
            self.bot.db.execute("INSERT INTO tickets VALUES(?, ?, ?, ?)", (ch.id, m.id, author.id, 1))
    
    #listener
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        config = self.bot.db.execute("SELECT * FROM ticketconfig WHERE guild_id=?", (payload.guild_id,)).fetchone()
        if not config:
            return
        
        db = self.bot.db.execute("SELECT * FROM tickets WHERE channel_id=?", (payload.channel_id,)).fetchone()
        if not db:
            return
        
    
    #ticket
    @commands.group(name="ticket", description="チケット関連のコマンドです。", invoke_without_command=False)
    async def ticket(self, ctx):
        pass
    
    #ticket help
    @ticket.command(name="help", description="チケットのヘルプです")
    async def help(self, ctx, cmd=None):
        m = await ctx.reply("> 処理中...")
        
        if cmd:
            c = self.ticket.get_command(cmd)
            
            if not c:
                return await m.edit(content=">  そのコマンドは存在しないよ！")
            return await m.edit(content=None, embed=self.gen_help(ctx, c))
        else:
            return await m.edit(content=None, embed=self.gen_help(ctx))
    
    #ticket panel
    @ticket.command(name="panel", description="チケットのパネルを作成/削除します", usage="panel <create/delete> [channel]")
    @commands.check(is_mod)
    async def panel(self, ctx, mode: str=None, panel_id: typing.Optional[int]=None, channel: commands.TextChannelConverter=None):
        m = await ctx.reply("> 処理中...")
        
        if not channel:
            channel = ctx.channel
        
        if mode == "create":
            e = discord.Embed(title="Ticket Panel", description="リアクションをクリックするとチケットを発行できます。", color=self.bot.color)
            msg = await channel.send(embed=e)
            await msg.add_reaction("📩")
            
            self.bot.db.execute("INSERT INTO ticketpanel VALUES(?, ?, ?, ?)", (msg.id, channel.id, ctx.guild.id, ctx.author.id))
            return await m.edit(content="> 作成しました！")
        elif mode == "delete":
            if not panel_id:
                return await m.edit(content="> パネルIDを入力してね！")
            
            db = self.bot.db.execute("SELECT * FROM ticketpanel WHERE panel_id=?", (panel_id,)).fetchone()
            
            if not db:
                return await m.edit(content="> パネルIDを確認してね！")
            
            self.bot.db.execute("DELETE FROM ticketpanel WHERE panel_id=?", (panel_id,))
            return await m.edit(content="> パネルを削除したよ！")
        else:
            return await m.edit(content="> createかdeleteか指定してね！")
    
    #ticket close
    @ticket.command(name="close", description="チケットをクローズします。", usage="close")
    async def close(self, ctx):
        m = await ctx.reply("> 処理中...")
        
        db = self.bot.db.execute("SELECT * FROM tickets WHERE channel_id=?", (ctx.channel.id,)).fetchone()
        
        if not db:
            return await m.edit(content="> このチャンネルはチケットチャンネルじゃないよ！")
        
        if not db["status"] == 1:
            return await m.edit(content="> このチャンネルはすでにクローズされているよ！")
        
        self.bot.db.execute("UPDATE tickets SET status=0 WHERE channel_id=?", (ctx.channel.id,))
        await m.edit(content="> チケットをクローズしたよ！")
    
    #ticket create
    @ticket.command(name="create", description="チケットを作成します", usage="create [reason]")
    async def create(self, ctx, *, reason=None):
        m = await ctx.reply("> 処理中...")
        
        db = self.bot.db.execute("SELECT * FROM ticketconfig WHERE guild_id=?", (ctx.guild.id,)).fetchone()
        if not db:
            return await m.edit(content="> データが存在しないよ！")
        
        cat = ctx.guild.get_channel(db["category_id"])
        if not cat:
            return await m.edit(content="> チャンネルが存在しないよ！")
        
        try:
            await self.create_ticket(ctx, ctx.author, reason=reason)
            return await m.edit(content="> チケットを作成しました！")
        except:
            return await m.edit(content="> チケットを作成できなかったよ...")
    
    #ticket config
    @ticket.command(name="config", description="チケットシステムの設定を変更します", usage="ticket config [options..]", invoke_without_command=False)
    @commands.check(is_mod)
    async def config(self, ctx):
        pass
    
    #config role
    @config.command(name="role", description="チケット作成時にメンションするロールを設定します", usage="config role <role>")
    @commands.check(is_mod)
    async def role(self, ctx, role: commands.RoleConverter=None):
        m = await ctx.reply("> 処理中...")
        
        if not role:
            return await m.edit(content="> ロールが存在しないよ！")
        
        db = self.bot.db.execute("SELECT * FROM ticketconfig WHERE guid_id=?", (ctx.guild.id,)).fetchone()
        if not db:
            return await m.edit(content="> データが存在しないよ！")
        
        self.bot.db.execute("UPDATE ticketconfig SET admin_role_id=? WHERE guild_id=?", (role.id, ctx.guild.id))
        await m.edit(content="> 設定を変更したよ！")
    
    #config mentino
    @config.command(name="mention", description="チケット作成時にメンションするか設定します", usage="config mention <on/off>")
    @commands.check(is_mod)
    async def mention(self, ctx, mention: bool=False):
        m = await ctx.reply("> 処理中...")
        
        db = self.bot.db.execute("SELECT * FROM ticketconfig WHERE guid_id=?", (ctx.guild.id,)).fetchone()
        if not db:
            return await m.edit(content="> データが存在しないよ！")
        
        self.bot.db.execute("UPDATE ticketconfig SET mention=? WHERE guild_id=?", (int(mention), ctx.guild.id))
        await m.edit(content="> 設定を変更したよ！")
    
    #config category
    @config.command(name="category", description="チケットを作成するカテゴリを設定します", usage="config category <category>")
    @commands.check(is_mod)
    async def category(self, ctx, category: commands.CategoryChannelConverter=None):
        m = await ctx.reply("> 処理中...")
        
        if not category:
            return await m.edit(content="> カテゴリを入力してね！")
        
        db = self.bot.db.execute("SELECT * FROM ticketconfig WHERE guid_id=?", (ctx.guild.id,)).fetchone()
        if not db:
            return await m.edit(content="> データが存在しないよ！")
        
        self.bot.db.execute("UPDATE ticketconfig SET category_id=? WHERE guild_id=?", (category.id, ctx.guild.id))
        await m.edit(content="> 設定を変更したよ！")
    
def setup(bot):
    bot.add_cog(mido_ticket(bot))
