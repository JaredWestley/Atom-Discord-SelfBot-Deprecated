import discord
from discord.ext import commands
import aiohttp
import asyncio
import requests
from utils.helpers import EMBED_COLOUR, VERSION, create_embed
from utils.config import get_auto_delete_timeout
from colorama import Fore


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def joke(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Sending in a joke for you!"+Fore.RESET)
        headers = {"Accept": "application/json"}
        async with aiohttp.ClientSession() as session:
            async with session.get("https://icanhazdadjoke.com", headers=headers) as req:
                r = await req.json()
        await ctx.send(r["joke"])
        
    @commands.command()
    async def wyr(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Sending a Would you rather"+Fore.RESET)
        r = requests.get('https://www.conversationstarters.com/wyrqlist.php').text
        from bs4 import BeautifulSoup as bs4
        soup = bs4(r, 'html.parser')
        qa = soup.find(id='qa').text
        qor = soup.find(id='qor').text
        qb = soup.find(id='qb').text
        em = create_embed(description=f'{qa}\n{qor}\n{qb}')
        msg = await ctx.send(embed=em)
        await msg.add_reaction("🇦")
        await msg.add_reaction("🇧")
        
    @commands.command()
    async def ascii(self, ctx, *, text):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to send {text} in Ascii"+Fore.RESET)
        import urllib.parse
        r = requests.get(f'http://artii.herokuapp.com/make?text={urllib.parse.quote_plus(text)}').text
        if len('```'+r+'```') > 2000:
            return
        await ctx.send(f"```{r}```")
        
    @commands.command()
    async def topicstarter(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Sending a topic starter"+Fore.RESET)
        r = requests.get('https://www.conversationstarters.com/generator.php').content
        from bs4 import BeautifulSoup as bs4
        soup = bs4(r, 'html.parser')
        topic = soup.find(id="random").text
        await ctx.send(topic)
        
    @commands.command()
    async def abcs(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Listing the ABC's"+Fore.RESET)
        ABC = ['a', 'a, b', 'a, b, c', 'a, b, c, d', 'a, b, c, d, e', 'a, b, c, d, e, f', 
               'a, b, c, d, e, f, g', 'a, b, c, d, e, f, g, h', 'a, b, c, d, e, f, g, h, i', 
               'a, b, c, d, e, f, g, h, i, j', 'a, b, c, d, e, f, g, h, i, j, k', 
               'a, b, c, d, e, f, g, h, i, j, k, l', 'a, b, c, d, e, f, g, h, i, j, k, l, m', 
               'a, b, c, d, e, f, g, h, i, j, k, l, m, n', 'a, b, c, d, e, f, g, h, i, j, k, l, m, n, o', 
               'a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p', 'a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q', 
               'a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r', 'a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s', 
               'a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t', 
               'a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u', 
               'a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v', 
               'a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w', 
               'a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x', 
               'a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y', 
               'a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z', 
               "Now you know your abc's!"]
        message = await ctx.send(ABC[0])
        await asyncio.sleep(1)
        for _next in ABC[1:]:
            await message.edit(content=_next)
            await asyncio.sleep(1)
            
    @commands.command()
    async def caps(self, ctx, *, message):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Making {Fore.CYAN}{message} {Fore.YELLOW}Upercase ^ "+Fore.RESET)
        await ctx.send(message.upper())
        
    @commands.command()
    async def devowel(self, ctx, *, text):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Devoweling - {Fore.CYAN}{text}"+Fore.RESET)
        dvl = text.replace('a', '').replace('A', '').replace('e', '')\
                .replace('E', '').replace('i', '').replace('I', '')\
                .replace('o', '').replace('O', '').replace('u', '').replace('U', '')
        await ctx.send(dvl)
        
    @commands.command()
    async def virus(self, ctx, user: discord.Member = None):
        await ctx.message.delete()
        if user is None:
            user = ctx.author
        print(f"{Fore.YELLOW} | Injecting a Virus into - {Fore.CYAN}{user}"+Fore.RESET)
        mention = user
        Virus = [f'`Downloading Exploit.exe -`',
                  '`Downloading Exploit.exe |`',
                  '`Downloading Exploit.exe -`',
                  '`Downloading Exploit.exe |`', 
                  '`Downloading Exploit.exe -`', 
                 f"`Attempting to inject Exploit.exe into {mention}'s PC`",
                  '`Eploit.exe injected!`', 
                 f"`Attempting to remote connect to {mention}'s PC -`", 
                 f"`Attempting to remote connect to {mention}'s PC |`", 
                 f"`Attempting to remote connect to {mention}'s PC -`", 
                 f"`Attempting to remote connect to {mention}'s PC |`", 
                 f"`Connected to {mention}'s`", 
                  "`Running exploit!`", 
                  "`Stealing Data & Copying passwords`",
                 f"`Operation complete, I'd recommend changing all your passwords quickly {mention}!`" 
                ]
        message = await ctx.send(Virus[0])
        await asyncio.sleep(1)
        for _next in Virus[1:]:
            await message.edit(content=_next)
            await asyncio.sleep(1)
            
    @commands.command()
    async def tweet(self, ctx, username: str, *, message: str):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Creating a Tweet as - {Fore.CYAN}{username}"+Fore.RESET)
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://nekobot.xyz/api/imagegen?type=tweet&username={username}&text={message}") as r:
                res = await r.json()
        timeout = get_auto_delete_timeout()
        await ctx.send(f'{res["message"]}', delete_after=timeout)


def setup(bot):
    bot.add_cog(Fun(bot))
