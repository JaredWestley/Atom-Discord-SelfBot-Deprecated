import discord
from discord.ext import commands
import requests
from utils.helpers import EMBED_COLOUR, VERSION, create_embed
from utils.config import get_password, get_auto_delete_timeout
from colorama import Fore


class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def nickname(self, ctx, *, name: str = None):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Setting your nickname to - {Fore.CYAN}{name}"+Fore.RESET)
        if name is None:
            print(f"{Fore.RED} | please specifiy the name to change to"+Fore.RESET)
        elif len(name) < 1:
            print(f"{Fore.RED} | please specifiy the name to change to"+Fore.RESET)
        else:
            try:
                await ctx.author.edit(nick=name)
            except Exception as e:
                print(f"Error: {e}")
                
    @commands.command()
    async def steal(self, ctx, user: discord.Member):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to steal {Fore.CYAN}{user}'s {Fore.YELLOW} profile picture"+Fore.RESET)
        password = get_password()
        if password == 'password-here':
            print(f"{Fore.RED}[ERROR] {Fore.YELLOW}You didnt put your password in the config.json file"+Fore.RESET)
        else:
            import os
            os.makedirs('AtomSB_Data/Images/Avatars/Stolen', exist_ok=True)
            with open('AtomSB_Data/Images/Avatars/Stolen/Stolen.png', 'wb') as f:
                r = requests.get(user.avatar_url, stream=True)
                for block in r.iter_content(1024):
                    if not block:
                        break
                    f.write(block)
            try:
                with open('AtomSB_Data/Images/Avatars/Stolen/Stolen.png', 'rb') as f:
                    await self.bot.user.edit(password=password, avatar=f.read())
            except discord.HTTPException as e:
                print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{e}"+Fore.RESET)
                
    @commands.command()
    async def blankprofile(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Clean Slate"+Fore.RESET)
        password = get_password()
        if password == 'password-here':
            print(f"{Fore.RED}[ERROR] {Fore.YELLOW}You didnt put your password in the config.json file"+Fore.RESET)
        else:
            try:
                with open('AtomSB_Data/Images/Avatars/Transparent.png', 'rb') as f:
                    await self.bot.user.edit(password=password, username="᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼", avatar=f.read())
            except discord.HTTPException as e:
                print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{e}"+Fore.RESET)
                
    @commands.command()
    async def hypesquad(self, ctx, house):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Changing Hypesquad to - {Fore.CYAN}{house}"+Fore.RESET)
        request = requests.Session()
        headers = {
            'Authorization': get_password(),
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.305 Chrome/69.0.3497.128 Electron/4.0.8 Safari/537.36'
        }
        if house == "bravery":
            payload = {'house_id': 1}
        elif house == "brilliance":
            payload = {'house_id': 2}
        elif house == "balance":
            payload = {'house_id': 3}
        elif house == "random":
            import random
            houses = [1, 2, 3]
            payload = {'house_id': random.choice(houses)}
        try:
            request.post('https://discordapp.com/api/v6/hypesquad/online', headers=headers, json=payload, timeout=10)
        except Exception as e:
            print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{e}"+Fore.RESET)
            
    @commands.command()
    async def set(self, ctx, *, url):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to set your profile picture to - {Fore.CYAN}{url}"+Fore.RESET)
        password = get_password()
        if password == 'password-here':
            print(f"{Fore.RED}[ERROR] {Fore.YELLOW}You didnt put your Discord password in the config.json file"+Fore.RESET)
        else:
            import os
            os.makedirs('Images/Avatars', exist_ok=True)
            with open('Images/Avatars/PFP.png', 'wb') as f:
                r = requests.get(url, stream=True)
                for block in r.iter_content(1024):
                    if not block:
                        break
                    f.write(block)
            try:
                from PIL import Image
                Image.open('Images/Avatars/PFP-1.png').convert('RGB')
                with open('Images/Avatars/PFP-1.png', 'rb') as f:
                    await self.bot.user.edit(password=password, avatar=f.read())
            except discord.HTTPException as e:
                print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{e}"+Fore.RESET)
                
    @commands.command()
    async def junknickname(self, ctx):
        await ctx.message.delete()
        try:
            name = "𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫𒐫"
            await ctx.author.edit(nick=name)
            print(f"{Fore.YELLOW} | Nickname has been set to junk successfully"+Fore.RESET)
        except:
            pass
            
    @commands.command()
    async def invisablenickname(self, ctx):
        await ctx.message.delete()
        try:
            name = "᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼᲼"
            await ctx.author.edit(nick=name)
            print(f"{Fore.YELLOW}Nickname has been set to junk successfully"+Fore.RESET)
        except:
            pass


def setup(bot):
    bot.add_cog(Profile(bot))
