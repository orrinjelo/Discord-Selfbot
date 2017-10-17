import discord
import io

from discord.ext import commands
from cogs.utils.checks import load_optional_config, get_google_entries, embed_perms

from custom_cogs.utils.xkcd import *

class Gunter:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def gunter(self, ctx):
        """Everyone's favorite penguin"""
        await ctx.message.delete()
        if ctx.invoked_subcommand is None:
            await ctx.send(self.bot.bot_prefix + 'Invalid Syntax. See `>help gunter` for more info on how to use this command.')

    @gunter.command(pass_context=True, name="angry")
    async def angry(self, ctx):
        # await ctx.message.delete()
        await ctx.send(file=discord.File(fp=open("images/angry.gif",'rb'), filename="angry.gif"))

    @gunter.command(pass_context=True, name="annoyed")
    async def annoyed(self, ctx):
        # await ctx.message.delete()
        await ctx.send(file=discord.File(fp=open("images/annoyed.png",'rb'), filename="annoyed.png"))

    @gunter.command(pass_context=True, name="barf")
    async def barf(self, ctx):
        # await ctx.message.delete()
        await ctx.send(file=discord.File(fp=open("images/barf.gif",'rb'), filename="barf.gif"))

    @gunter.command(pass_context=True, name="chained")
    async def chained(self, ctx):
        # await ctx.message.delete()
        await ctx.send(file=discord.File(fp=open("images/chained.gif",'rb'), filename="chained.gif"))

    @gunter.command(pass_context=True, name="dance")
    async def dance(self, ctx):
        # await ctx.message.delete()
        await ctx.send(file=discord.File(fp=open("images/dance.gif",'rb'), filename="dance.gif"))

    @gunter.command(pass_context=True, name="eggface")
    async def eggface(self, ctx):
        # await ctx.message.delete()
        await ctx.send(file=discord.File(fp=open("images/eggface.gif",'rb'), filename="eggface.gif"))

    @gunter.command(pass_context=True, name="haters")
    async def haters(self, ctx):
        # await ctx.message.delete()
        await ctx.send(file=discord.File(fp=open("images/haters.gif",'rb'), filename="haters.gif"))

    @gunter.command(pass_context=True, name="nastybooty")
    async def nastybooty(self, ctx):
        # await ctx.message.delete()
        await ctx.send(file=discord.File(fp=open("images/nastybooty.gif",'rb'), filename="nastybooty.gif"))

    @gunter.command(pass_context=True, name="sick")
    async def sick(self, ctx):
        # await ctx.message.delete()
        await ctx.send(file=discord.File(fp=open("images/sick.gif",'rb'), filename="sick.gif"))

    @gunter.command(pass_context=True, name="thief")
    async def thief(self, ctx):
        # await ctx.message.delete()
        await ctx.send(file=discord.File(fp=open("images/thief.png",'rb'), filename="thief.png"))    

    @gunter.command(pass_context=True, name="wenk")
    async def wenk(self, ctx):
        # await ctx.message.delete()
        await ctx.send(file=discord.File(fp=open("images/wenk.gif",'rb'), filename="wenk.gif"))

def setup(bot):
    bot.add_cog(Gunter(bot))
