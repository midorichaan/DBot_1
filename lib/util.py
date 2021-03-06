from discord.ext import commands

#resolve_status
def resolve_status(status):        
    if str(status) == "online":
        return "๐ใชใณใฉใคใณ"
    elif str(status) == "dnd":
        return "โคๅใ่พผใฟไธญ"
    elif str(status) == "idle":
        return "๐งก้ๅธญไธญ"
    elif str(status) == "offline":
        return "๐คใชใใฉใคใณ"

#get_region
def get_region(guild):
    region = guild.region
    
    regions = {
        "brazil":"๐ง๐ท Brazil",
        "europe":"๐ช๐บ Europe",
        "hongkong":"๐ญ๐ฐ HongKong",
        "india":"๐ฎ๐ณ India",
        "japan":"๐ฏ๐ต Japan",
        "russia":"๐ท๐บ Russia",
        "singapore":"๐ธ๐ฌ Singapore",
        "southafrica":"๐ฟ๐ฆ SouthAfrica",
        "sydney":"๐ฆ๐บ Sydney",
        "us_central":"๐บ๐ธ US_Central",
        "us_east":"๐บ๐ธ US_East",
        "us_south":"๐บ๐ธ US_South",
        "us_west":"๐บ๐ธ US_West"
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