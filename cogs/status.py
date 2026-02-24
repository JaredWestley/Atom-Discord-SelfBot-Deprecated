import discord
from discord.ext import commands
import asyncio
from utils.helpers import EMBED_COLOUR, VERSION, create_embed
from utils.config import get_stream_url, get_auto_delete_timeout
from colorama import Fore


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def sstream(self, ctx, *, message):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to set your activity to {Fore.CYAN}{message}"+Fore.RESET)
        stream_url = get_stream_url()
        await self.bot.change_presence(activity=discord.Streaming(url=stream_url, name=message, game="Minecraft", platform="YouTube"))
        
    @commands.command()
    async def sgame(self, ctx, *, message):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to set your activity to {Fore.CYAN}{message}"+Fore.RESET)
        game = discord.Game(name=message)
        await self.bot.change_presence(activity=game)
        
    @commands.command()
    async def slistening(self, ctx, *, message):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to set your activity to {Fore.CYAN}{message}"+Fore.RESET)
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening, 
                name=message, 
            ))
            
    @commands.command()
    async def swatching(self, ctx, *, message):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to set your activity to {Fore.CYAN}{message}"+Fore.RESET)
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, 
                name=message
            ))
            
    @commands.command()
    async def stopactivity(self, ctx):
        await ctx.message.delete()
        await self.bot.change_presence(activity=None, status=discord.Status.dnd)
        
    @commands.command()
    async def typing(self, ctx, typing: int = None):
        await ctx.message.delete()
        if typing is None:
            typing = 2
        typingtime = typing * 3600
        typingdis = typingtime / 3600
        print(f"{Fore.YELLOW} | Setting status to typing for - {Fore.CYAN}{typingdis} hours")
        async with ctx.typing():
            await asyncio.sleep(typingtime)
        print(f'{Fore.YELLOW} | Finished typing for {typingdis} hours')
        
    @commands.command()
    async def invisible(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Setting status to invisible for others "+Fore.RESET)
        await self.bot.change_presence(status=discord.Status.invisible)
        
    @commands.command()
    async def online(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Setting status to online for others "+Fore.RESET)
        self.bot.default_status = 'online'
        
    @commands.command()
    async def dnd(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Setting status to dnd for others "+Fore.RESET)
        self.bot.default_status = 'dnd'
        
    @commands.command()
    async def idle(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Setting status to idle for others "+Fore.RESET)
        await self.bot.change_presence(status=discord.Status.idle)
        
    @commands.command()
    async def light(self, ctx):
        await ctx.message.delete()
        from utils.config import get_token
        token = get_token()
        print(f"{Fore.YELLOW} | Setting theme to light for - {Fore.CYAN}{token}"+Fore.RESET)
        import requests
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7',
            'Content-Type': 'application/json',
            'Authorization': token,
        }
        request = requests.Session()
        payload = {'theme': "light"}
        try:
            request.patch("https://canary.discordapp.com/api/v6/users/@me/settings", headers=headers, json=payload)
        except Exception as e:
            print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{e}"+Fore.RESET)
            
    @commands.command()
    async def dark(self, ctx):
        await ctx.message.delete()
        from utils.config import get_token
        token = get_token()
        print(f"{Fore.YELLOW} | Setting theme to dark for - {Fore.CYAN}{token}"+Fore.RESET)
        import requests
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7',
            'Content-Type': 'application/json',
            'Authorization': token,
        }
        request = requests.Session()
        payload = {'theme': "dark"}
        try:
            request.patch("https://canary.discordapp.com/api/v6/users/@me/settings", headers=headers, json=payload)
        except Exception as e:
            print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{e}"+Fore.RESET)


def setup(bot):
    bot.add_cog(Status(bot))
