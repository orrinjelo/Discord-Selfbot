import discord
import io
import numpy as np 
import pandas as pd
import pylab
import matplotlib.pyplot as plt
from discord.ext import commands
from cogs.utils.checks import load_optional_config, get_google_entries, embed_perms
import datetime as dt
import requests
from requests import get
import os
from urllib.request import urlopen
from PIL import Image
import matplotlib.image as mpimg
import matplotlib.font_manager as fm

from custom_cogs.utils.xkcd import *



prop = fm.FontProperties(fname='Humor-Sans.ttf', size=16)
font = {'fontname':'Comic Sans MS'}

class Jplot:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, name='jplot')
    async def jplot(self, ctx):
        """Grabbing a plot and cracking a cold one with the boys"""
        if ctx.invoked_subcommand is None:
            await ctx.send(self.bot.bot_prefix + 'Invalid Syntax. See `>help jplot` for more info on how to use this command.')


    @jplot.command(pass_context=True, name="xkcd")
    async def xkcd(self, ctx):        
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


    @jplot.command(pass_context=True, name="pandas")
    async def pandas(self, ctx):        
        fig = plt.figure()

        ts = pd.Series(np.random.randn(24*7), index=pd.date_range('1/1/2000', periods=24*7, freq='H'))
        ts = ts.cumsum()
        ts.plot()

        f = io.BytesIO()
        fig.savefig(f, format='png')
        await ctx.send(file=discord.File(fp=f.getbuffer(), filename="plot.png"))
        f.close()  


    @jplot.command(pass_context=True, name="posts", aliases=['post'])
    async def posts(self, ctx, channel, numhours=48, msg_limit=1000):
        freq = 15
        try:
            now = dt.datetime.now() 
            now -= dt.timedelta(minutes = now.minute, seconds = now.second, microseconds = now.microsecond)
            then = now - dt.timedelta(hours=numhours)
            messages = None
            for chan in self.bot.get_all_channels():
                if chan.guild == ctx.guild:
                    if chan.name == channel:
                        messages = await chan.history(limit=msg_limit).flatten()
            if not messages:
                await ctx.send("Channel not found.")
                return
            dcount = {}
            # for msg in messages:
            #     tTime = msg.created_at
            #     tTime -= dt.timedelta(minutes = tTime.minute, seconds = tTime.second, microseconds =  tTime.microsecond)
            #     if tTime in dcount:
            #         dcount[ tTime ] += 1
            #     else:
            #         dcount[ tTime ] = 1 

            dx = {}
            for x in [now - dt.timedelta(hours=h) for h in range(numhours)]:
                dx[str(x)] = 0
            for msg in messages:
                tTime = msg.created_at
                tTime -= dt.timedelta(minutes = tTime.minute, seconds = tTime.second, microseconds =  tTime.microsecond)
                if tTime < then:
                    continue
                if str(tTime) in dx:
                    dx[ str(tTime) ] += 1
                else:
                    dx[ str(tTime) ] = 1

            ts = pd.DataFrame.from_dict(dx, orient='index')      

            ax = ts.plot(kind='barh')
            ax.legend(['member posts'])
            for container in ax.containers:
                plt.setp(container, height=1)
            plt.tight_layout()            
            plt.gca().invert_yaxis()
            plt.title('post histogram for #{0}'.format(channel))
            plt.yticks(range(len(dx.keys()))[::max(1,len(dx.keys())//freq)], sorted(list(dx.keys()))[::max(1,len(dx.keys())//freq)])

            fig = ax.get_figure()

            f = io.BytesIO()
            fig.savefig(f, format='png')
            await ctx.send(file=discord.File(fp=f.getbuffer(), filename="plot.png"))
            f.close()

        except Exception as e:
            print('{}'.format(e)) 
         


    @jplot.command(pass_context=True, name="quote", aliases=['q'])
    async def quote(self, ctx, msg, keyword='abstract'):    
        def wrapstr(mystr, wraplen=38):
            finstr = ''''''

            while mystr:
                maxidx = wraplen if len(mystr)>wraplen-1 else len(mystr)
                if len(mystr) > wraplen:
                    spidx = maxidx - mystr[0:maxidx][::-1].index(' ')
                    finstr += mystr[:spidx-1] + '\n'
                    mystr = mystr[spidx:]
                else:
                    finstr += mystr
                    mystr = ''
            return finstr
        fig, ax = plt.subplots()

        key = '6969366-f7162cb00b48396f58f497b2b'

        response = requests.get(
            'https://pixabay.com/api/',
            params={'key': key,
                    'q': keyword,
                    'category': 'backgrounds',
                    'safesearch': 'true'
                    })

        imageDatas = response.json()['hits']
        hit = np.random.choice(imageDatas)
        img = hit['webformatURL']

        def download(url, file_name):
            # open in binary mode
            with open(file_name, "wb") as file:
                # get request
                response = get(url)
                # write to file
                file.write(response.content)

        download(img, img[-5:])
        im = Image.open(img[-5:])
        im.save('temp.png')
        image = plt.imread('temp.png')
        plt.imshow(image * 0.6 + 0.4)    
        print(hit['imageWidth'], hit['imageHeight'], image.shape)
        plt.text(image.shape[1]//2, image.shape[0]//2, r'{0}'.format(wrapstr(msg,image.shape[1]//20)), fontdict=font, horizontalalignment='center', verticalalignment='center')
        for text in ax.texts:
            text.set_fontproperties(prop)
        ax.set_xticks([])
        ax.set_yticks([])     

        f = io.BytesIO()
        fig.savefig(f, format='png')
        await ctx.send(file=discord.File(fp=f.getbuffer(), filename="quote.png"))
        f.close()

def setup(bot):
    bot.add_cog(Jplot(bot))
