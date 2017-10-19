import discord
import io

from discord.ext import commands
from cogs.utils.checks import load_optional_config, get_google_entries, embed_perms

class WordSmith:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def wordsmith(self, ctx):
        """A utility to analyze word statistics"""
        await ctx.message.delete()
        if ctx.invoked_subcommand is None:
            await ctx.send(self.bot.bot_prefix + 'Invalid Syntax. See `>help wordsmith` for more info on how to use this command.')

    @wordsmith.command(pass_context=True, name="frequency")
    async def angry(self, ctx):
        # client = discord.Client()
        logs = self.bot.logs_from("testing")
        # print(help(self.bot))
        



def setup(bot):
    bot.add_cog(WordSmith(bot))

    client = discord.Client()
    try:
        client.logs_from
        print('it works')
    except:
        print('what??')