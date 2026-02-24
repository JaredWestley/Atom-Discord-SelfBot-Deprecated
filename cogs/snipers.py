import discord
from discord.ext import commands
import re
import datetime
import requests
import asyncio
from utils.config import get_nitro_sniper, get_giveaway_sniper, get_silent_mode, get_auto_giveaway_delay, get_token
from colorama import Fore


class Snipers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.nitro_sniper = get_nitro_sniper()
        self.giveaway_sniper = get_giveaway_sniper()
        self.privnote_sniper = get_silent_mode()
        self.slotbot_sniper = get_silent_mode()
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user.id:
            return
            
        token = get_token()
        
        if 'discord.gift/' in message.content and self.nitro_sniper:
            try:
                code = re.search("discord.gift/(.*)", message.content).group(1)
                headers = {'Authorization': token}
                
                start = datetime.datetime.now()
                r = requests.post(
                    f'https://discordapp.com/api/v6/entitlements/gift-codes/{code}/redeem', 
                    headers=headers,
                ).text
                elapsed = datetime.datetime.now() - start
                elapsed_str = f'{elapsed.seconds}.{elapsed.microseconds}'
                
                time = datetime.datetime.now().strftime("%H:%M %p")
                
                if 'This gift has been redeemed already.' in r:
                    print(f"{Fore.YELLOW}Nitro redeemed by another user - {Fore.CYAN}{time}")
                    print(f" {Fore.YELLOW}| Nitro Code - {Fore.CYAN}{code}")
                    print(f" {Fore.YELLOW}| Information - By: {Fore.CYAN} {message.author} {Fore.YELLOW}In: {Fore.CYAN}{message.channel}, {message.guild}")
                    print(f" {Fore.YELLOW}| Delay - {Fore.CYAN}{elapsed_str}")
                elif 'subscription_plan' in r:
                    print(f"{Fore.YELLOW}Nitro has been redeemed! - {Fore.CYAN}{time}")
                    print(f" {Fore.YELLOW}| Nitro Code - {Fore.CYAN}{code}")
                    print(f" {Fore.YELLOW}| Information - By: {Fore.CYAN} {message.author} {Fore.YELLOW}In: {Fore.CYAN}{message.channel}, {message.guild}")
                    print(f" {Fore.YELLOW}| Delay - {Fore.CYAN}{elapsed_str}")
                elif 'Unknown Gift Code' in r:
                    print(f"{Fore.YELLOW}Invalid nitro code - {Fore.CYAN}{time}")
                    print(f" {Fore.YELLOW}| Nitro Code - {Fore.CYAN}{code}")
                    print(f" {Fore.YELLOW}| Information - By: {Fore.CYAN} {message.author} {Fore.YELLOW}In: {Fore.CYAN}{message.channel}, {message.guild}")
                    print(f" {Fore.YELLOW}| Delay - {Fore.CYAN}{elapsed_str}")
            except Exception as e:
                print(f"{Fore.RED}[ERROR]{Fore.YELLOW} Nitro sniper error: {e}")
                
        if 'GIVEAWAY' in message.content and self.giveaway_sniper:
            if message.author.id == 294882584201003009:
                try:
                    giveaway_delay = get_auto_giveaway_delay()
                    await asyncio.sleep(int(giveaway_delay))
                    await message.add_reaction("🎉")
                    time = datetime.datetime.now().strftime("%H:%M %p")
                    print(f"{Fore.CYAN}[{time} - Giveaway Entered!]")
                    print(f" {Fore.YELLOW}| Channel - {Fore.CYAN}{message.channel}")
                    print(f" {Fore.YELLOW}| Server - {Fore.CYAN}{message.guild}")
                except discord.errors.Forbidden:
                    time = datetime.datetime.now().strftime("%H:%M %p")
                    print(f"{Fore.CYAN}[{time} - Couldn't enter Giveaway]")
                    print(f" {Fore.YELLOW}| Channel - {Fore.CYAN}{message.channel}")
                    print(f" {Fore.YELLOW}| Server - {Fore.CYAN}{message.guild}")
                    
        if 'Congratulations!' in message.content and self.giveaway_sniper:
            if message.author.id == 294882584201003009:
                time = datetime.datetime.now().strftime("%H:%M %p")
                print(f"{Fore.CYAN}[{time} - You won a Giveaway]")
                print(f" {Fore.YELLOW}| Channel - {Fore.CYAN}{message.channel}")
                print(f" {Fore.YELLOW}| Server - {Fore.CYAN}{message.guild}")


def setup(bot):
    bot.add_cog(Snipers(bot))
