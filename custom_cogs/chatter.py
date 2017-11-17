import discord
import io
import re
import json

from discord.ext import commands
from cogs.utils.checks import load_optional_config, get_google_entries, embed_perms

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

CLIENT_ACCESS_TOKEN = 'f83ff865da164af5bf87b8de4c815e6e'

class Chatter:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, aliases=['ch', 'chat'])
    async def chatter(self, ctx, *msg):
        '''A utility to communicate with Jelobot dialog flow'''
        ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

        request = ai.text_request()

        request.lang = 'en'  # optional, default value equal 'en'

        request.session_id = "jelobot_user_11302"

        request.query = ' '.join(msg)

        response = request.getresponse()

        d = json.loads(response.read().decode('utf-8'))

        await ctx.send(self.bot.bot_prefix + ": " + d['result']['fulfillment']['messages'][0]['speech'])


    @commands.group(pass_context=True, aliases=['xch', 'xchat'])
    async def xchatter(self, ctx, *msg):
        '''A utility to communicate with Jelobot dialog flow'''
        ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

        request = ai.text_request()

        request.lang = 'en'  # optional, default value equal 'en'

        request.session_id = "jelobot_user_11302"

        request.query = ' '.join(msg)

        response = request.getresponse()

        d = json.loads(response.read().decode('utf-8'))

        await ctx.send(self.bot.bot_prefix + ": " + d)


def setup(bot):
    bot.add_cog(Chatter(bot))