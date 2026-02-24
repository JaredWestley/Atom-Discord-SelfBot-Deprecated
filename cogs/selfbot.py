import discord
from discord.ext import commands
import os
from utils.helpers import EMBED_COLOUR, VERSION, create_embed
from utils.config import get_auto_delete_timeout
from colorama import Fore


class SelfBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def clear(self, ctx):
        await ctx.message.delete()
        def cls():
            os.system('cls' if os.name=='nt' else 'clear')
        cls()
        print("Console cleared")
        
    @commands.command()
    async def restart(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Restarting AtomSB..."+Fore.RESET)
        os.system(r"AtomSB.exe")
        
    @commands.command()
    async def logout(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Goodbye, I hope to see you again soon!"+Fore.RESET)
        await self.bot.logout()
        
    @commands.command()
    async def pcspecs(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Getting PC Specs..."+Fore.RESET)
        try:
            import GPUtil
            import psutil
            import platform
            import shutil
            gpus = GPUtil.getGPUs()
            list_gpus = []
            for gpu in gpus:
                gpu_name = gpu.name
            uname1 = platform.uname()
            svmem = psutil.virtual_memory()
            release = uname1.release
            version = uname1.version
            Machine = uname1.machine
            Memory = int(svmem.total/1053741824)
            GPU = gpu.name
            total, used, free = shutil.disk_usage("/")
            total = int(total/1053741824)
            free = int(free/1053741824)
            em = create_embed(title="PcSpecs")
            em.add_field(name='System', value=f'Windows {release}', inline=False)
            em.add_field(name='Version', value=f'{version}', inline=False)
            em.add_field(name='Memory', value=f'{Memory} GB', inline=False)
            em.add_field(name='GPU', value=f'{GPU}', inline=False)
            em.add_field(name='Free Storage on Boot Drive', value=f'{free} GB', inline=False)
            em.add_field(name='Total Storage on Boot Drive', value=f'{total} GB', inline=False)
            await ctx.send(embed=em, delete_after=get_auto_delete_timeout())
        except Exception as e:
            print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{e}"+Fore.RESET)
            
    @commands.command()
    async def price(self, ctx, curen: str = None):
        await ctx.message.delete()
        if curen is None:
            await ctx.send(">> Please specify a currency\nAvaliable Currency's: `Ethereum (eth), Bitcoin (btc), Litecoin (ltc), Monero (xmr)`")
            return
        import requests
        if curen.lower() == "btc" or curen.lower() == "bitcoin":
            try:
                with requests.session() as ses:
                    resp = ses.get('https://blockchain.info/ticker')
                    pret = resp.json()['USD']['last']
                    pret1 = resp.json()['EUR']['last']
                    em = create_embed(title="Bitcoin Price", description="Show's the current Bitcoin Price!")
                    em.add_field(name="The current Price is:", value=f"${pret}\n€{pret1}", inline=True)
                    await ctx.send(embed=em, delete_after=get_auto_delete_timeout())
            except Exception as e:
                await ctx.send(f"Error: {e}")
        elif curen.lower() == "eth" or curen.lower() == "ethereum":
            try:
                with requests.session() as ses:
                    resp = ses.get('https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD,EUR,GBP')
                    pret = resp.json()['USD']
                    pret1 = resp.json()['EUR']
                    em = create_embed(title="Ethereum Price", description="Show's the current Ethereum Price!")
                    em.add_field(name="The current Price is:", value=f"${pret}\n€{pret1}", inline=True)
                    await ctx.send(embed=em, delete_after=get_auto_delete_timeout())
            except Exception as e:
                await ctx.send(f"Error: {e}")
        elif curen.lower() == "ltc" or curen.lower() == "litecoin":
            try:
                with requests.session() as ses:
                    resp = ses.get('https://min-api.cryptocompare.com/data/price?fsym=LTC&tsyms=USD,EUR,GBP')
                    pret = resp.json()['USD']
                    pret1 = resp.json()['EUR']
                    em = create_embed(title="Litecoin Price", description="Show's the current Litecoin Price!")
                    em.add_field(name="The current Price is:", value=f"${pret}\n€{pret1}", inline=True)
                    await ctx.send(embed=em, delete_after=get_auto_delete_timeout())
            except Exception as e:
                await ctx.send(f"Error: {e}")
        else:
            await ctx.send("Invalid currency!")
            
    @commands.command()
    async def read(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Marking all unread chats as read"+Fore.RESET)
        for guild in self.bot.guilds:
            await guild.ack()
        
    @commands.command()
    async def wasted(self, ctx, *, user: discord.Member):
        await ctx.message.delete()
        pfp = user.avatar_url
        print(f"{Fore.YELLOW} | Wasted - {Fore.CYAN}{user.name}"+Fore.RESET)
        await ctx.send(f"https://some-random-api.ml/canvas/wasted?avatar={pfp}", delete_after=get_auto_delete_timeout())
        
    @commands.command()
    async def chat(self, ctx):
        await ctx.message.delete()
        subprocess.Popen('start AtomSB_Data\\Data\\AtomSb-Webchat.exe', shell=True)
        
    @commands.command()
    async def stopbump(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Stopping auto bump"+Fore.RESET)
        global bumpon
        bumpon = False
        
    @commands.command()
    async def uptime(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Getting uptime..."+Fore.RESET)
        from datetime import datetime
        import utils.helpers as helpers
        if helpers.start_time is None:
            await ctx.send("Uptime not available")
            return
        uptime = datetime.utcnow() - helpers.start_time
        uptime = str(uptime).split('.')[0]
        em = create_embed(title="Uptime")
        em.add_field(name='Uptime', value=f'{uptime}')
        await ctx.send(embed=em, delete_after=get_auto_delete_timeout())


def setup(bot):
    bot.add_cog(SelfBot(bot))
