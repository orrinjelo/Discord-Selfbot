import discord
import io
import re

from discord.ext import commands
from cogs.utils.checks import load_optional_config, get_google_entries, embed_perms

class Chatter:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, aliases=['ch', 'chat'])
    async def chatter(self, ctx, *msg):
        '''A utility to communicate with Jelobot dialog flow'''
        await ctx.send(' '.join(msg))


def setup(bot):
    bot.add_cog(Chatter(bot))