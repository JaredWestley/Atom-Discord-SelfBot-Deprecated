import discord
from discord.ext import commands
import requests
import asyncio
from utils.helpers import EMBED_COLOUR, VERSION, create_embed
from utils.config import get_auto_delete_timeout
from colorama import Fore


class Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def embedsay(self, ctx, *, message):
        print(f"{Fore.YELLOW} | Attempting to say {Fore.CYAN}{message}"+Fore.RESET)
        await ctx.message.delete()
        em = create_embed(title="Embedsay", description=message)
        timeout = get_auto_delete_timeout()
        await ctx.send(embed=em, delete_after=timeout)
        
    @commands.command()
    async def choose(self, ctx, *, choices: str):
        print(f"{Fore.YELLOW} | Attempting to choose between {Fore.CYAN}{choices}"+Fore.RESET)
        await ctx.message.delete()
        choices = choices.split(' ')
        if len(choices) < 2:
            return print('Not enough choices to pick from.')
        import random
        choice = str(random.choice(choices))
        em = create_embed(title="Choose")
        em.add_field(name='Choice :', value=f'{choice}')
        timeout = get_auto_delete_timeout()
        await ctx.send(embed=em, delete_after=timeout)
        
    @commands.command()
    async def space(self, ctx, *, msg):
        print(f"{Fore.YELLOW} | Placing a space between each letter of {Fore.CYAN}{msg}"+Fore.RESET)
        await ctx.message.delete()
        if msg.split(' ', 1)[0].isdigit():
            spaces = int(msg.split(' ', 1)[0]) * ' '
            msg = msg.split(' ', 1)[1].strip()
        else:
            spaces = ' '
        spaced_message = spaces.join(list(msg))
        await ctx.send(spaced_message)
        
    @commands.command()
    async def trump(self, ctx, *, message):
        await ctx.message.delete()
        msg = message.replace(" ", "%20")
        print(f"{Fore.YELLOW} | Wow trump tweeted that? - {Fore.CYAN}{message}"+Fore.RESET)
        await ctx.send(f"https://nekobot.xyz/api/imagegen?type=trumptweet&text={msg}&raw=1", delete_after=get_auto_delete_timeout())
        
    @commands.command()
    async def code(self, ctx, *, message):
        print(f"{Fore.YELLOW} | Sending {Fore.CYAN}{message} {Fore.YELLOW} in code format"+Fore.RESET)
        await ctx.message.delete()
        await ctx.send('`' + message + "`")
        
    @commands.command()
    async def reverse(self, ctx, *, message):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to reverse - {Fore.CYAN}{message}"+Fore.RESET)
        message = message[::-1]
        await ctx.send(message)
        
    @commands.command()
    async def unreverse(self, ctx, *, message):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to unreverse - {Fore.CYAN}{message}"+Fore.RESET)
        message = message[::-1]
        await ctx.send(message)
        
    @commands.command()
    async def shrug(self, ctx):
        await ctx.message.delete()
        await ctx.send(r'\ (•◡•) /')
        
    @commands.command()
    async def lenny(self, ctx):
        await ctx.message.delete()
        await ctx.send('( ͡°( ͡° ͜ʖ( ͡° ͜ʖ ͡°)ʖ ͡°) ͡°)')
        
    @commands.command()
    async def tableflip(self, ctx):
        await ctx.message.delete()
        await ctx.send('(ノಠ益ಠ)ノ彡┻━┻')
        
    @commands.command()
    async def uwu(self, ctx):
        await ctx.message.delete()
        await ctx.send('(ง ͠° ͟ل͜ ͡°)ง')
        
    @commands.command()
    async def bold(self, ctx, *, message):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to make - {Fore.CYAN}{message} {Fore.YELLOW} bold"+Fore.RESET)
        await ctx.send('**'+message+'**')
        
    @commands.command()
    async def secret(self, ctx, *, message):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Hiding your message - {Fore.CYAN}{message}"+Fore.RESET)
        await ctx.send('||'+message+'||')
        
    @commands.command()
    async def py(self, ctx, *, message):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to make - {Fore.CYAN}{message} {Fore.YELLOW} into py format"+Fore.RESET)
        await ctx.send('```py\n'+message+'\n```')
        
    @commands.command()
    async def cpp(self, ctx, *, message):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to make - {Fore.CYAN}{message} {Fore.YELLOW} into c++ format"+Fore.RESET)
        await ctx.send('```c++\n'+message+'\n```')
        
    @commands.command()
    async def junk(self, ctx):
        await ctx.message.delete()
        for each in range(0, 11):
            d = "\n"*100
            await ctx.send(f".{d}.")
            print(f"{Fore.YELLOW} | Junk text has been sent"+Fore.RESET)
            
    @commands.command()
    async def snipe(self, ctx):
        await ctx.message.delete()
        currentChannel = ctx.channel.id
        if currentChannel in self.bot.snipe_history_dict:
            try:
                await ctx.send(self.bot.snipe_history_dict[currentChannel])
            except:
                del self.bot.snipe_history_dict[currentChannel]
                
    @commands.command()
    async def editsnipe(self, ctx):
        await ctx.message.delete()
        currentChannel = ctx.channel.id
        if currentChannel in self.bot.sniped_edited_message_dict:
            print(f"{self.bot.sniped_edited_message_dict[currentChannel]}")
        else:
            await ctx.send("No message to snipe!", delete_after=3)
            
    @commands.command()
    async def cyclenick(self, ctx, *, text):
        await ctx.message.delete()
        global cycling
        cycling = True
        while cycling:
            name = ""
            for letter in text:
                name = name + letter
                await ctx.message.author.edit(nick=name)
                await asyncio.sleep(1)
                
    @commands.command()
    async def stopcyclenick(self, ctx):
        await ctx.message.delete()
        global cycling
        cycling = False
        
    @commands.command()
    async def massreact(self, ctx, emote, amount=5):
        print(f"{Fore.YELLOW} | Attempting to send - {Fore.CYAN}{emote} {amount} Times"+Fore.RESET)
        await ctx.message.delete()
        messages = await ctx.message.channel.history(limit=amount).flatten()
        for message in messages:
            await message.add_reaction(emote)
            
    @commands.command()
    async def advice(self, ctx):
        print(f"{Fore.YELLOW} | Getting some useful advice for you! :)"+Fore.RESET)
        await ctx.message.delete()
        r = requests.get('https://api.adviceslip.com/advice')
        em = create_embed(title="Advice!", description=r.json()['slip']['advice'])
        await ctx.send(embed=em, delete_after=get_auto_delete_timeout())
        
    @commands.command()
    async def clyde(self, ctx, *, text):
        await ctx.message.delete()
        msg = text.replace(" ", "%20")
        print(f"{Fore.YELLOW} | Creating an image as - {Fore.CYAN}Clyde"+Fore.RESET)
        await ctx.send(f"https://nekobot.xyz/api/imagegen?type=clyde&text={msg}&raw=1", delete_after=get_auto_delete_timeout())
        
    @commands.command()
    async def changemymind(self, ctx, *, message):
        await ctx.message.delete()
        msg = message.replace(" ", "%20")
        print(f"{Fore.YELLOW} | Changing your mind with - {Fore.CYAN}{message}"+Fore.RESET)
        await ctx.send(f"https://nekobot.xyz/api/imagegen?type=changemymind&text={msg}&raw=1", delete_after=get_auto_delete_timeout())
        
    @commands.command()
    async def chatbot(self, ctx, *, msg):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Asking AtomSB Chat Bot - {Fore.CYAN}{msg}"+Fore.RESET)
        r = requests.get(f"https://some-random-api.ml/chatbot?message={msg}")
        res = r.json()
        em = create_embed(title="AtomSB")
        em.add_field(name='AtomSB Chat Bot', value=f'{res["response"]}', inline=False)
        await ctx.send(embed=em, delete_after=get_auto_delete_timeout())
        
    @commands.command()
    async def sendall(self, ctx, *, message):
        await ctx.message.delete()
        try:
            channels = ctx.guild.text_channels
            print(f"{Fore.YELLOW} | Sending a message in every channel of - {Fore.YELLOW}{ctx.guild.name}"+Fore.RESET)
            for channel in channels:
                await channel.send(message)
        except:
            pass
            
    @commands.command(aliases=["del", "quickdel"])
    async def quickdelete(self, ctx, *, args):
        print(f"{Fore.YELLOW} | Sending {args} and quickly deleting it"+Fore.RESET)
        await ctx.message.delete()
        await ctx.send(args, delete_after=1)
        
    @commands.command()
    async def credits(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | AtomSB credits "+Fore.RESET)
        em = create_embed(title="Credits")
        em.add_field(name='Developer', value="Atomoyo", inline=False)
        em.add_field(name='Ideas', value="Jappie, Dxjq, Retard, Ultralight04, Mineplay", inline=False)
        em.add_field(name='Designer', value="Mineplay", inline=False)
        em.add_field(name='Beta Testers', value="Thanks to all of them for testing!", inline=False)
        await ctx.send(embed=em, delete_after=get_auto_delete_timeout())
        
    @commands.command()
    async def masspin(self, ctx, amount=5):
        print(f"{Fore.YELLOW} | Attempting to pin messages - {Fore.CYAN}{amount} Times"+Fore.RESET)
        await ctx.message.delete()
        messages = await ctx.message.channel.history(limit=amount).flatten()
        for message in messages:
            await message.pin()
            await asyncio.sleep(2.5)
            
    @commands.command()
    async def lyrics(self, ctx, artist, *, song):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Searching for - {Fore.CYAN} {song} by {artist}!"+Fore.RESET)
        r = requests.get(f"https://api.lyrics.ovh/v1/{artist}/{song}")
        res = r.json()
        lyric = res['lyrics']
        em = create_embed(title="Lyrics")
        em.add_field(name='Lyrics', value=f"{lyric}", inline=True)
        await ctx.send(embed=em, delete_after=get_auto_delete_timeout())
        
    @commands.command()
    async def giphy(self, ctx, search):
        await ctx.message.delete()
        import urllib.request
        import json
        api_key = "add-your-own-api-key"
        request1 = urllib.request.Request(f"https://api.giphy.com/v1/gifs/search?api_key={api_key}&q={search}&limit=5&offset=0&rating=r&lang=en")
        opener = urllib.request.build_opener()
        response = opener.open(request1)
        obj = json.loads(response.read())
        gif = obj['data'][0]['images']['original']['url']
        titlegif = obj['data'][0]['title']
        rating = obj['data'][0]['rating']
        shorturl = obj['data'][0]['bitly_gif_url']
        creationdate = obj['data'][0]['import_datetime']
        embed = create_embed(title=f'Gif Lookup')
        embed.set_image(url=gif)
        embed.add_field(name="Search Term", value=search, inline=True)
        embed.add_field(name="Rating", value=rating, inline=True)
        embed.add_field(name="Url", value=shorturl, inline=False)
        embed.add_field(name="Upload Date", value=creationdate, inline=False)
        await ctx.send(embed=embed, delete_after=get_auto_delete_timeout())
        print(f'{Fore.YELLOW}Used Giphy to search for - {Fore.CYAN}{search}'+Fore.RESET)
        
    @commands.command()
    async def ranstory(self, ctx):
        await ctx.message.delete()
        when = ['A few years ago', 'Yesterday', 'Last night', 'A long time ago','On 20th Jan']
        who = ['a rabbit', 'an elephant', 'a mouse', 'a turtle','a cat']
        name = ['Ali', 'Miriam','daniel', 'Hoouk', 'Starwalker']
        residence = ['Barcelona','India', 'Germany', 'Venice', 'England']
        went = ['cinema', 'university','seminar', 'school', 'laundry']
        happened = ['made a lot of friends','Eats a burger', 'found a secret key', 'solved a mistery', 'wrote a book']
        ranwhen = random.choice(when)
        ranwho = random.choice(who)
        ranresidence = random.choice(residence)
        ranwent = random.choice(went)
        ranhappened = random.choice(happened)
        await ctx.send(f"{ranwhen}, {ranwho} that lived in {ranresidence} went to the {ranwent} and {ranhappened}")
        
    @commands.command()
    async def count(self, ctx, num):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Counting to - {Fore.CYAN}{num}"+Fore.RESET)
        count = 1
        numb = int(num)
        global counton
        counton = True
        while counton:
            for cont in num:
                if count <= numb:
                    await ctx.send(count)
                    count += 1
                    await asyncio.sleep(1)
                else:
                    return
                    
    @commands.command()
    async def stopcount(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Stopping Count"+Fore.RESET)
        global counton
        counton = False


def setup(bot):
    bot.add_cog(Chat(bot))
