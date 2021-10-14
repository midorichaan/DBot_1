import discord
from discord.ext import commands

class mido_ticket(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
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
        db = self.bot.db.execute("SELECT * FROM ticketconfig WHERE guild_id=?", (ctx.guild.id, ))
        
        if db:
            e = discord.Embed(title=f"{author} Ticket", description=f"```\n{reason or '理由なし'}\n```", color=self.bot.color)
            chs = [i for i in ctx.guild.channels if str(author.id) in i.name]
            
            ow = {
                ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                ctx.guild.get_role(db["role_id"]): discord.PermissionOverwrite(read_messages=True, add_reactions=True, view_channel=True, send_messages=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
                author: discord.PermissionOverwrite(read_messages=True, add_reactions=True, view_channel=True, send_messages=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
            }
            ch = await ctx.guild.get_channel(db["category_id"]).create_text_channel(name=f"ticket-{author.id}-{len(chs)}", overwrites=ow)
            m = await ch.send(embed=e)
            await m.add_reaction("🔒")
            
            self.bot.db.execute("INSERT INTO tickets VALUES(?, ?, ?, ?)", (ch.id, m.id, author.id, 1))
    
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
                return await m.edit(content="> そのコマンドは存在しないよ！")
            return await m.edit(content=None, embed=self.gen_help(ctx, c))
        else:
            return await m.edit(content=None, embed=self.gen_help(ctx))
    
    #ticket panel
    @ticket.command(name="panel", description="チケットのパネルを作成/削除します", usage="panel <create/delete> [channel]")
    async def panel(self, ctx, mode: str=None, channel: commands.TextChannelConverter=None):
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
        else:
            return await m.edit(content="> createかdeleteか指定してね！")
        
def setup(bot):
    bot.add_cog(mido_ticket(bot))
