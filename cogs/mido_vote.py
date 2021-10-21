import discord
from discord.ext import commands

class mido_vote(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.reactions = [
            '🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲', '🇳', 
            '🇴', '🇵', '🇶', '🇷', '🇸', '🇹', '🇺', '🇻', '🇼', '🇽', '🇾', '🇿'
        ]
    
    #vote
    @commands.command(name="vote", aliases=["poll"], description="投票を作成します。", usage="vote <args> [args]")
    async def _vote(self, ctx, question=None, *args=None):
        m = await ctx.reply("> 処理中...")
        
        if not question:
            return await m.edit(content="> 内容を指定してね！")
        
        if not args:
            return await m.edit(content="> オプションを指定してね！")
        
        e = discord.Embed(title=question, description="", color=self.bot.color, timestamp=ctx.message.created_at)
        if len(args) == 1:
            e.description = f"{self.reactions[0]} {args[0]}"
            return await m.edit(content=None, embed=e)
        
        c = 0
        
        for i in args:
            e.description += f"{self.reactions[c]} {i}"
            c += 1
            
        await m.edit(content=None, embed=e)

def setup(bot):
    bot.add_cog(mido_vote(bot))
