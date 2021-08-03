import discord
from discord.ext import commands

class mido_help(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    #help
    @commands.command(name="help", description="ヘルプを表示します", usage="[prefix]help [command]")
    async def help(self, ctx, *, cmd=None):
        if cmd:
            c = self.bot.get_command(cmd)
         
            if c:
                e = discord.Embed(title=f"Help - {c.name}", timestamp=ctx.message.created_at)
        
                if c.name == "jishaku":
                    e.add_field(name="説明", value="jishakuを実行します。")
                    e.add_field(name="使用法", value="jishaku [arg1] [arg2] [arg3] | rsp!jsk [arg1] [arg2] [arg3]")
                    e.add_field(name="エイリアス", value=", ".join([f"`{row}`" for row in c.aliases]))
                    e.add_field(name="権限", value="Botオーナーのみ")
                    return await ctx.send(embed=e)
            
                if c.description:
                    e.add_field(name="説明", value=c.description)
                else:
                    e.add_field(name="説明", value="なし")
                
                if c.usage:
                    e.add_field(name="使用法", value=c.usage)
                else:
                    e.add_field(name="使用法", value="なし")
            
                if c.aliases:
                    e.add_field(name="エイリアス", value=", ".join([f"`{row}`" for row in c.aliases]))
                else:
                    e.add_field(name="エイリアス", value="なし")
                
                if c.name in ["kick", "ban"]:
                    e.add_field(name="権限", value="メンバーをBan, メンバーをKick")
                else:
                    e.add_field(name="権限", value="なし")

                return await msg.edit(embed=e)
            else:
                return await ctx.send("> そのコマンドは存在しません")
        else:
            e = discord.Embed(title="Help Menu", timestamp=ctx.message.created_at)
        
            for c in self.bot.commands:
                if c.name == "jishaku":
                    e.add_field(name=c.name, value="jishakuを実行します。")
                else:
                    e.add_field(name=c.name, value=c.description or "説明なし")
        
            return await ctx.send(embed=e)

def setup(bot):
    bot.add_cog(mido_help(bot))