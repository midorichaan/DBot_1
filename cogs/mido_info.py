import discord
from discord.ext import commands

from lib import util

class mido_info(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
    
    #ping
    @commands.command(name="ping", description="Ping値を表示します", usage="[prefix]ping")
    async def ping(self, ctx):
        msg = time.perf_counter()
        m = await ctx.send("> Pinging...")
        
        latency = round(self.bot.latency * 1000, 2)
        msg_end = time.perf_counter()
        
        await m.edit(content=f"ぽんぐっ！🏓 \nPing: {round(msg - msg_end, 3) * 1000}\nWebsocket: {latency}")
    
    #userinfo
    @commands.command(name="userinfo", aliases=["ui", "user"], description="ユーザーの情報を表示します。", usage="[prefix]userinfo [user/member]")
    async def userinfo(self, ctx, user:util.FetchUserConverter=None):
        e = discord.Embed(title="User Information", description="処理中", timestamp=ctx.message.created_at)
        msg = await ctx.send(embed=e)
        
        if not user:
            user = ctx.author
            
        e.set_thumbnail(url=user.avatar_url_as(static_format="png"))
        e.description = None
        e.add_field(name="ユーザー名", value=f"{user} \n({user.id})")

        if ctx.guild and isinstance(user, discord.Member):
            e.add_field(name="ニックネーム", value=user.display_name)
        else:
            pass
        
        e.add_field(name="Botか", value="はい" if user.bot else "いいえ")
        
        if isinstance(user, discord.Member):
            if not user.premium_since is None:
                e.add_field(name="Nitroブースター", value=f"{user.premium_since.strftime('%Y/%m/%d %H:%M:%S')}から")
            else:
                e.add_field(name="Nitroブースター", value="なし。")
        else:
            pass
        
        e.add_field(name="アカウント作成日時", value=user.created_at.strftime('%Y/%m/%d %H:%M:%S'))
            
        if isinstance(user, discord.Member):
            e.add_field(name="サーバー参加日時", value=user.joined_at.strftime('%Y/%m/%d %H:%M:%S'))
            e.add_field(name="ステータス", value=util.resolve_status(user.status))
            if not user.activity:
                try:
                    if user.activity.type == discord.ActivityType.custom:
                        e.add_field(name="カスタムステータス", value=user.activity)
                    else:
                        e.add_field(name="カスタムステータス", value=f"{user.activity.name}")
                except:
                    e.add_field(name="カスタムステータス", value=user.activity)
            
            roles = ", ".join(c.mention for c in list(reversed(user.roles)))
            if len(user.roles) <= 1000:    
                e.add_field(name="役職", value=roles, inline=False)
            else:
                e.add_field(name="役職", value="多すぎて表示できないよ！", inline=False)
            e.add_field(name=f"権限 ({user.guild_permissions.value})", value=", ".join("`{}`".format(self.bot.jsondata["roles"].get(c, str(c))) for c,b in dict(user.guild_permissions).items() if b is True), inline=False)

        await msg.edit(embed=e)
    
    #serverinfo
    @commands.command(name="serverinfo", aliases=["si"], description="サーバーの情報を表示します", usage="[prefix]serverinfo [ServerID]")
    async def serverinfo(self, ctx, *, guild:util.GuildConverter=None):
        e = discord.Embed(title="Server Information", description="取得中...", timestamp=ctx.message.created_at)
        msg = await ctx.send(embed=e)
        
        if not guild:
            srvinfo = ctx.guild
        else:
            srvinfo = guild

        if not srvinfo.icon_url == None:
            e.set_thumbnail(url=srvinfo.icon_url_as(static_format="png"))
        e.add_field(name="サーバー名", value=f"{srvinfo.name} \n({srvinfo.id})")
        e.add_field(name="サーバーリージョン", value=util.get_region(srvinfo))
        owner = srvinfo.owner
        if owner is not None:
            e.add_field(name="サーバーオーナー", value=f"{srvinfo.owner} \n({srvinfo.owner.id})")
        else:
            e.add_field(name="サーバーオーナー", value="取得不可")
        e.add_field(name="サーバーブースト", value=f"Level: {srvinfo.premium_tier} ({srvinfo.premium_subscription_count})")
        if srvinfo.mfa_level == 0:
            levels = "False"
        elif srvinfo.mfa_level == 1:
            levels = "True"
        else:
            levels = "Unknown"
        e.add_field(name="セキュリティ", value=f"二段階認証: {levels} \n管理レベル: {srvinfo.verification_level}")
        e.add_field(name="作成日時", value=srvinfo.created_at.strftime('%Y/%m/%d %H:%M:%S'))
        bm = 0
        ubm = 0
        for m in srvinfo.members:
            if m.bot:
                bm = bm + 1
            else:
                ubm = ubm + 1
        e.add_field(name="ユーザー数", value=f"{len(srvinfo.members)} (User: {ubm} Bot: {bm})")
        e.add_field(name="チャンネル数", value=f"Category: {len(srvinfo.categories)} \nCh: {len(srvinfo.channels)} (Text: {len(srvinfo.text_channels)} Voice: {len(srvinfo.voice_channels)})")
        e.add_field(name="絵文字数", value=len(srvinfo.emojis))
        if srvinfo.get_member(ctx.author.id):
            rlist = ", ".join([i.mention for i in srvinfo.roles])
        else:
            rlist = ", ".join([i.name for i in srvinfo.roles])
        if len(rlist) <= 1000:
            e.add_field(name=f"役職({len(srvinfo.roles)})", value=rlist, inline=False)
        else:
            e.add_field(name=f"役職({len(srvinfo.roles)})", value="多すぎて表示できないよ！", inline=False)
        
        await msg.edit(embed=e)

def setup(bot):
    bot.add_cog(mido_info(bot))