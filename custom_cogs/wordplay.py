import discord
import io
import re

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
    async def frequency(self, ctx):
        try:
            messages = await ctx.history(limit=1000).flatten()
            wordDict = {}
            for msg in messages:
                for word in re.sub(r'([^\s\w]|_)+', '', msg.content).lower().split():
                    if word in wordDict:
                        wordDict[word] += 1
                    else:
                        wordDict[word] = 1
            await ctx.send(self.bot.bot_prefix + 'Frequency report over 1000 messages:')
            count = 0
            for key, val in sorted(wordDict.items(), key=lambda x: (-x[1],x[0])):
                if key in banned:
                    continue
                count += 1
                await ctx.send('\t{0}: {1}'.format(key, val))
                if count == 10:
                    break

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