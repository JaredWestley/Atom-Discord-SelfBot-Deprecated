import discord
from discord.ext import commands
import requests
import re
import datetime
from utils.config import get_nitro_sniper, get_giveaway_sniper, get_auto_giveaway_delay, get_silent_mode, get_token, get_auto_delete_timeout
from colorama import Fore


class Nitro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def nitro(self, ctx):
        await ctx.message.delete()
        import random
        import string
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        await ctx.send(f"https://discord.gift/{code}")


def setup(bot):
    bot.add_cog(Nitro(bot))
