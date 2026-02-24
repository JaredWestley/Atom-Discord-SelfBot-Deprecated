import discord
from discord.ext import commands
import requests
import aiohttp
import io
import functools
from utils.helpers import EMBED_COLOUR, VERSION, create_embed, encode_string, decode_string
from utils.config import get_auto_delete_timeout, get_token
from colorama import Fore


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def weather(self, ctx, *, city):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Checking the weather outside of {Fore.CYAN}{city} {Fore.YELLOW}really quick"+Fore.RESET)
        weather_key = 'add-your-own-api-key'
        if weather_key == '':
            print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}Weather API key has not been set in the config.json file"+Fore.RESET)
        else:
            try:
                req = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_key}')
                r = req.json()
                temperature = round(float(r["main"]["temp"]) - 273.15, 1)
                weather1 = r["weather"][0]["main"]
                pressure = r["main"]["pressure"]
                visibility = r["visibility"]
                humidity = round(float(r["main"]["humidity"]), 1)
                wind_speed = round(float(r["wind"]["speed"]), 1)
                em = create_embed(title=f"Weather - {city}", description=f'''
                Temperature: {temperature}
                Weather: {weather1}
                Pressure: {pressure}
                Visibility: {visibility}
                Wind Speed: {wind_speed}
                ''')
                em.add_field(name='City', value=city.capitalize())
                timeout = get_auto_delete_timeout()
                try:
                    await ctx.send(embed=em, delete_after=timeout)
                except:
                    await ctx.send(f'''
                    Temperature: {temperature}
                    Weather: {weather1}
                    Pressure: {pressure}
                    Visibility: {visibility}
                    Wind Speed: {wind_speed}
                    ''', delete_after=timeout)
            except KeyError:
                print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{city} Is not a real city"+Fore.RESET)
                
    @commands.command()
    async def encode(self, ctx, *, string):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Encoding - {Fore.CYAN}{string}"+Fore.RESET)
        encoded = encode_string(string)
        await ctx.send(encoded)
        
    @commands.command()
    async def decode(self, ctx, *, string):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Decoding - {Fore.CYAN}{string}"+Fore.RESET)
        decoded = decode_string(string)
        await ctx.send(decoded)
        
    @commands.command()
    async def dm(self, ctx, user: discord.Member, *, message):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to DM {Fore.CYAN}{user} {Fore.YELLOW}- {Fore.CYAN}{message}"+Fore.RESET)
        user = self.bot.get_user(user.id)
        try:
            await user.send(message)
        except:
            pass
            
    @commands.command()
    async def shrink(self, ctx, *, link):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to shorten - {Fore.CYAN}{link}"+Fore.RESET)
        r = requests.get(f'http://tinyurl.com/api-create.php?url={link}').text
        em = create_embed(title='TinyURL', description=f'Shortened link: {r}')
        await ctx.send(embed=em)
        
    @commands.command()
    async def tts(self, ctx, *, message):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attmepting to make a TTS - {Fore.CYAN}{message}"+Fore.RESET)
        from gtts import gTTS
        import asyncio
        
        loop = asyncio.get_event_loop()
        
        def do_tts():
            f = io.BytesIO()
            tts = gTTS(text=message.lower(), lang='en')
            tts.write_to_fp(f)
            f.seek(0)
            return f
        
        buff = await loop.run_in_executor(None, do_tts)
        await ctx.send(file=discord.File(buff, f"{message}.wav"))
        
    @commands.command()
    async def bump(self, ctx, channelid):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to Auto bump the server in - {Fore.CYAN}{channelid}"+Fore.RESET)
        
    @commands.command()
    async def backupfriends(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Backing up friends list"+Fore.RESET)
        import os
        os.makedirs('AtomSB_Data/Saved', exist_ok=True)
        
        saved_friends = 0
        headers = {'authorization': get_token()}
        connect = requests.get('https://canary.discordapp.com/api/v6/users/@me', headers=headers)
        friends = requests.get('https://discord.com/api/v6/users/@me/relationships', headers=headers)
        for friend in friends.json():
            if friend['type'] == 1:
                username = f'Name - {Fore.CYAN}%s#%s | User ID - {Fore.CYAN}%s\n' % (friend['user']['username'], friend['user']['discriminator'], friend['id'])
                print(username)
                with open('AtomSB_Data/Saved/Friends.txt', 'a', encoding='UTF-8') as f:
                    f.write(username)
                saved_friends += 1
                
        with open('AtomSB_Data/Saved/Friends.txt', 'r', encoding='UTF-8') as f:
            fixed = f.read()[:-1]
        with open('AtomSB_Data/Saved/Friends.txt', 'w', encoding='UTF-8') as f:
            f.write(fixed)


def setup(bot):
    bot.add_cog(Utility(bot))
