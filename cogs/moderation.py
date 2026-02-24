import discord
from discord.ext import commands
from utils.helpers import EMBED_COLOUR, VERSION, create_embed
from utils.config import get_auto_delete_timeout
from colorama import Fore


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def massr(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to make spam the server with roles"+Fore.RESET)
        import asyncio
        while True:
            try:
                guild = ctx.guild
                await guild.create_role(name="AtomSB")
            except:
                return
                
    @commands.command()
    async def massc(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to spam the server with channels"+Fore.RESET)
        import asyncio
        while True:
            try:
                guild = ctx.guild
                await guild.create_text_channel(name="Atom SB")
            except:
                return
                
    @commands.command()
    async def delc(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to delete all channels"+Fore.RESET)
        for channel in list(ctx.guild.channels):
            try:
                await channel.delete()
            except:
                return
                
    @commands.command()
    async def delr(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to delete all roles"+Fore.RESET)
        for role in list(ctx.guild.roles):
            try:
                await role.delete()
            except:
                pass
                
    @commands.command()
    async def massun(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to Mass Unban"+Fore.RESET)
        import asyncio
        banlist = await ctx.guild.bans()
        for users in banlist:
            try:
                await asyncio.sleep(2)
                await ctx.guild.unban(user=users.user)
            except:
                pass
                
    @commands.command()
    async def copys(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to Copy {ctx.guild.name}"+Fore.RESET)
        import asyncio
        await self.bot.create_guild(f'Copy of {ctx.guild.name}')
        await asyncio.sleep(4)
        for g in self.bot.guilds:
            if f'Copy of {ctx.guild.name}' in g.name:
                for c in g.channels:
                    await c.delete()
                for cate in ctx.guild.categories:
                    x = await g.create_category(f"{cate.name}")
                    for chann in cate.channels:
                        if isinstance(chann, discord.TextChannel):
                            await x.create_text_channel(f"{chann}")
                        elif isinstance(chann, discord.VoiceChannel):
                            await x.create_voice_channel(f"{chann}")
                            
                for chann in ctx.guild.channels:
                    if chann.category is None:
                        if isinstance(chann, discord.TextChannel):
                            await g.create_text_channel(f"{chann}")
                        elif isinstance(chann, discord.VoiceChannel):
                            await g.create_voice_channel(f"{chann}")
                            
                for role in ctx.guild.roles:
                    name = role.name
                    color = role.colour
                    perms = role.permissions
                    await g.create_role(name=name, permissions=perms, colour=color)
                    
        print(f"{Fore.GREEN} | Succesfully Duplicated Server" + Fore.RESET)
        
    @commands.command()
    async def destroys(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to Destroy the entire server"+Fore.RESET)
        for channel in list(ctx.guild.channels):
            try:
                await channel.delete()
            except:
                pass
        for user in list(ctx.guild.members):
            try:
                await user.ban()
            except:
                pass
        for role in list(ctx.guild.roles):
            try:
                await role.delete()
            except:
                pass
        try:
            await ctx.guild.edit(
                name="AtomSB",
                description="None",
                reason="None",
                icon=None,
                banner=None
            )
        except:
            pass
        import asyncio
        while True:
            try:
                guild = ctx.guild
                await guild.create_text_channel(name="Atom SB")
            except:
                return
        while True:
            try:
                guild = ctx.guild
                await guild.create_role(name="AtomSB")
            except:
                return
                
    @commands.command()
    async def purge(self, ctx, amount: int):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to purge all messages in the channel"+Fore.RESET)
        async for message in ctx.message.channel.history(limit=amount).filter(lambda m: m.author == self.bot.user).map(lambda m: m):
            try:
                await message.delete()
            except:
                pass


def setup(bot):
    bot.add_cog(Moderation(bot))
