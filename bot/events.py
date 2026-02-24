import discord
from discord.ext import commands
from discord import utils as discord_utils
import re
import asyncio

from bot.bot import AtomSB
from utils.config import get_giveaway_sniper, get_nitro_sniper, get_silent_mode, get_auto_giveaway_delay
from utils.helpers import EMBED_COLOUR, VERSION
from colorama import Fore

URL_RE = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')


@AtomSB.event
async def on_connect():
    from utils.config import get_token
    from utils.helpers import get_hwid
    import os
    os.system('cls')
    
    print(f"""
{Fore.CYAN}
        █████╗ ████████╗ ██████╗ ███╗   ███╗       ███████╗███████╗██╗     ███████╗██████╗  ██████╗ ████████╗
       ██╔══██╗╚══██╔══╝██╔═══██╗████╗ ████║       ██╔════╝██╔════╝██║     ██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝
       ███████║   ██║   ██║   ██║██╔████╔██║       ███████╗█████╗  ██║     █████╗  ██████╔╝██║   ██║   ██║   
       ██╔══██║   ██║   ██║   ██║██║╚██╔╝██║       ╚════██║██╔══╝  ██║     ██╔══╝  ██╔══██╗██║   ██║   ██║   
       ██║  ██║   ██║   ╚██████╔╝██║ ╚═╝ ██║       ███████║███████╗███████╗██║     ██████╔╝╚██████╔╝   ██║   
       ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝       ╚══════╝╚══════╝╚══════╝╚═╝     ╚═════╝  ╚═════╝    ╚═╝   
{Fore.YELLOW} | MOTD            - {Fore.CYAN}Welcome to AtomSB
{Fore.YELLOW} | Discord         - {Fore.CYAN}Connected
{Fore.YELLOW} | Prefix          - {Fore.CYAN}{AtomSB.command_prefix}
{Fore.YELLOW} | Version         - {Fore.CYAN}v{VERSION}
{Fore.YELLOW} | Username        - {Fore.CYAN}{AtomSB.user.name}#{AtomSB.user.discriminator}
{Fore.YELLOW} | HWID            - {Fore.CYAN}{get_hwid()}
{Fore.YELLOW} | Help            - {Fore.CYAN}Type {AtomSB.command_prefix}help
    """ + Fore.RESET)


@AtomSB.event
async def on_command_error(ctx, error):
    error_str = str(error)
    error = getattr(error, 'original', error)
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.CheckFailure):
        print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}You're missing permission to execute this command"+Fore.RESET)
    elif isinstance(error, commands.MissingRequiredArgument):
        print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}Missing arguments: {error}"+Fore.RESET)
    elif isinstance(error, discord.errors.Forbidden):
        print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}Discord error: {error}"+Fore.RESET)
    elif "Cannot send an empty message" in error_str:
        print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}Couldnt send a empty message"+Fore.RESET)
    else:
        print(f"{Fore.RED}[ERROR]: {Fore.YELLOW}{error_str}"+Fore.RESET)


def escape_mention(text):
    return text.replace('@everyone', '@\u200beveryone').replace('@here', '@\u200bhere')


