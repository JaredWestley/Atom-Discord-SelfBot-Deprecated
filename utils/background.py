import discord
from discord.ext import tasks
import requests
import asyncio
import functools
import io
import threading


async_executor_loop = asyncio.get_event_loop()


def async_executor():
    def outer(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            thing = functools.partial(func, *args, **kwargs)
            return async_executor_loop.run_in_executor(None, thing)
        return inner
    return outer


@async_executor()
def do_tts(message, tts_language='en'):
    from gtts import gTTS
    f = io.BytesIO()
    tts = gTTS(text=message.lower(), lang=tts_language)
    tts.write_to_fp(f)
    f.seek(0)
    return f


def Nitro():
    import random
    import string
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    return f'https://discord.gift/{code}'


def BotTokens():
    with open('AtomSB_Data/Data/Tokens/bot-tokens.txt', 'a+') as f:
        tokens = {token.strip() for token in f if token}
    for token in tokens:
        yield token


def UserTokens():
    with open('AtomSB_Data/Data/Tokens/user-tokens.txt', 'a+') as f:
        tokens = {token.strip() for token in f if token}
    for token in tokens:
        yield token


class Login(discord.Client):
    async def on_connect(self):
        guilds = len(self.guilds)
        users = len(self.users)
        print("")
        print(f"Connected to: [{self.user.name}]")
        print(f"Token: {self.http.token}")
        print(f"Guilds: {guilds}")
        print(f"Users: {users}")
        print("-------------------------------")
        await self.logout()


def mass_login(choice):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    if choice == 'user':
        for token in UserTokens():
            loop.run_until_complete(Login().start(token, bot=False))
    elif choice == 'bot':
        for token in BotTokens():
            loop.run_until_complete(Login().start(token, bot=True))


def Dump(ctx):
    for member in ctx.guild.members:
        f = open(f'AtomSB_Data/Images/{ctx.guild.id}-Dump.txt', 'a+')
        f.write(str(member.avatar_url) + '\n')


Sent = 0
Errors = 0
lock = threading.Lock()


def safe_print(arguments):
    lock.acquire()
    print(arguments)
    lock.release()


def Report(channel, message, guild, reason, token):
    global Sent, Errors
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
            print(f'Invalid token: %s' % (token))
        else:
            Errors += 1
    except Exception as Error:
        print(Error)
