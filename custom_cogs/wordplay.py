import discord
import io
import re
from wordcloud import WordCloud
import datetime as dt

from discord.ext import commands
from cogs.utils.checks import load_optional_config, get_google_entries, embed_perms

import pandas as pd 
import matplotlib.pyplot as plt

class WordSmith:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, aliases=['ws'])
    async def wordsmith(self, ctx):
        """A utility to analyze word statistics"""
        await ctx.message.delete()
        if ctx.invoked_subcommand is None:
            await ctx.send(self.bot.bot_prefix + 'Invalid Syntax. See `>help wordsmith` for more info on how to use this command.')

    @wordsmith.command(pass_context=True, name="frequency", aliases=['freq'])
    async def frequency(self, ctx, channel, maxmsg=1000):
        try:
            messages = None
            for chan in self.bot.get_all_channels():
                if chan.guild == ctx.guild:
                    if chan.name == channel:
                        messages = await chan.history(limit=maxmsg).flatten()
            if not messages:
                await ctx.send("Channel not found.")
                return
            wordDict = {}
            for msg in messages:
                for word in re.sub(r'([^\s\w]|_)+', '', msg.content).lower().split():
                    if word in banned:
                        continue
                    if word in wordDict:
                        wordDict[word] += 1
                    else:
                        wordDict[word] = 1

            # em = discord.Embed(color=0xbc0b0b, description='Frequency report over {0} messages for channel #{1}:'.format(maxmsg, channel))             
            # count = 0
            # for key, val in sorted(wordDict.items(), key=lambda x: (-x[1],x[0])):
            #     if key in banned:
            #         continue
            #     count += 1
            #     em.add_field(name=key, value=val, inline=False)
            #     if count == 10:
            #         break

            # em.set_author(name='Jelobot WordSmith Frequency Analyzer')
            # await ctx.send(embed=em)

            wordcloud = WordCloud().generate_from_frequencies(wordDict)
            
            fig = plt.figure()
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            f = io.BytesIO()
            fig.savefig(f, format='png', bbox_inches='tight', pad_inches = 0, transparent=True)
            await ctx.send(file=discord.File(fp=f.getbuffer(), filename="wordcloud.png"))
            f.close()        


        except Exception as e:
            print('{}'.format(e))
        
    # @wordsmith.command(pass_context=True, name="channels", aliases=['chan','chans','ch'])
    # async def channels(self, ctx, channel):
    #     try:
    #         pass
    #     except:
    #         print("Fail.")

    @wordsmith.command(pass_context=True, name="posts", aliases=['post'])
    async def posts(self, ctx, channel, maxmsg=1000):
        try:
            messages = None
            for chan in self.bot.get_all_channels():
                if chan.guild == ctx.guild:
                    if chan.name == channel:
                        messages = await chan.history(limit=maxmsg).flatten()
            if not messages:
                await ctx.send("Channel not found.")
                return
            dcount = {}
            for msg in messages:
                tTime = msg.created_at
                tTime -= dt.timedelta(minutes = tTime.minute, seconds = tTime.second, microseconds =  tTime.microsecond)
                if tTime in dcount:
                    dcount[ tTime ] += 1
                else:
                    dcount[ tTime ] = 1

 

            dx = {}
            for x in [min(dcount) + dt.timedelta(hours=h) for h in range((max(dcount) - min(dcount)).seconds // 60**2 + (max(dcount) - min(dcount)).days * 24)]:
                dx[str(x)] = 0
            for k in dcount.keys():
                dx[str(k)] = dcount[k]
            ts = pd.DataFrame.from_dict(dx, orient='index')      

            ax = ts.plot(kind='barh')
            plt.tight_layout()            

            fig = ax.get_figure()
            
            f = io.BytesIO()
            fig.savefig(f, format='png')
            await ctx.send(file=discord.File(fp=f.getbuffer(), filename="plot.png"))
            f.close()

        except Exception as e:
            print('{}'.format(e)) 


def setup(bot):
    bot.add_cog(WordSmith(bot))

banned = '''a
about
all
also
and
as
at
be
because
but
by
can
come
could
day
do
even
find
first
for
from
get
give
go
have
he
her
here
him
his
how
I
if
in
into
it
its
just
know
like
look
make
man
many
me
more
my
new
no
not
now
of
on
one
only
or
other
our
out
people
say
see
she
so
some
take
tell
than
that
the
their
them
then
there
these
they
thing
think
this
those
time
to
two
up
use
very
want
way
we
well
what
when
which
who
will
with
would
year
you
your'''
