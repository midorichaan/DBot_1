import discord
from discord.ext import commands

class mido_role_panel(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
        self.bot.execute("CREATE TABLE IF NOT EXISTS panelroles(panel_id integer PRIMARY KEY NOT NULL, roles json)")
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        db = self.bot.db.execute("SELECT * FROM panelroles WHERE panel_id=?", (payload.message_id,)).fetchone()
        
        if db:
            role = db["roles"].get(str(payload.emoji), None)
            
            if role:
                m = payload.member
                msg = await self.bot.fetch_message(payload.message_id)
                r = self.bot.get_guild(payload.guild_id).get_role(role)
                
                if m.id == self.bot.user.id:
                    return
                
                try:
                    await msg.remove_reaction(str(payload.emoji), m)
                except:
                    pass
                
                try:
                    if int(role) in [i.id for i in m.roles]:
                        await m.remove_roles(r)
                        await msg.channel.send("役職を剥奪しました！", delete_after=3)
                    else:
                        await m.add_roles(r)
                        await msg.channel.send("役職を付与しました！", delete_after=3)
                except Exception as exc:
                    await msg.channel.send("エラーが発生したため、役職を付与できませんでした")
                    await msg.channel.send(f"```py\n{exc}\n```")
    
    #rolepanel
    @commands.group(name="rolepanel", aliases=["rp", "panel"], description="役職パネル関連のコマンドです", usage="[prefix]rolepanel <args> [args]", invoke_without_command=True)
    async def rolepanel(self, ctx):
        pass
    
    #rolepanel help
    @rolepanel.command(name="help", description="ヘルプを表示します。", usage="[prefix]rolepanel help")
    async def help(self, ctx, cmd=None):
        e = discord.Embed(title="Rolepanel - help", description="", timestamp=ctx.message.created_at)
        
        if cmd:
            c = self.bot.get_command(cmd)
            
            if c:
                e.add_field(name="説明", value=c.description)
                e.add_field(name="使用法", value=c.usage)
                e.add_field(name="エイリアス", value=", ".join([f"`{row}`" for row in c.aliases]))
            else:
                return await ctx.send("そのコマンドは存在しません")
        else:
            for i in self.bot.get_command("rolepanel").commands:
                e.add_field(name=i.name, value=i.description)
        
        await ctx.send(embed=e)
    
    #rolepanel delete
    @rolepanel.command(name="delete", description="パネルを削除します", usage="[prefix]rolepanel delete <panel_id>", brief="役職の管理")
    async def delete(self, ctx, panel_id: int=None):
        if not panel_id:
            return await ctx.send("パネルIDを指定してください。")
        
        if not ctx.author.guild_permissions.manage_roles:
            return await ctx.send("権限がありません")
        
        try:
            m = await ctx.channel.fetch_message(panel_id)
        except Exception as exc:
            await ctx.send(f"メッセージが見つからなかった、またはエラーが発生しました")
            return await ctx.send(f"> Debug Log\n```py\n{exc}\n```")
        
        db = self.bot.db.execute("SELECT * FROM panelroles WHERE panel_id=?", (panel_id,)).fetchone()
        
        if db:
            self.bot.db.execute("DELETE FROM panelroles WHERE panel_id=?", (panel_id,))
            return await ctx.send("削除しました！")
        else:
            return await ctx.send("パネルが存在しません")
    
    #rolepanel create
    @rolepanel.command(name="create", description="パネルを作成します。", usage="[prefix]rolepanel create")
    async def create(self, ctx):
        e = discord.Embed(title="役職パネル")
        e.set_footer(text=f"{ctx.author} によって作成されました")
        
        m = await ctx.send(embed=e)
        self.bot.cursor.execute("INSERT INTO panelroles(panel_id, roles) VALUES(?, ?)", (m.id, {}))
        await ctx.send(f"パネルを作成しました！\nパネルID: {m.id}")
    
    #rolepanel add
    @rolepanel.command(name="add", description="パネルに役職を追加します", usage="[prefix]rolepanel add <panel_id> <emoji> <role>", brief="役職の管理")
    async def add(self, ctx, panel_id: int=None, emoji: str=None, role: commands.RoleConverter=None):
        if not panel_id:
            return await ctx.send("パネルIDを入力してください")
        
        if not emoji:
            return await ctx.send("絵文字を入力してください")
        
        if not role:
            return await ctx.send("ロールを入力してください")
        
        if not ctx.author.guild_permissions.manage_roles:
            return await ctx.send("権限がありません")
        
        try:
            m = await ctx.channel.fetch_message(panel_id)
        except Exception as exc:
            await ctx.send(f"メッセージが見つからなかった、またはエラーが発生しました")
            return await ctx.send(f"> Debug Log\n```py\n{exc}\n```")
        
        db = self.bot.db.execute("SELECT * FROM panelroles WHERE panel_id=?", (panel_id,)).fetchone()
        
        if db:
            rd = db["roles"]
            
            if rd.get(str(emoji), None) is None:
                rd[str(emoji)] = role.id
                self.bot.db.execute("UPDATE panelroles SET roles=? WHERE panel_id=?", (rd, panel_id))
                e = m.embeds[0]
                e.add_field(name=emoji, value=role.mention)
                await m.edit(embed=e)
                await m.add_reaction(emoji)
                return await ctx.send("追加しました！")
            else:
                return await ctx.send("その絵文字は使用できません")
        else:
            return await ctx.send("そのIDのパネルは存在しません")
    
    #rolepanel remove
    @rolepanel.command(name="remove", description="パネルからロールを削除します", usage="[prefix]rolepanel remove <panel_id> <emoji>", brief="役職の管理")
    async def remove(self, ctx, panel_id: int=None, emoji: int=None):
        if not panel_id:
            return await ctx.send("パネルIDを入力してください")
        
        if not emoji:
            return await ctx.send("絵文字を入力してください")
        
        if not ctx.author.guild_permissions.manage_roles:
            return await ctx.send("権限がありません")
        
        try:
            m = await ctx.channel.fetch_message(panel_id)
        except Exception as exc:
            await ctx.send(f"メッセージが見つからなかった、またはエラーが発生しました")
            return await ctx.send(f"> Debug Log\n```py\n{exc}\n```")
        
        db = self.bot.db.execute("SELECT * FROM panelroles WHERE panel_id=?", (panel_id,)).fetchone()
        
        if db:
            rd = db["roles"]
            
            if rd.get(str(emoji), None) is None:
                del rd[str(emoji)]
                self.bot.db.execute("UPDATE panelroles SET roles=? WHERE panel_id=?", (rd, panel_id))
                e = m.embeds[0]
                e.clear_fields()
                [e.add_field(name=k, value=ctx.guild.get_role(v).mention) for k, v in rd.items()]
                
                await m.edit(embed=e)
                
                await m.clear_reactions()
                
                for i in rd.keys():
                    try:
                        await m.add_reaction(i)
                    except Exception as exc:
                        await ctx.send(f"エラーが発生しました")
                        return await ctx.send(f"> Debug Log\n```py\n{exc}\n```")
                    
                return await ctx.send("完了しました！")
            else:
                return await ctx.send("その絵文字は使用できません")
        else:
            return await ctx.send("そのIDのパネルは存在しません")
    
 def setup(bot):
    bot.add_cog(mido_role_panel(bot))
