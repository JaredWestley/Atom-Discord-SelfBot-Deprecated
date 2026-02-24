import discord
from discord.ext import commands, tasks
import requests
import asyncio
from colorama import Fore


class StatusTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Only start the task if there's an event loop running
        try:
            loop = asyncio.get_running_loop()
            self.btc_status.start()
        except RuntimeError:
            # No event loop running - skip the background task
            pass
        
    @tasks.loop(seconds=3)
    async def btc_status(self):
        try:
            r = requests.get('https://api.coindesk.com/v1/bpi/currentprice/btc.json').json()
            value = r['bpi']['USD']['rate']
            btc_stream = discord.Streaming(
                name="Current BTC price: " + value + "$ USD",
                url="https://www.twitch.tv/monstercat",
            )
            await self.bot.change_presence(activity=btc_stream)
        except:
            pass


def setup(bot):
    bot.add_cog(StatusTasks(bot))
