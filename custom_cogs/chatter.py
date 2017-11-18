import discord
import io
import re
import json
import wikipedia

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

        try:
            if d['result']['action'] == "web.search":
                res, root = await get_google_entries(d['result']['parameters']['q'])
                await ctx.send(self.bot.bot_prefix + ": Well, I did find this: " + res[0])
            elif d['result']['action'] == "wikipedia.search":
                await ctx.send(self.bot.bot_prefix + ": " + wikipedia.summary(d['result']['parameters']['q'][:1980]))
            else:
                await ctx.send(self.bot.bot_prefix + ": " + d['result']['fulfillment']['messages'][0]['speech'])
        except Exception as e:
            await ctx.send(self.bot.bot_prefix + ": I'm sorry, I don't know how to respond to that.  I haz teh dumbz. ({})".format(e))


    @commands.group(pass_context=True, aliases=['xch', 'xchat'])
    async def xchatter(self, ctx, *msg):
        '''A utility to communicate with Jelobot dialog flow'''
        ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

        request = ai.text_request()

        request.lang = 'en'  # optional, default value equal 'en'

        request.session_id = "jelobot_user_11302"

        request.query = ' '.join(msg)

        response = request.getresponse()

        jsr = response.read().decode('utf-8')

        d = json.loads(jsr)

        await ctx.send(self.bot.bot_prefix + ": " + jsr)
        print(d)


def setup(bot):
    bot.add_cog(Chatter(bot))