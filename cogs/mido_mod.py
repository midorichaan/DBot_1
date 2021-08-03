import discord
from discord.ext import commands

import asyncio

from lib import util

class mido_mod(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.check = "✅"
        self.x = "❌"
    
    #ban
    @commands.command(name="ban", description="メンバー/ユーザーをサーバーからBanします", usage="[prefix]ban <member/user> [reason]")
    @commands.bot_has_permissions(ban_members=True, kick_members=True)
    @commands.has_permissions(ban_members=True, kick_members=True)
    async def ban(self, ctx, member:util.FetchUserConverter=None, *, reason=None):     
        msg = await ctx.send("> 処理中...")
        
        if isinstance(ctx.message.channel, discord.DMChannel):
            return await msg.edit(content="> DMでは使用できません")
        
        if not reason:
            reason = "なし"
        
        if not member:
            return await msg.edit(content="> Banしたいメンバーまたはユーザーを入力してください")
        
        if member.id == ctx.author.id:
            return await msg.edit(content="> 自分自身は指定できません")
        
        banlist = await ctx.guild.bans()
        entity = discord.utils.find(lambda u: str(u.user.id) == member.id, banlist)
        
        if entity:
            return await msg.edit(content="> そのユーザーはすでにBanされています")
        
        await msg.edit(content=f"> {member} ({member.id})をBanしますか？")
        
        await msg.add_reaction(self.check)
        await msg.add_reaction(self.x)
        
        try:
            r,u = await self.bot.wait_for("reaction_add", check=lambda r,u: r.message.id==msg.id and u.id == ctx.message.author.id, timeout=30)
        except asyncio.TimeoutError:
            try:
                await msg.clear_reactions()
            except:
                pass
            return await msg.edit(content="> 30秒が経過したため、自動でキャンセルされました")
        except:
            try:
                await msg.clear_reactions()
            except:
                pass
            return await msg.edit(content="> エラーが発生したため、自動でキャンセルされました")
        
        try:
            if r.emoji == self.check:
                await ctx.guild.ban(member, reason=reason)

                try:
                    await msg.clear_reactions()
                except:
                    pass
                return await msg.edit(content=f"> {member} ({member.id})をこのサーバーからBanしました\n理由: {reason}")
            elif r.emoji == self.x:
                try:
                    await msg.clear_reactions()
                except:
                    pass
                return await msg.edit(content=f"> {member} ({member.id})のBanをキャンセルしました")
        except Exception as exc:
            try:
                await msg.clear_reactions()
            except:
                pass
            return await msg.edit(content=f"> エラー \n```py\n{exc}\n```")
    
    #kick
    @commands.command(name="kick", description="メンバーをサーバーからKickします", usage="[prefix]kick <member> [reason]")
    @commands.bot_has_permissions(ban_members=True, kick_members=True)
    @commands.has_permissions(ban_members=True, kick_members=True)
    async def kick(self, ctx, member:commands.MemberConverter=None, *, reason=None):
        msg = await ctx.send("> 処理中...")
        
        if isinstance(ctx.message.channel, discord.DMChannel):
            return await msg.edit(content="> DMでは使用できません")
        
        if not reason:
            reason = "なし"
        
        if not member:
            return await msg.edit(content="> Kickしたいメンバーを入力してください")
        
        if member.id == ctx.author.id:
            return await msg.edit(content="> 自分自身は指定できません")
        
        await msg.edit(content=f"> {member} ({member.id})をKickしますか？")
        
        await msg.add_reaction(self.check)
        await msg.add_reaction(self.x)
        
        try:
            r,u = await self.bot.wait_for("reaction_add", check=lambda r,u: r.message.id==msg.id and u.id == ctx.message.author.id, timeout=30)
        except asyncio.TimeoutError:
            try:
                await msg.clear_reactions()
            except:
                pass
            return await msg.edit(content="> 30秒が経過したため、自動でキャンセルされました")
        except:
            try:
                await msg.clear_reactions()
            except:
                pass
            return await msg.edit(content="> エラーが発生したため、自動でキャンセルされました")
        
        try:
            if r.emoji == self.check:
                await ctx.guild.kick(member, reason=reason)

                try:
                    await msg.clear_reactions()
                except:
                    pass
                return await msg.edit(content=f"> {member} ({member.id})をこのサーバーからKickしました\n理由: {reason}")
            elif r.emoji == self.x:
                try:
                    await msg.clear_reactions()
                except:
                    pass
                return await msg.edit(content=f"> {member} ({member.id})のKickをキャンセルしました")
        except Exception as exc:
            try:
                await msg.clear_reactions()
            except:
                pass
            return await msg.edit(content=f"> エラー \n```py\n{exc}\n```")

def setup(bot):
    bot.add_cog(mido_mod(bot))