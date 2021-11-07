import discord
from discord.ext import commands

from async_google_trans_new import AsyncTranslator

class mido_trans(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.translator = AsyncTranslator()

    #trans
    @commands.command(name="translate", aliases=["t", "trans"], usage="translate <to_lang> <content>", description="テキストを翻訳します")
    async def translate(self, ctx, lang: str=None, *, content: str=None):
        m = await ctx.reply("> 処理中...")
        
        if not lang:
            lang = "ja"
        
        if not content:
            return await m.edit(content="> 翻訳する内容を入力してね！")
        
        try:
            ret = await self.translator.translate(content, lang)
        except Exception as exc:
            return await m.edit(content=f"> エラー \n```py\n{exc}\n```")
        else:
            return await m.edit(content=f"> Result \n{ret}", allowed_mentions=discord.AllowedMentions.none())

def setup(bot):
    bot.add_cog(mido_trans(bot))
