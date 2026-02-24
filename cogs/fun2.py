import discord
from discord.ext import commands
import requests
import random
import asyncio
import os
import re
import io
from utils.helpers import EMBED_COLOUR, VERSION, create_embed
from utils.config import get_auto_delete_timeout
from colorama import Fore


class Fun2(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def selfdestruct(self, ctx, *, amount):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Self destructing your last message in {Fore.CYAN}{amount}"+Fore.RESET)
        async for message in ctx.message.channel.history():
            if message.id == ctx.message.id:
                continue
            if message.author == ctx.message.author:
                killmsg = message
                break
        if not killmsg:
            return print('There is no message to destroy.')
        timer = int(amount.strip())
        timer -= 1
        await ctx.message.edit(content=' :bomb:' + "-"*int(timer)+":fire:")
        await asyncio.sleep(1)
        msg = ctx.message
        while timer:
            timer -= 1
            await msg.edit(content=' :bomb:' + "-"*int(timer)+":fire:")
            await asyncio.sleep(1)
        await msg.edit(content=' :boom:')
        await asyncio.sleep(.5)
        await killmsg.edit(content=' :fire:')
        await asyncio.sleep(.5)
        await killmsg.delete()
        await msg.delete()
        
    @commands.command()
    async def dick(self, ctx, *, user: discord.Member = None):
        await ctx.message.delete()
        if user is None:
            user = ctx.author
        print(f"{Fore.YELLOW} | Geussing {Fore.CYAN}{user}'s {Fore.YELLOW}dicksize"+Fore.RESET)
        size = random.randint(1, 15)
        dong = ""
        for _i in range(0, size):
            dong += "="
        em = create_embed(title=f"{user.name}'s Dick size", description=f"8{dong}D")
        timeout = get_auto_delete_timeout()
        await ctx.send(embed=em, delete_after=timeout)
        
    @commands.command()
    async def gay(self, ctx, *, user: discord.Member = None):
        await ctx.message.delete()
        if user is None:
            user = ctx.author
        print(f"{Fore.YELLOW} | Guessing {Fore.CYAN}{user}'s {Fore.YELLOW}gayness"+Fore.RESET)
        level = random.randint(1, 100)
        em = create_embed(title=f"Gay Calculator - {user.name}", description=f"I have calculated that {user.name} is {level}% Gay")
        timeout = get_auto_delete_timeout()
        await ctx.send(embed=em, delete_after=timeout)
        
    @commands.command()
    async def spam(self, ctx, amount, delay: int=None, *, message):
        await ctx.message.delete()
        if amount is None or message is None:
            print(f"{Fore.YELLOW} | Invalid input! Please refer to help command to learn proper usage")
        else:
            print(f"{Fore.YELLOW} | Attempting to spam - {Fore.CYAN} {message} {amount} times with a delay of {delay}"+Fore.RESET)
        global spamon
        spamon = True
        count = 1
        amnt = int(amount)
        while spamon:
            for cont in amount:
                if count <= amnt:
                    await ctx.send(message)
                    count += 1
                    await asyncio.sleep(delay)
                else:
                    return
                    
    @commands.command()
    async def stopspam(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Stopping Spam"+Fore.RESET)
        global spamon
        spamon = False
        
    @commands.command()
    async def modem(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Well you asked for it!"+Fore.RESET)
        try:
            import playsound
            playsound.playsound('AtomSB_Data/Music/Dont_touch/Modem.mp3', True)
        except:
            print("playsound not available")
        
    @commands.command()
    async def music(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Playing your mixtape (You won't be able to use the SB until the song is done)"+Fore.RESET)
        try:
            import playsound
            playsound.playsound('AtomSB_Data/Music/song.mp3', True)
        except:
            print("playsound not available")
            
    @commands.command()
    async def sendmusic(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Sharing your mixtape (This may take a while, it depeneds on your internet speed)"+Fore.RESET)
        try:
            with open("AtomSB_Data/Music/song.mp3", "rb") as file:
                await ctx.send("Your Mixtape ", file=discord.File(file))
        except:
            print("Music file not found")
            
    @commands.command()
    async def copyuser(self, ctx, user: discord.User):
        await ctx.message.delete()
        self.bot.copyuser = user
        user = str(self.bot.copyuser)
        print(f"{Fore.YELLOW} | Now copying {Fore.CYAN}{user}"+Fore.RESET)
        
    @commands.command()
    async def stopcopy(self, ctx):
        await ctx.message.delete()
        if self.bot.user is None:
            await ctx.send(f"{Fore.YELLOW} | You weren't copying anyone to begin with")
            return
        user=str(self.bot.copyuser)
        print(f"{Fore.YELLOW} | Stopped copying {Fore.CYAN}{user}"+Fore.RESET)
        self.bot.copyuser = None
        
    @commands.command()
    async def triggered(self, ctx, *, user: discord.Member):
        await ctx.message.delete()
        pfp=user.avatar_url
        print(f"{Fore.YELLOW} | Triggering - {Fore.CYAN}{user.name}"+Fore.RESET)
        await ctx.send(f"https://some-random-api.ml/canvas/triggered?avatar={pfp}")
        
    @commands.command()
    async def kanyeq(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Kanye quote "+Fore.RESET)
        r = requests.get(f"https://api.kanye.rest/")
        res = r.json()
        kanyemsg = res['quote']
        await ctx.send(f"*{kanyemsg} - Kanye*")
        
    @commands.command()
    async def geekj(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Geek Joke "+Fore.RESET)
        r = requests.get(f"https://geek-jokes.sameerkumar.website/api")
        res = r.json()
        await ctx.send(f"{res}")
        
    @commands.command()
    async def insult(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Insult "+Fore.RESET)
        r = requests.get(f"https://evilinsult.com/generate_insult.php?lang=en&type=json")
        res = r.json()
        insultt = res['insult']
        await ctx.send(f"{insultt}")
        
    @commands.command()
    async def randomfact(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Random Fact"+Fore.RESET)
        r = requests.get(f"https://uselessfacts.jsph.pl/random.json")
        res = r.json()
        fact = res['text']
        await ctx.send(f"{fact}")
        
    @commands.command()
    async def bored(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Finding something to do!"+Fore.RESET)
        r = requests.get(f"http://www.boredapi.com/api/activity/")
        res = r.json()
        act = res['activity']
        type = res['type']
        participants = res['participants']
        em = create_embed(title="Bored")
        em.add_field(name='Type', value=f"{type}", inline=False)
        em.add_field(name='Activity', value=f"{act}", inline=False)
        em.add_field(name='Participants', value=f"{participants}", inline=False)
        timeout = get_auto_delete_timeout()
        await ctx.send(embed=em, delete_after=timeout)
        
    @commands.command()
    async def ageguess(self, ctx, name):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Age Guesser - {Fore.CYAN}{name}"+Fore.RESET)
        r = requests.get(f"https://api.agify.io/?name={name}")
        res = r.json()
        kanyemsg = res['age']
        em = create_embed(title=f'Age Guesser')
        em.add_field(name='Name', value=f"{name}", inline=False)
        em.add_field(name='Age', value=f"{kanyemsg}", inline=False)
        timeout = get_auto_delete_timeout()
        await ctx.send(embed=em, delete_after=timeout)
        
    @commands.command()
    async def iss(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Locating the ISS! "+Fore.RESET)
        import urllib.request
        import json
        request1 = urllib.request.Request("http://api.open-notify.org/iss-now.json")
        opener = urllib.request.build_opener()
        response = opener.open(request1)
        obj = json.loads(response.read())
        timestamp = obj['timestamp']
        pos_long = obj['iss_position']['longitude']
        pos_lat = obj['iss_position']['latitude']
        em = create_embed(title='ISS Location')
        em.add_field(name='Timestamp', value=f"{timestamp}", inline=False)
        em.add_field(name='Latitude', value=f"{pos_lat}", inline=False)
        em.add_field(name='Longitude', value=f"{pos_long}", inline=False)
        timeout = get_auto_delete_timeout()
        await ctx.send(embed=em, delete_after=timeout)
        
    @commands.command()
    async def cyberpunk(self, ctx, console = None):
        print(f"{Fore.YELLOW} | Cyberpunk Bugs "+Fore.RESET)
        await ctx.message.delete()
        if console is None:
            print(f"{Fore.YELLOW} | The options are - {Fore.CYAN}ps4, xbox, wii, pc"+Fore.RESET)
            return
        elif console == "ps4":
            message = "**THIS IS CYBERPUNK ON PS4** \n https://www.youtube.com/watch?v=VhvDy8h3FG8"
        elif console == "xbox":
            message = "**THIS IS CYBERPUNK ON XBOX** \n https://www.youtube.com/watch?v=2uID5aponCg"
        elif console == "wii":
            message = "**THIS IS CYBERPUNK ON WII** \n https://www.youtube.com/watch?v=VACQgTN6skE"
        elif console == "pc":
            message = "**THIS IS CYBERPUNK ON PC** \n https://www.youtube.com/watch?v=SazapfUt4ig"
        else:
            return
        await ctx.send(message)
        
    @commands.command()
    async def copyname(self, ctx, user: discord.Member = None):
        await ctx.message.delete()
        if user is None:
            print("Please select a user to continue!")
            return
        username = str(f"{user.name}")
        from utils.config import get_password
        password = get_password()
        try:
            await self.bot.user.edit(password=password, username=f"{username}")
        except KeyError:
            print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}There has been an error changing your name to {username}"+Fore.RESET)
            
    @commands.command()
    async def ricky(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to set your profile picture to Ricky"+Fore.RESET)
        from utils.config import get_password
        password = get_password()
        if password == 'password-here':
            print(f"{Fore.RED}[ERROR] {Fore.YELLOW}You didnt put your Discord password in the config.json file"+Fore.RESET)
        else:
            try:
                from PIL import Image
                Image.open('AtomSB_Data/Images/Avatars/Ricky.png').convert('RGB')
                with open('AtomSB_Data/Images/Avatars/Ricky.png', 'rb') as f:
                    await self.bot.user.edit(password=password, avatar=f.read())
                await self.bot.user.edit(password=password, username="Ricky")
            except discord.HTTPException as e:
                print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{e}"+Fore.RESET)
                
    @commands.command()
    async def rikka(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to set your profile picture to Rikka"+Fore.RESET)
        from utils.config import get_password
        password = get_password()
        if password == 'password-here':
            print(f"{Fore.RED}[ERROR] {Fore.YELLOW}You didnt put your Discord password in the config.json file"+Fore.RESET)
        else:
            try:
                from PIL import Image
                Image.open('AtomSB_Data/Images/Avatars/Rikka.png').convert('RGB')
                with open('AtomSB_Data/Images/Avatars/Rikka.png', 'rb') as f:
                    await self.bot.user.edit(password=password, avatar=f.read())
                await self.bot.user.edit(password=password, username="Rikka")
            except discord.HTTPException as e:
                print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{e}"+Fore.RESET)
                
    @commands.command()
    async def yes(self, ctx):
        await ctx.message.delete()
        await ctx.send('no')
        
    @commands.command()
    async def no(self, ctx):
        await ctx.message.delete()
        await ctx.send('yes')
        
    @commands.command()
    async def yesno(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | YesNo"+Fore.RESET)
        r = requests.get(f"https://yesno.wtf/api")
        res = r.json()
        act = res['answer']
        imag = res['image']
        em = create_embed(title='YesNo')
        em.add_field(name='Yes-No', value=f"{act}", inline=False)
        em.set_thumbnail(url=f"{imag}")
        timeout = get_auto_delete_timeout()
        await ctx.send(embed=em, delete_after=timeout)
        
    @commands.command()
    async def dice(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Rolling a dice"+Fore.RESET)
        roll_num = "123456"
        random_ans = random.choice(roll_num)
        random_ans = "".join(random_ans)
        em = create_embed(title="Dice")
        em.add_field(name='Roll', value=f"{random_ans}", inline=False)
        timeout = get_auto_delete_timeout()
        await ctx.send(embed=em, delete_after=timeout)
        
    @commands.command()
    async def flip(self, ctx, *, string):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Fliping - {Fore.CYAN}{string}"+Fore.RESET)
        conversion_code = {
            'A': 'ɐ', 'B': 'q', 'C': 'ɔ', 'D': 'p', 'E': 'ǝ', 'F': 'ɟ', 
            'G': 'ƃ', 'H': 'ɥ', 'I': 'ı', 'J': 'ɾ', 'K': 'ʞ', 'L': '˥', 
            'M': 'ɯ', 'N': 'u', 'O': 'o', 'P': 'd', 'Q': 'b', 'R': 'ɹ', 
            'S': 's', 'T': 'ʇ', 'U': 'n', 'V': 'ʌ', 'W': 'ʍ', 'X': 'x', 
            'Y': 'ʎ', 'Z': 'A',
            'a': 'ɐ', 'b': 'q', 'c': 'ɔ', 'd': 'p', 'e': 'ǝ', 'f': 'ɟ', 
            'g': 'ƃ', 'h': 'ɥ', 'i': 'ı', 'j': 'ɾ', 'k': 'ʞ', 'l': '˥', 
            'm': 'ɯ', 'n': 'u', 'o': 'o', 'p': 'd', 'q': 'b', 'r': 'ɹ', 
            's': 's', 't': 'ʇ', 'u': 'n', 'v': 'ʌ', 'w': 'ʍ', 'x': 'x', 
            'y': 'ʎ', 'z': 'z'
        }
        converted_data = ""
        for i in range(0, len(string)):
            if string[i] in conversion_code.keys():
                converted_data += conversion_code[string[i]]
            else:
                converted_data += string[i]
        await ctx.send(converted_data)
        
    @commands.command()
    async def shrekmov(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | The Shrek Movie "+Fore.RESET)
        await ctx.send("https://cdn.discordapp.com/attachments/654804796364292106/662279189923233792/Shrek_VP9-60k_Opus-20300-1.webm")
        
    @commands.command()
    async def lefishe(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | LeFish"+Fore.RESET)
        await ctx.send("https://cdn.discordapp.com/attachments/743911477773336577/789498023432552498/SPOILER_Hot_chick_in_water.mp4")
        
    @commands.command()
    async def fakeperson(self, ctx):
        print(f"{Fore.YELLOW} | Generating a fake person "+Fore.RESET)
        await ctx.message.delete()
        import urllib.request
        import json
        request1 = urllib.request.Request("https://pipl.ir/v1/getPerson")
        opener = urllib.request.build_opener()
        response = opener.open(request1)
        obj = json.loads(response.read())
        education = obj['person']
        em = create_embed(title=f'Fake Person Gen')
        em.add_field(name='Education', value=f"{education}", inline=False)
        timeout = get_auto_delete_timeout()
        await ctx.send(embed=em, delete_after=timeout)
        
    @commands.command()
    async def scrapper(self, ctx, linkc, optionc):
        await ctx.message.delete()
        
        class ImageSpider:
            def __init__(self):
                self.home = os.getcwd()
        
            def grab_all_image_links(self, URL):
                try:
                    valid_links = []
                    url_protocol = URL.split('/')[0]
                    url_html = requests.get(URL).text
                    Image_urls = re.findall(r'((http\:|https\:)?\//[^"\' ]*?\.(png|jpg))', url_html, flags=re.IGNORECASE | re.MULTILINE | re.UNICODE)
                    for image in Image_urls:
                        image_url = image[0]
                        if not image_url.startswith(url_protocol):
                            image_url = url_protocol+image_url
                            valid_links.append(image_url)
                        else:
                            valid_links.append(image_url)
                except Exception as graberror:
                    print(f'{Fore.YELLOW} | Grab occured while getting links')
                    print(graberror)
                    return []  
                return valid_links

            @staticmethod
            def extract_image_name(url):
                image_name = str(url).split('/')[-1]
                return image_name

            @staticmethod
            def extract_site_name(url):
                sitename = str(url).split('/')[2]
                return sitename
        
            def saving_images(self, url):
                Image_links = self.grab_all_image_links(url)
                for link in Image_links:
                    raw_image = requests.get(link, stream=True).raw
                    from PIL import Image
                    img = Image.open(raw_image)
                    image_name = self.extract_image_name(link)
                    img.save(image_name)
        
            def grab_all_links(self, url):
                links = [url]
                link_html = requests.get(url).text
                from bs4 import BeautifulSoup as bs4
                all_links = bs4(link_html, 'html.parser').findAll('a')
                for link in all_links:
                    href = link.get('href')
                    if href:       
                        if href.startswith('http') or href.startswith('https'):
                            links.append(href)
                return links

            def download_images(self):
                url = linkc
                try:
                    sitename = self.extract_site_name(url)
                    print("Extracting images from {} ...".format(sitename))
                    os.chdir("AtomSB_Data/Scrapper")
                    os.mkdir(sitename);os.chdir(sitename)
                    option = optionc
                    if option == 1:
                        all_avaialble_links = set(self.grab_all_links(url))
                    else:
                        all_avaialble_links = [url]
                    for link in all_avaialble_links:
                        try:                        
                            print(link)
                            self.saving_images(link)
                        except:
                            continue

                except Exception as Error:
                    print(f'{Fore.RED} | Error occured while grabing site links')
                    print(Error)

                finally:
                    print(f'{Fore.GREEN} | Finished scrapping')
                    os.chdir(self.home)

        spider = ImageSpider()
        spider.download_images()


def setup(bot):
    bot.add_cog(Fun2(bot))
