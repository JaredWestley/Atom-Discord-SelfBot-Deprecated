import discord
from discord.ext import commands
import requests
import aiohttp
from utils.helpers import EMBED_COLOUR, VERSION, create_embed, format_user_info
from utils.config import get_auto_delete_timeout
from colorama import Fore


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def lookup(self, ctx, *, user: discord.Member = None):
        await ctx.message.delete()
        if user is None:
            user = ctx.author
        print(f"{Fore.YELLOW} | Getting information about - {Fore.CYAN}{user}"+Fore.RESET)
        
        info = format_user_info(user)
        em = create_embed(title=f"Userinfo - {user.name}", description=info["name"])
        em.add_field(name="Joined", value=info["joined"])
        em.add_field(name="Registered", value=info["registered"])
        em.add_field(name="Server Permissions", value=info["permissions"], inline=False)
        if info["role_count"] > 0:
            em.add_field(name=f"Roles [{info['role_count']}]", value=info["roles"], inline=False)
        
        timeout = get_auto_delete_timeout()
        await ctx.send(embed=em, delete_after=timeout)
        
    @commands.command()
    async def ip(self, ctx, *, ipaddr: str = '1.3.3.7'):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Looking up - {Fore.CYAN}{ipaddr}"+Fore.RESET)
        r = requests.get(f'http://extreme-ip-lookup.com/json/{ipaddr}')
        geo = r.json()
        em = create_embed(title='AtomSB IP Info')
        
        fields = [
            {'name': 'IP', 'value': geo['query']},
            {'name': 'Latitude', 'value': geo['lat']},
            {'name': 'Longitude', 'value': geo['lon']},
            {'name': 'City', 'value': geo['city']},
            {'name': 'Continent', 'value': geo['continent']},
            {'name': 'Location', 'value': geo['region']},
            {'name': 'CountryCode', 'value': geo['countryCode']},
            {'name': 'IPType', 'value': geo['ipType']},
            {'name': 'ISP', 'value': geo['isp']},
        ]
        for field in fields:
            if field['value']:
                em.add_field(name=field['name'], value=field['value'], inline=True)
        
        timeout = get_auto_delete_timeout()
        await ctx.send(embed=em, delete_after=timeout)
        
    @commands.command()
    async def avatar(self, ctx, *, user: discord.Member = None):
        await ctx.message.delete()
        user = user or ctx.author
        print(f"{Fore.YELLOW} | Getting avatar - {Fore.CYAN}{user}"+Fore.RESET)
        
        format = "gif"
        if not user.is_avatar_animated():
            format = "png"
        avatar = user.avatar_url_as(format=format if format != "gif" else None)
        
        async with aiohttp.ClientSession() as session:
            async with session.get(str(avatar)) as resp:
                image = await resp.read()
        import io
        with io.BytesIO(image) as file:
            await ctx.send(file=discord.File(file, f"Avatar.{format}"))
            
    @commands.command()
    async def reverseav(self, ctx, user: discord.Member = None):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Looking up {Fore.CYAN}{user}'s {Fore.YELLOW}avatar"+Fore.RESET)
        if user is None:
            user = ctx.author
        try:
            em = create_embed(
                title='Reverse Image Search',
                description=f"https://images.google.com/searchbyimage?image_url={user.avatar_url}"
            )
            timeout = get_auto_delete_timeout()
            await ctx.send(embed=em, delete_after=timeout)
        except Exception as e:
            print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{e}"+Fore.RESET)
            
    @commands.command()
    async def servericon(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Icon of the Guild"+Fore.RESET)
        em = create_embed(title=ctx.guild.name)
        em.set_image(url=ctx.guild.icon_url)
        timeout = get_auto_delete_timeout()
        await ctx.send(embed=em, delete_after=timeout)
        
    @commands.command()
    async def ping(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Ping"+Fore.RESET)
        em = create_embed(title="Pong!", description=f"Latency: {round(self.bot.latency * 1000)}ms")
        timeout = get_auto_delete_timeout()
        await ctx.send(embed=em, delete_after=timeout)
        
    @commands.command()
    async def firstmsg(self, ctx, channel: discord.TextChannel = None):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Finding the first message in this channel"+Fore.RESET)
        if channel is None:
            channel = ctx.channel
        first_message = (await channel.history(limit=1, oldest_first=True).flatten())[0]
        em = create_embed(description=first_message.content)
        em.add_field(name="First Message", value=f"[Jump]({first_message.jump_url})")
        timeout = get_auto_delete_timeout()
        await ctx.send(embed=em, delete_after=timeout)
        
    @commands.command()
    async def pingsite(self, ctx, website=None):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Attempting to ping - {Fore.CYAN}{website}"+Fore.RESET)
        if website is None:
            pass
        else:
            try:
                r = requests.get(website).status_code
            except Exception as e:
                print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{e}"+Fore.RESET)
            
            em = create_embed(title='AtomSB Site Test')
            if r == 404:
                em.add_field(name='Status', value=f'Site is down, status code - {r}', inline=False)
            else:
                em.add_field(name='Status', value=f'Site is up, status code - {r}', inline=False)
            
            timeout = get_auto_delete_timeout()
            await ctx.send(embed=em, delete_after=timeout)


def setup(bot):
    bot.add_cog(Info(bot))
