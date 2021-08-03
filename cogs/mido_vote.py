import discord
from discord.ext import commands

class mido_vote(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(mido_vote(bot))