@AtomSB.event
async def on_message_delete(message):
    if message.author.id == AtomSB.user.id:
        return
    
    if AtomSB.msgsniper:
        if isinstance(message.channel, discord.DMChannel):
            attachments = message.attachments
            if len(attachments) == 0:
                msg_content = escape_mention(str(message.content))
                message_content = f"\n{Fore.YELLOW} | Message Sniper - Delete  \n | User - {Fore.CYAN}{discord_utils.escape_markdown(str(message.author))}\n{Fore.YELLOW} | Deleted - {Fore.CYAN}{msg_content}"
                print(f"{message_content}")
            else:
                links = ""
                for attachment in attachments:
                    links += attachment.proxy_url + "\n"
                message_content = f"\n{Fore.YELLOW} | Message Sniper - Delete  \n | User - {Fore.CYAN}{discord_utils.escape_markdown(str(message.author))}: {discord_utils.escape_mentions(message.content)}\n{Fore.YELLOW} | Deleted - {Fore.CYAN}{links}"
                print(f"{message_content}")
    
    if len(AtomSB.sniped_message_dict) > 1000:
        AtomSB.sniped_message_dict.clear()
    if len(AtomSB.snipe_history_dict) > 1000:
        AtomSB.snipe_history_dict.clear()
    
    attachments = message.attachments
    if len(attachments) == 0:
        channel_id = message.channel.id
        msg_content = escape_mention(str(message.content))
        message_content = f"`{discord_utils.escape_markdown(str(message.author))}`: {msg_content}"
        AtomSB.sniped_message_dict.update({channel_id: message_content})
        
        if channel_id in AtomSB.snipe_history_dict:
            pre = AtomSB.snipe_history_dict[channel_id]
            msg = escape_mention(str(message.content))
            post = f"{message.author}: {msg}"
            AtomSB.snipe_history_dict.update({channel_id: pre[:-3] + post + "\n```"})
        else:
            msg = escape_mention(str(message.content))
            post = f"{message.author}: {msg}"
            AtomSB.snipe_history_dict.update({channel_id: "```\n" + post + "\n```"})
    else:
        links = ""
        for attachment in attachments:
            links += attachment.proxy_url + "\n"
        channel_id = message.channel.id
        message_content = f"`{discord_utils.escape_markdown(str(message.author))}`: {discord_utils.escape_mentions(message.content)}\n\n**Attachments:**\n{links}"
        AtomSB.sniped_message_dict.update({channel_id: message_content})


@AtomSB.event
async def on_message_edit(before, after):
    await AtomSB.process_commands(after)
    if before.author.id == AtomSB.user.id:
        return
    
    if AtomSB.msgsniper:
        if before.content is after.content:
            return
        if isinstance(before.channel, discord.DMChannel):
            attachments = before.attachments
            if len(attachments) == 0:
                before_content = escape_mention(str(before.content))
                after_content = escape_mention(str(after.content))
                message_content = f"\n{Fore.YELLOW} | Message Sniper - Edit  \n | User - {Fore.CYAN}{discord_utils.escape_markdown(str(before.author))}\n{Fore.YELLOW} | Before - {Fore.CYAN}{before_content}\n{Fore.YELLOW} | After - {Fore.CYAN}{after_content}"
                print(f"\n{message_content}")
            else:
                links = ""
                for attachment in attachments:
                    links += attachment.proxy_url + "\n"
                message_content = f"`{discord_utils.escape_markdown(str(before.author))}`: {discord_utils.escape_mentions(before.content)}\n\n**Attachments:**\n{links}"
                print(f"{message_content}")
    
    if len(AtomSB.sniped_edited_message_dict) > 1000:
        AtomSB.sniped_edited_message_dict.clear()
    
    attachments = before.attachments
    if len(attachments) == 0:
        channel_id = before.channel.id
        before_content = escape_mention(str(before.content))
        after_content = escape_mention(str(after.content))
        message_content = f"\n{Fore.YELLOW} | Message Sniper - Editsnipe  \n | User - {Fore.CYAN}{discord_utils.escape_markdown(str(before.author))}\n{Fore.YELLOW} | Before - {Fore.CYAN}{before_content}\n{Fore.YELLOW} | After - {Fore.CYAN}{after_content}"
        AtomSB.sniped_edited_message_dict.update({channel_id: message_content})
    else:
        links = ""
        for attachment in attachments:
            links += attachment.proxy_url + "\n"
        channel_id = before.channel.id
        message_content = f"\n{Fore.YELLOW} | Message Sniper - Attachment  \n | User - {Fore.CYAN}{discord_utils.escape_markdown(str(before.author))}`: {discord_utils.escape_mentions(before.content)}\n{Fore.YELLOW} | AFTER - {Fore.CYAN}{links}"
        AtomSB.sniped_edited_message_dict.update({channel_id: message_content})


@AtomSB.event
async def on_message(message):
    if AtomSB.copyuser is not None and AtomSB.copyuser.id == message.author.id:
        await message.channel.send(chr(173) + message.content)
    
    await AtomSB.process_commands(message)
