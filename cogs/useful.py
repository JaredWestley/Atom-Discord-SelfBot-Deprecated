import discord
from discord.ext import commands
import requests
import datetime
import subprocess
import sys
import os
import webbrowser
from utils.helpers import EMBED_COLOUR, VERSION, create_embed
from utils.config import get_auto_delete_timeout, get_token
from colorama import Fore


class Useful(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def serverinfo(self, ctx, server_id: int = None):
        await ctx.message.delete()
        server = self.bot.get_guild(id=server_id) or ctx.guild
        total_users = len(server.members)
        online = len([m for m in server.members if m.status != discord.Status.offline])
        text_channels = len([x for x in server.channels if isinstance(x, discord.TextChannel)])
        voice_channels = len([x for x in server.channels if isinstance(x, discord.VoiceChannel)])
        categories = len(server.channels) - text_channels - voice_channels
        passed = (ctx.message.created_at - server.created_at).days
        created_at = "Created {}. ".format(server.created_at.strftime("%d %b %Y %H:%M"), passed)
        print(f"{Fore.YELLOW} | Getting information on {Fore.CYAN}{server.name}"+Fore.RESET)
        em = create_embed(title='AtomSB ServerInfo', description=created_at)
        em.add_field(name="Region", value=str(server.region))
        em.add_field(name="Text Channels", value=text_channels)
        em.add_field(name="Voice Channels", value=voice_channels)
        em.add_field(name="Roles", value=len(server.roles))
        em.add_field(name="Categories", value=categories)
        em.set_author(name=server.name, icon_url=None or server.icon_url)
        em.set_thumbnail(url=None or server.icon_url)
        await ctx.send(embed=em, delete_after=get_auto_delete_timeout())
        
    @commands.command()
    async def aboutbot(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Getting information about AtomSB"+Fore.RESET)
        em = create_embed(title='Atom SB')
        em.url = 'https://selfbot-py.tk'
        
        total_members = sum(1 for _ in self.bot.get_all_members())
        total_online = len({m.id for m in self.bot.get_all_members() if m.status is discord.Status.online})
        total_unique = len(self.bot.users)
        
        voice_channels = []
        text_channels = []
        for guild in self.bot.guilds:
            voice_channels.extend(guild.voice_channels)
            text_channels.extend(guild.text_channels)
        
        text = len(text_channels)
        voice = len(voice_channels)
        dm = len(self.bot.private_channels)
        
        em.add_field(name='Guilds', value=len(self.bot.guilds))
        em.add_field(name='Members', value=f'{total_unique} total')
        em.add_field(name='Channels', value=f'{text} text\n{voice} voice\n{dm} direct')
        
        try:
            import psutil
            svmem = psutil.virtual_memory()
            memory_usage = svmem.percent
            cpu_usage = psutil.cpu_percent()
            em.add_field(name='Process', value=f'{memory_usage:.2f} MiB\n{cpu_usage:.2f}% CPU')
        except:
            pass
            
        await ctx.send(embed=em, delete_after=get_auto_delete_timeout())
        
    @commands.command()
    async def time(self, ctx):
        await ctx.message.delete()
        dandt = datetime.datetime.now()
        date_time = dandt.strftime("%H:%M:%S")
        print(f"{Fore.YELLOW} | The current time is {Fore.CYAN}{date_time}"+Fore.RESET)
        em = create_embed(title="Time")
        em.add_field(name='Current Time', value=f'{date_time}')
        await ctx.send(embed=em, delete_after=get_auto_delete_timeout())
        
    @commands.command()
    async def date(self, ctx):
        await ctx.message.delete()
        dandt = datetime.datetime.now()
        date_time = dandt.strftime("%d/%m/%Y")
        print(f"{Fore.YELLOW} | The current date is {Fore.CYAN}{date_time}"+Fore.RESET)
        em = create_embed(title="Date")
        em.add_field(name='Current Date', value=f'{date_time}')
        await ctx.send(embed=em, delete_after=get_auto_delete_timeout())
        
    @commands.command()
    async def banner(self, ctx):
        await ctx.message.delete()
        em = create_embed(title=ctx.guild.name)
        em.set_image(url=ctx.guild.banner_url)
        await ctx.send(embed=em, delete_after=get_auto_delete_timeout())
        
    @commands.command()
    async def search(self, ctx, *, link):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Searching the web for - {Fore.CYAN}{link}"+Fore.RESET)
        webbrowser.open_new_tab(link)
        
    @commands.command()
    async def google(self, ctx, *, search):
        await ctx.message.delete()
        url = f"https://www.google.com.tr/search?q={search}"
        webbrowser.open_new_tab(url)
        
    @commands.command()
    async def yt(self, ctx, *, ytkey):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to Look up {Fore.CYAN}{ytkey}{Fore.YELLOW} on Youtube"+Fore.RESET)
        msg = ytkey.replace(" ", "+")
        url = f"https://www.youtube.com/results?search_query={msg}"
        webbrowser.open_new_tab(url)
        
    @commands.command()
    async def covid(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Collecting the sad truth! :( "+Fore.RESET)
        r = requests.get(f"https://corona.lmao.ninja/v3/covid-19/all")
        res = r.json()
        em = create_embed(title="Covid-19 Stats")
        em.add_field(name='Recent Cases', value=f'{res["todayCases"]}', inline=False)
        em.add_field(name='Total Cases', value=f'{res["cases"]}', inline=False)
        em.add_field(name='Recent Recoveries', value=f'{res["todayRecovered"]}', inline=False)
        em.add_field(name='Total Recoveries', value=f'{res["recovered"]}', inline=False)
        em.add_field(name='Recent Deaths', value=f'{res["todayDeaths"]}', inline=False)
        em.add_field(name='Total Deaths', value=f'{res["deaths"]}', inline=False)
        await ctx.send(embed=em, delete_after=get_auto_delete_timeout())
        
    @commands.command()
    async def adminservers(self, ctx):
        print(f"{Fore.YELLOW} | Getting servers you have permissions in"+Fore.RESET)
        await ctx.message.delete()
        admins = []
        bots = []
        kicks = []
        bans = []
        for guild in self.bot.guilds:
            if guild.me.guild_permissions.administrator:
                admins.append(discord.utils.escape_markdown(guild.name))
            if guild.me.guild_permissions.manage_guild and not guild.me.guild_permissions.administrator:
                bots.append(discord.utils.escape_markdown(guild.name))
            if guild.me.guild_permissions.ban_members and not guild.me.guild_permissions.administrator:
                bans.append(discord.utils.escape_markdown(guild.name))
            if guild.me.guild_permissions.kick_members and not guild.me.guild_permissions.administrator:
                kicks.append(discord.utils.escape_markdown(guild.name))
        em = create_embed(title="Server Permissions")
        em.add_field(name=f'Servers with Admin ({len(admins)})', value=f"{admins}", inline=False)
        em.add_field(name=f'Servers with BOT_ADD Permission ({len(bots)})', value=f'{bots}', inline=False)
        em.add_field(name=f'Servers with Ban Permission ({len(bans)})', value=f'{bans}', inline=False)
        em.add_field(name=f'Servers with Kick Permission ({len(kicks)})', value=f'{kicks}', inline=False)
        await ctx.send(embed=em, delete_after=get_auto_delete_timeout())
        
    @commands.command()
    async def screenshot(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Taking a screenshot "+Fore.RESET)
        try:
            from mss import mss
            with mss() as sct:
                sct.shot()
            file = discord.File("monitor-1.png", filename="monitor-1.png")
            await ctx.send(file=file)
        except Exception as e:
            print(f"Error: {e}")
            
    @commands.command()
    async def volumemax(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Volumemax "+Fore.RESET)
        try:
            import win32api
            import win32con
            for i in range(200):
                win32api.keybd_event(win32con.VK_VOLUME_UP, 0)
        except:
            print("win32api not available")
            
    @commands.command()
    async def volumemin(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Volumemin "+Fore.RESET)
        try:
            import win32api
            import win32con
            for i in range(200):
                win32api.keybd_event(win32con.VK_VOLUME_DOWN, 0)
        except:
            print("win32api not available")
            
    @commands.command()
    async def nickscan(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Scanning servers for nicknames "+Fore.RESET)
        message = ''
        for guild in self.bot.guilds:
            if guild.me.nick != None:
                message += f'{guild.name} - {guild.me.nick}\n'
        em = create_embed(title=f'Servers Nicknames', description=message)
        await ctx.send(embed=em, delete_after=get_auto_delete_timeout())
        
    @commands.command()
    async def bans(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | List of banned users in the guild "+Fore.RESET)
        try:
            bans = await ctx.guild.bans()
        except:
            return await ctx.send('You dont have the perms to see bans.')
        em = create_embed(title=f'List of Banned Members - {len(bans)}')
        em.description = ', '.join([str(b.user) for b in bans])
        await ctx.send(embed=em, delete_after=get_auto_delete_timeout())
        
    @commands.command()
    async def bottoken(self, ctx):
        await ctx.message.delete()
        import random
        p1 = 22
        p2 = 6
        p3 = 27
        possible_characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890-_"
        random_character_list1 = [random.choice(possible_characters) for i in range(p1)]
        random_character_list2 = [random.choice(possible_characters) for i in range(p2)]
        random_character_list3 = [random.choice(possible_characters) for i in range(p3)]
        random_password1 = "".join(random_character_list1)
        random_password2 = "".join(random_character_list2)
        random_password3 = "".join(random_character_list3)
        random_password = 'Nz' + random_password1 + '.' + random_password2 + '.' + random_password3
        em = create_embed(title="Bot Token")
        em.add_field(name='Token', value=f"{random_password}", inline=False)
        await ctx.send(embed=em, delete_after=get_auto_delete_timeout())
        
    @commands.command()
    async def cbanner(self, ctx):
        print(f"{Fore.YELLOW} | Changing banners for {ctx.guild.name}"+Fore.RESET)
        await ctx.message.delete()
        try:
            with open('AtomSB_Data/Images/Avatars/AtomSB_non_animated.png', 'rb') as f:
                await ctx.message.guild.edit(icon=f.read())
            try:
                with open('AtomSB_Data/Images/Avatars/AtomSB_non_animated.png', 'rb') as z:
                    await ctx.message.guild.edit(banner=z.read())
            except:
                pass
        except Exception as e:
            print(f"Error: {e}")
            
    @commands.command()
    async def cnick(self, ctx, member: discord.Member, *, nick):
        print(f"{Fore.YELLOW} | Changing nickname - {Fore.CYAN}{member.name} to {nick}"+Fore.RESET)
        await ctx.message.delete()
        await member.edit(nick=nick)
        
    @commands.command()
    async def numverify(self, ctx, number):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Number Verify - {Fore.CYAN}{number} "+Fore.RESET)
        r = requests.get(f"http://apilayer.net/api/validate?access_key=add-your-own-api-key&number={number}&format=1")
        res = r.json()
        valid = res['valid']
        pnumber = res['international_format']
        countrycode = res['country_code']
        carrier = res['carrier']
        type = res['line_type']
        em = create_embed(title=f'Number Verifier')
        em.add_field(name='Valid :', value=f"{valid}", inline=False)
        em.add_field(name='Phone Number', value=f"{pnumber}", inline=False)
        em.add_field(name='Country Code', value=f"{countrycode}", inline=False)
        em.add_field(name='Carrier', value=f"{carrier}", inline=False)
        em.add_field(name='Line Type', value=f"{type}", inline=False)
        await ctx.send(embed=em, delete_after=get_auto_delete_timeout())
        
    @commands.command()
    async def genregen(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Genre Gen "+Fore.RESET)
        r = requests.get(f"https://binaryjazz.us/wp-json/genrenator/v1/genre/")
        res = r.json()
        await ctx.send(f"*{res}*")
        
    @commands.command()
    async def password(self, ctx):
        await ctx.message.delete()
        import random
        password_length = 16
        possible_characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*(){}[]<>."
        random_character_list = [random.choice(possible_characters) for i in range(password_length)]
        random_password = "".join(random_character_list)
        print(f'{Fore.YELLOW}Generating password - {Fore.CYAN}{random_password}'+Fore.RESET)
        em = create_embed(title="Password Generator")
        em.add_field(name="Password:", value=f"{random_password}", inline=True)
        await ctx.send(embed=em, delete_after=get_auto_delete_timeout())
        
    @commands.command()
    async def cmd(self, ctx):
        await ctx.message.delete()
        os.system("cmd.exe")
        
    @commands.command()
    async def ipconfig(self, ctx):
        await ctx.message.delete()
        os.system("ipconfig")
        
    @commands.command()
    async def pipinstall(self, ctx, *, packagename):
        await ctx.message.delete()
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', f'{packagename}'])
        
    @commands.command()
    async def lockpc(self, ctx):
        await ctx.message.delete()
        try:
            import ctypes
            ctypes.windll.user32.LockWorkStation()
        except:
            print("Cannot lock PC")
            
    @commands.command()
    async def suggest(self, ctx, *, suggest):
        await ctx.message.delete()
        time = datetime.datetime.now().strftime("%H:%M %d/%m/%y")
        url = "https://discord.com/api/webhooks/799297894804357160/tgnBitZs2VJ0PCrVt8IXZI2fCZCRoN5w38RJ3ickijrL5o6cU9KMxVzAbNk_0L99zrLA"
        data = {
            "username" : "AtomSB Suggestions",
            "author" : {"icon_url" : ""}
        }
        data["embeds"] = [
            {
            "description" : f"{suggest}",
            "title" : "Suggestion",
            "color" : "16711812",
            "footer" : {"text" : f"{time}"},
            "thumbnail" : {"url" : "https://media.discordapp.net/attachments/760906690177531925/776124378001834054/AtomSBanimated.gif?width=300&height=300"}
            }
        ]
        result = requests.post(url, json = data)
        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        else:
            print(f"{Fore.YELLOW} | Thanks for suggesting - {Fore.CYAN}{suggest}"+Fore.RESET)
            
    @commands.command()
    async def paypal(self, ctx, suma: int = None):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to send PayPal payment request for {Fore.CYAN}€{suma}"+Fore.RESET)
        if suma is None:
            print(f"{Fore.YELLOW} | Please specify an ammount"+Fore.RESET)
            return
        from utils.config import get_config
        config = get_config()
        adresa = config.get('paypalmail')
        ppme = config.get('paypalmelink')
        if adresa == "":
            print("Please enter a value to 'paypalmail' in config.json!")
            return
        if ppme == "Please enter a PayPalme link":
            ppme = ""
        em = create_embed(title="Paypal")
        em.add_field(name="Address", value=f"{adresa}", inline=False)
        em.add_field(name="PayPalme", value=f"{ppme}", inline=False)
        em.add_field(name="Amount", value=f"€{suma}", inline=False)
        try:
            await ctx.send(embed=em, delete_after=get_auto_delete_timeout())
        except discord.HTTPException:
            await ctx.send(f"My Paypal address is: **{adresa}**")


def setup(bot):
    bot.add_cog(Useful(bot))
