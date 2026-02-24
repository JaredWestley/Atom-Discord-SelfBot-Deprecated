import os
import sys
import time
import requests
from colorama import Fore, init

init(autoreset=True)


def get_motd():
    try:
        r = requests.get("https://atomsb.000webhostapp.com/")
        res = r.json()
        return res['main']['quote'], res['main']['serverinv']
    except:
        return "Welcome to AtomSB", "https://discord.gg/atomsb"


def auth_menu():
    from utils.keyauth import keyauthapp
    
    print(f"{Fore.CYAN}Initializing")
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')
    keyauthapp.init()
    
    print(f"""{Fore.YELLOW}

        █████╗ ████████╗ ██████╗ ███╗   ███╗       ███████╗███████╗██╗     ███████╗██████╗  ██████╗ ████████╗
       ██╔══██╗╚══██╔══╝██╔═══██╗████╗ ████║       ██╔════╝██╔════╝██║     ██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝
       ███████║   ██║   ██║   ██║██╔████╔██║       ███████╗█████╗  ██║     █████╗  ██████╔╝██║   ██║   ██║   
       ██╔══██║   ██║   ██║   ██║██║╚██╔╝██║       ╚════██║██╔══╝  ██║     ██╔══╝  ██╔══██╗██║   ██║   ██║   
       ██║  ██║   ██║   ╚██████╔╝██║ ╚═╝ ██║       ███████║███████╗███████╗██║     ██████╔╝╚██████╔╝   ██║   
       ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝       ╚══════╝╚══════╝╚══════╝╚═╝     ╚═════╝  ╚═════╝    ╚═╝   
                                            ---AtomSB Auth---
        
 {Fore.YELLOW} | 1 - {Fore.CYAN}Login
 {Fore.YELLOW} | 2 - {Fore.CYAN}Register
 {Fore.YELLOW} | 3 - {Fore.CYAN}Upgrade
 """)
    
    ans = input(f"{Fore.YELLOW} | - {Fore.CYAN}Select Option : ")
    
    if ans == "1":
        user = input('Provide username: ')
        password = input('Provide password: ')
        keyauthapp.login(user, password)
    elif ans == "2":
        user = input('Provide username: ')
        password = input('Provide password: ')
        license_key = input('Provide License: ')
        keyauthapp.register(user, password, license_key)
    elif ans == "3":
        user = input('Provide username: ')
        license_key = input('Provide License: ')
        keyauthapp.upgrade(user, license_key)
    else:
        print("\n Not Valid Option")


def startprint(prefix, username, discriminator, time_delay, silent_mode, nitro_sniper, giveaway_sniper, giveaway_delay):
    atombotinfo1, atombotinfo2 = get_motd()
    
    giveaway = f"{Fore.GREEN}Enabled" if giveaway_sniper else f"{Fore.RED}Disabled"
    nitro = f"{Fore.GREEN}Enabled" if nitro_sniper else f"{Fore.RED}Disabled"
    
    print(f'''{Fore.YELLOW}

        █████╗ ████████╗ ██████╗ ███╗   ███╗       ███████╗███████╗██╗     ███████╗██████╗  ██████╗ ████████╗
       ██╔══██╗╚══██╔══╝██╔═══██╗████╗ ████║       ██╔════╝██╔════╝██║     ██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝
       ███████║   ██║   ██║   ██║██╔████╔██║       ███████╗█████╗  ██║     █████╗  ██████╔╝██║   ██║   ██║   
       ██╔══██║   ██║   ██║   ██║██║╚██╔╝██║       ╚════██║██╔══╝  ██║     ██╔══╝  ██╔══██╗██║   ██║   ██║   
       ██║  ██║   ██║   ╚██████╔╝██║ ╚═╝ ██║       ███████║███████╗███████╗██║     ██████╔╝╚██████╔╝   ██║   
       ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝       ╚══════╝╚══════╝╚══════╝╚═╝     ╚═════╝  ╚═════╝    ╚═╝                                                                                                                                               

 {Fore.YELLOW} | MOTD            - {Fore.CYAN}{atombotinfo1}
 {Fore.YELLOW} | Discord         - {Fore.CYAN}{atombotinfo2}

 {Fore.YELLOW} | Prefix          - {Fore.CYAN}{prefix}
 {Fore.YELLOW} | Version         - {Fore.CYAN}v1.4
 {Fore.YELLOW} | Username        - {Fore.CYAN}{username}#{discriminator}
 {Fore.YELLOW} | Delete Delay    - {Fore.CYAN}{time_delay} seconds
 {Fore.YELLOW} | Silent Mode     - {Fore.CYAN}{silent_mode}
 {Fore.YELLOW} | Nitro Sniper    - {nitro}
 {Fore.YELLOW} | Giveaway Sniper - {giveaway} {Fore.CYAN}- {giveaway_delay} seconds
 {Fore.YELLOW} | Help            - {Fore.CYAN}To get started type {prefix}help or {prefix}helpweb into a chat on discord!
    '''+Fore.RESET)


def check_token(token):
    from utils.config import get_token
    token = get_token()
    if token == "token-here" or token is None:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{Fore.RED}[ERROR] {Fore.YELLOW}You didn't put your token in the config.json file"+Fore.RESET)
        return False
    return True
