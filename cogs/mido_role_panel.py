import discord
from discord.ext import commands

class mido_role_panel(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

 def setup(bot):
    bot.add_cog(mido_role_panel(bot))