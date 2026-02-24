import discord
from discord.ext import commands
import requests
from utils.helpers import EMBED_COLOUR, VERSION, create_embed, locales, languages
from utils.config import get_token, get_auto_delete_timeout
from colorama import Fore


class Token(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def tokeninfo(self, ctx, _token):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Getting as much info about - {Fore.CYAN}{_token}"+Fore.RESET)
        headers = {
            'Authorization': _token,
            'Content-Type': 'application/json'
        }
        try:
            res = requests.get('https://canary.discordapp.com/api/v6/users/@me', headers=headers)
            res = res.json()
            user_id = res['id']
            locale = res['locale']
            avatar_id = res['avatar']
            nitro = res['premium_type']
            if nitro == '0':
                nitro = 'None'
            elif nitro == '1':
                nitro = 'Nitro Classic'
            elif nitro == '2':
                nitro = 'Nitro'
            language = languages.get(locale)
            import datetime
            creation_date = datetime.datetime.utcfromtimestamp(((int(user_id) >> 22) + 1420070400000) / 1000).strftime('%d-%m-%Y')
        except KeyError:
            print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}Invalid token"+Fore.RESET)
            
        em = create_embed(
            title='AtomSB TokenInfo',
            description=f"Name: {res['username']}#{res['discriminator']}\nEmail: {res['email']}\nCreation Date: {creation_date}"
        )
        fields = [
            {'name': 'Phone', 'value': res['phone']},
            {'name': 'Flags', 'value': res['flags']},
            {'name': 'Public flags', 'value': res['public_flags']},
            {'name': 'Language', 'value': f"{res['locale']} {language}"},
            {'name': 'MFA', 'value': res['mfa_enabled']},
            {'name': 'Nitro', 'value': f"{nitro}"},
            {'name': 'Verified', 'value': res['verified']},
        ]
        for field in fields:
            if field['value']:
                em.add_field(name=field['name'], value=field['value'], inline=False)
        
        timeout = get_auto_delete_timeout()
        return await ctx.send(embed=em, delete_after=timeout)
        
    @commands.command()
    async def tokenfixer(self, ctx):
        await ctx.message.delete()
        embed = create_embed(title="Token Fixer", description="https://mega.nz/folder/epQREK5J#Zx5aRRGdTfp2RB8TZS9vfg")
        timeout = get_auto_delete_timeout()
        await ctx.send(embed=embed, delete_after=timeout)


def setup(bot):
    bot.add_cog(Token(bot))
