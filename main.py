import os
import sys
import asyncio
import discord
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

os.system('cls')

from colorama import Fore, Style, init
import ctypes
import time

from bot.bot import AtomSB
from utils.config import (
    get_token, 
    load_config,
    get_prefix,
    get_password,
    get_giveaway_sniper,
    get_nitro_sniper,
    get_silent_mode,
    get_auto_delete_timeout,
    get_auto_giveaway_delay
)
from utils.helpers import VERSION
from utils.auth import startprint
from utils.keyauth import keyauthapp

init(autoreset=True)


def main():
    ctypes.windll.kernel32.SetConsoleTitleW(f'Atom Selfbot v{VERSION} - Loaded')
    
    print(f"{Fore.CYAN}Initializing...")
    time.sleep(2)
    os.system('cls')
    
    load_config()
    
    token = get_token()
    if token == "token-here" or token is None:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.RED}[ERROR] {Fore.YELLOW}You didn't put your token in the config.json file"+Fore.RESET)
        input("Press Enter to exit...")
        sys.exit(1)
    
    print(f"""
{Fore.YELLOW}

        █████╗ ████████╗ ██████╗ ███╗   ███╗       ███████╗███████╗██╗     ███████╗██████╗  ██████╗ ████████╗
       ██╔══██╗╚══██╔══╝██╔═══██╗████╗ ████║       ██╔════╝██╔════╝██║     ██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝
       ███████║   ██║   ██║   ██║██╔████╔██║       ███████╗█████╗  ██║     █████╗  ██████╔╝██║   ██║   ██║   
       ██╔══██║   ██║   ██║   ██║██║╚██╔╝██║       ╚════██║██╔══╝  ██║     ██╔══╝  ██╔══██╗██║   ██║   ██║   
       ██║  ██║   ██║   ╚██████╔╝██║ ╚═╝ ██║       ███████║███████╗███████╗██║     ██████╔╝╚██████╔╝   ██║   
       ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝       ╚══════╝╚══════╝╚══════╝╚═╝     ╚═════╝  ╚═════╝    ╚═╝   
                                                ---AtomSB Bot---
    {Fore.CYAN}
    Starting bot...
    Loading cogs...
    """)
    
    try:
        import bot.events
        
        @AtomSB.event
        async def on_connect():
            os.system('cls' if os.name == 'nt' else 'clear')
            startprint(
                prefix=get_prefix(),
                username=AtomSB.user.name,
                discriminator=AtomSB.user.discriminator,
                time_delay=get_auto_delete_timeout(),
                silent_mode=get_silent_mode(),
                nitro_sniper=get_nitro_sniper(),
                giveaway_sniper=get_giveaway_sniper(),
                giveaway_delay=get_auto_giveaway_delay()
            )
            ctypes.windll.kernel32.SetConsoleTitleW(f'Atom Selfbot v{VERSION} - Logged into {AtomSB.user.name}#{AtomSB.user.discriminator}')
        
        AtomSB.run(token, reconnect=True)
    except discord.errors.LoginFailure:
        print(f"{Fore.RED}[ERROR] {Fore.YELLOW}Improper token has been passed.{Fore.RESET}")
        print(f"{Fore.YELLOW}This token is not valid. Continuing but will be unable to perform any commands.{Fore.RESET}")
        countdown = 5
        try:
            while countdown > 0:
                print(f"{Fore.CYAN}Continuing in {countdown} seconds...", end='\r')
                time.sleep(1)
                countdown -= 1
            print(f"{Fore.CYAN}Loading modules...                                                   ")
            
            # Load events manually
            import bot.events
            
            print(f"{Fore.CYAN}Loading cogs...")
            
            # Load cogs synchronously since we're not actually running the bot
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
                    import importlib
                    module = importlib.import_module(cog)
                    # Get the setup function and call it directly
                    if hasattr(module, 'setup'):
                        module.setup(AtomSB)
                        print(f"{Fore.CYAN}Loaded {cog}{Fore.RESET}")
                except Exception as e:
                    print(f"{Fore.RED}Failed to load {cog}: {e}{Fore.RESET}")
            
            print(f"{Fore.GREEN}AtomSB Fully Loaded!{Fore.RESET}")
            print(f"{Fore.YELLOW}Note: Not logged in due to invalid token. Commands will not work.{Fore.RESET}")
            print(f"{Fore.CYAN}Press Ctrl+C to exit...")
            
            # Keep running
            try:
                while True:
                    time.sleep(1)
            except (KeyboardInterrupt, SystemExit):
                print(f"{Fore.YELLOW}Exiting...{Fore.RESET}")
                sys.exit(0)
                
        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}Exiting...{Fore.RESET}")
            sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}[ERROR] {Fore.YELLOW}{e}"+Fore.RESET)
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
