import discord
from discord.ext import commands
from utils.config import get_prefix
from utils.helpers import VERSION


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        
        super().__init__(
            command_prefix=get_prefix(),
            intents=intents,
            description='Atom Selfbot',
            self_bot=True
        )
        self.remove_command('help')
        
        self.copyuser = None
        self.msgsniper = True
        self.snipe_history_dict = {}
        self.sniped_message_dict = {}
        self.sniped_edited_message_dict = {}
        
    async def setup_hook(self):
        await self.load_cogs()
        
    async def load_cogs(self):
        cogs = [
            'cogs.fun',
            'cogs.fun2',
            'cogs.info',
            'cogs.moderation',
            'cogs.nitro',
            'cogs.profile',
            'cogs.utility',
            'cogs.token',
            'cogs.status',
            'cogs.chat',
            'cogs.useful',
            'cogs.help',
            'cogs.malicious',
            'cogs.selfbot',
            'cogs.snipers',
            'cogs.status_tasks',
        ]
        for cog in cogs:
            try:
                await self.load_extension(cog)
                print(f"Loaded {cog}")
            except Exception as e:
                print(f"Failed to load {cog}: {e}")


AtomSB = Bot()
