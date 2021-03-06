import discord
from discord.ext import commands

class mido_vote(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.reactions = [
            '๐ฆ', '๐ง', '๐จ', '๐ฉ', '๐ช', '๐ซ', '๐ฌ', '๐ญ', '๐ฎ', '๐ฏ', '๐ฐ', '๐ฑ', '๐ฒ', '๐ณ', 
            '๐ด', '๐ต', '๐ถ', '๐ท', '๐ธ', '๐น', '๐บ', '๐ป', '๐ผ', '๐ฝ', '๐พ', '๐ฟ'
        ]
    
    #vote
    @commands.command(name="vote", aliases=["poll"], description="ๆ็ฅจใไฝๆใใพใใ", usage="vote <args> [args]")
    async def _vote(self, ctx, question=None, *, args=None):
        m = await ctx.reply("> ๅฆ็ไธญ...")
        
        if not question:
            return await m.edit(content="> ๅๅฎนใๆๅฎใใฆใญ๏ผ")
        
        if not args:
            return await m.edit(content="> ใชใใทใงใณใๆๅฎใใฆใญ๏ผ")
        
        e = discord.Embed(title=question, description="", color=self.bot.color, timestamp=ctx.message.created_at)
        if len(args) == 1:
            e.description = f"{self.reactions[0]} {args[0]}"
            return await m.edit(content=None, embed=e)
        
        c = 0
        
        for i in args:
            e.description += f"{self.reactions[c]} {i} \n"
            c += 1
            
        await m.edit(content=None, embed=e)

def setup(bot):
    bot.add_cog(mido_vote(bot))
