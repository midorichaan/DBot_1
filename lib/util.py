from discord.ext import commands

#resolve_status
def resolve_status(self, status):        
    if str(status) == "online":
        return "💚オンライン"
    elif str(status) == "dnd":
        return "❤取り込み中"
    elif str(status) == "idle":
        return "🧡退席中"
    elif str(status) == "offline":
        return "🖤オフライン"

#get_region
def get_region(guild):
    region = guild.region
    
    regions = {
        "brazil":"🇧🇷 Brazil",
        "europe":"🇪🇺 Europe",
        "hongkong":"🇭🇰 HongKong",
        "india":"🇮🇳 India",
        "japan":"🇯🇵 Japan",
        "russia":"🇷🇺 Russia",
        "singapore":"🇸🇬 Singapore",
        "southafrica":"🇿🇦 SouthAfrica",
        "sydney":"🇦🇺 Sydney",
        "us_central":"🇺🇸 US_Central",
        "us_east":"🇺🇸 US_East",
        "us_south":"🇺🇸 US_South",
        "us_west":"🇺🇸 US_West"
    }
    
    try:
        key = regions[str(region)]
    except KeyError:
        key = str(region)
    
    return key

#FetchUserConverter
class FetchUserConverter(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            return await commands.MemberConverter().convert(ctx, argument)
        except:
            try:
                return await commands.UserConverter().convert(ctx, argument)
            except:
                raise commands.UserNotFound(f"User {argument} not found.")
 
 #GuildConverter
class GuildConverter(commands.Converter):
    async def convert(self, ctx, argument):
        g = None
        if argument.isdigit():
            g = ctx.bot.get_guild(int(argument))
        else:
            if g is None:
                g = discord.utils.get(ctx.bot.guilds, name=argument)
                if g is None:
                    raise commands.GuildNotFound(f"Guild {argument} not found.")
        
        return g