import discord
import io
import numpy as np 
import pylab
import matplotlib.pyplot as plt
from discord.ext import commands
from cogs.utils.checks import load_optional_config, get_google_entries, embed_perms

from custom_cogs.utils.xkcd import *

class Jplot:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def jplot(self, ctx):
        """Grabbing a plot and cracking a cold one with the boys"""
        # if ctx.invoked_subcommand is None:
        #     await ctx.send(self.bot.bot_prefix + 'Invalid Syntax. See `>help jplot` for more info on how to use this command.')

        await ctx.send(self.bot.bot_prefix + 'Check it out!.')

        np.random.seed(0)

        fig = plt.figure()

        ax = pylab.axes()

        x = np.linspace(0, 10, 100)
        ax.plot(x, np.sin(x) * np.exp(-0.1 * (x - 5) ** 2), 'b', lw=1, label='damped sine')
        ax.plot(x, -np.cos(x) * np.exp(-0.1 * (x - 5) ** 2), 'r', lw=1, label='damped cosine')

        ax.set_title('check it out!')
        ax.set_xlabel('x label')
        ax.set_ylabel('y label')

        ax.legend(loc='lower right')

        ax.set_xlim(0, 10)
        ax.set_ylim(-1.0, 1.0)

        #XKCDify the axes -- this operates in-place
        ax2 = XKCDify(ax, xaxis_loc=0.0, yaxis_loc=1.0,
                      xaxis_arrow='+-', yaxis_arrow='+-',
                      expand_axes=True)

        f = io.BytesIO()
        fig.savefig(f, format='png')
        await ctx.send(file=discord.File(fp=f.getbuffer(), filename="plot.png"))
        f.close()        

    

def setup(bot):
    bot.add_cog(Jplot(bot))
