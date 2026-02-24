import discord
from discord.ext import commands
from utils.helpers import EMBED_COLOUR, VERSION
from utils.config import get_prefix
from colorama import Fore


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def help(self, ctx):
        await ctx.message.delete()
        prefix = get_prefix()
        print(f"""{Fore.YELLOW}
Information:{Fore.CYAN}
 help - Lists all the commands available
 ip (IP) - Search up info about an IP
 lookup (@user) - Get information on the user
 ping - The bot's ping
 atomsb - Information about AtomSB
 pcspecs - Information about your PC (only works with Nvidia cards atm)
 
Status:{Fore.CYAN}
 sgame (message) - Sets your activity to playing (message)
 sstream (message) - Sets your activity to streaming with the URL specified in config.json and adds your message as the title
 swatching (message) - Sets your activity to watching (message)
 slistening (message) - Sets your activity to lisetening (message)
 stopactivity - Stops your current activity status
 typing (time-spent-typing) - Type for your specified amount of time (default is 2 hours if a value is not supplied)
 invisible - Sets status to Invisible
 online - Sets status to Online 
 dnd - Sets status to Do Not Disturb
 idle - Sets status to Idle

Profile:{Fore.CYAN}
 reverseav (@user) - Reverse lookup a users avatar
 avatar (@user) - Pastes a users Avatar into chat
 nickname (message) - Change your nickname
 blankprofile - changes your pfp and name to a blank image and name
 steal (@user)  - Steal a users profile picture
 set (URL)     - Set's your profile picture to the url specified
 hypesquad (house) - Change your Hypesquad eg.(brilliance, bravery, balance or random)
 junknickname - Make your nickname junk on a server
 invisablenickname - Set's your username to nothing

Fun:{Fore.CYAN}
 selfdestruct (delay) - Send a self destructing message that will delete your last message
 dick (@user) - Users Dick size 8=D
 gay (@user) - A gaydad 
 spam (amount, delay, message) - Spam a particular message
 stopspam - stops spamming messages
 joke - Get a new joke!
 modem - Pretty self explanitory
 music - Play music files in /Music/song.mp3 (MUST BE NAMED song.mp3)
 sendmusic - Share your saved song
 copyuser (@user) - Copy a user exactly
 stopcopy (@user) - Stops copying a user
 triggered (@user) - Trigger a user
 kanyeq - A Kanye quote
 geekj - A geek joke
 911 - 9/11
 insult - Insult people
 randomfact - Random fact
 bored - Gives you ideas of things to do
 ageguess (name) - Guesses a users name
 iss - International Space Stations current location
 Cyberpunk (xbox,ps4,pc or wii) - Meme about Cyberpunk on different versions
 copyname - Set your Discord name to copy a user
 ricky - Set your Discord name and pfp to Rick Astley
 rikka - Set your Discord name and pfp to Rikka
 yes - Answers No
 no - Answers Yes
 yesno - Randomly chooses between yes and no
 dice - Roll a dice

Games:{Fore.CYAN}
 wyr - Sends a Would you rather into the chat
 dice - 6 sided dice roll

Money:{Fore.CYAN}
 price (btc/ltc/eth) - Current prices of major crypto currencies

Malicious:{Fore.CYAN}
 login (token) - Login to a Discord token 
 botlogin (token) - Login to a Discord Bot token
 tokenmess (token) - Absolutely mess a token
 tokeninfo (token) - Information about a token
 destroys - Destroy a server
 massr - Give everyone a particular role
 massc - Make a large amount of channels
 delc - Deletes all channels
 delr - Deletes all Roles
 massun - Unbans Everyone
 spamr - Spams a server with roles
 nuke - Destroys a server (alternative to the destroy command)
 massping - Attempt to spam a user in every channel
 ban (member) (reason) - Ban users in a server
 kick (member) (reason) - Kick users in a server
 nukechannel - Nuke a channel in a server

Web:{Fore.CYAN}
 google (search) - Google things
 yt (search) - Search on youtube
 weather (city) - View the weather of any city
 shrink (URL) - Shorten a URL
 pingsite (URL) - Ping a webserver
 covid - Latest worldwide Covid-19 stats

Chat:{Fore.CYAN}
 embedsay (message) - Send an embedded message
 choose (Choices eg. test1 test2 test3) - Picks a random choice
 space (message) - Sends a message with a space between each letter
 encode (message) - Encode a message
 decode (message) - Decode a message
 trump (message) - Send a trump tweet
 tweet (name) (message) - Make a tweet!
 code (message) - Automatically send your code in Discords code format
 devowel (message) - Devowels your message
 tts (message) - Create a text to speak message
 caps (message) - Makes you message all uppercase
 firstmsg - Get's the first message of a channel
 abcs - Goes through the ABC's
 virus (user) - Inject a virus into a user
 count (number to count to) - Goes through every number to get to the specified number
 stopcount - Stops the counting process
 topicstarter - Conversation starters
 reverse (message)  - reverse your message   
 unreverse (message) - unreverse a message 
 shrug - Shrugs
 lenny - Lenny
 tableflip - Flip the damm table
 bold (message) - Bold your message
 secret (message) - Makes your message a secret
 nitro (amount) - Send Nitro to people
 junk - Send a large blank message
 snipe - View the recent message sniped
 editsnipe - View the last edited message sniped
 cyclenick (message) - Cycle your nickname 
 stopcyclenick - Stops the cycle
 massreact (emote) (ammount) - Add reactions in a specific channel for a specified amount
 advice - Get some advice!
 clyde (message) - Send a message as clyde the Discord bot
 changemymind (message) - Sends the change my mind meme
 chatbot (message) - Talk to the AtomSB AI chatbot
 sendall (message) - Send a message to every channel in the server specified
 quickdel (message) - Send a message that will be deleted after 1 second
 credits - View credits of the SB
 masspin (amount) - Masspin messages in a server
 lyrics (artist) (song) - Posts lyrics to a song (under 2,000 characters)
 giphy (name) - Search for any gif in the giphy database
 py (code) - Makes the message you type into py code  
 cpp (code) - Makes the message you type into c++ code
 flip (message) - Flip your message
 ranstory - Generate a random short story

Useful:{Fore.CYAN}
 serverinfo - Get info about the server
 aboutbot - info about the bot SB
 time - Gives the current time
 date - Gives the current date
 copys - Copy a server exactly
 dm (user) (message) - Send a Dm to a user
 bump (channel_Id) - Auto bump a server
 stopbump - Stops auto bumping a channel
 servericon - Gets the name of the guild with the guild icon
 backupfriends - Backup all your friends to a txt file
 purge (ammount) - Purge a certain ammount of messages
 read - Marks all you guilds as read
 banner - Sever banner
 light - Set's discord theme to light
 dark - Set's discord theme to dark
 search (link) - Open a new tab in your defalut browser
 adminservers - Lists all the servers you have perms in
 screenshot - Take a quick screenshot of your desktop
 nickscan - Scan for servers you have nicknames in
 bans - View bans in the current server
 bottoken - Random Discord Bot token
 cbanner - Change server banner and icon
 cnick (@member) (nickname) - Change a users nickname in a server
 numverify (number) - Search info about a phone number
 genregen - Generates a topic 
 password - Generate a strong password
 cmd - Opens Command prompt
 ipconfig - Get info on your network connections
 pipinstall (module) - Install python modules with this command
 lockpc - Lock your PC
 suggest (idea) - Send your suggestions to be added to the selfbot
 paypal (ammount) - send your paypal link to other people

SelfBot:{Fore.CYAN}
 clear - Clears the selfbot window
 restart - Restart AtomSB
 logout - Logout of the selfbot.

        """+Fore.RESET)
        
    @commands.command()
    async def helpweb(self, ctx):
        await ctx.message.delete()
        url = 'https://atom-sb.com/feature-list/'
        try:
            webbrowser.open(url)
        except:
            print(f'{Fore.RED}Page is currently under maintenance')
            
    @commands.command()
    async def atomsb(self, ctx):
        await ctx.message.delete()
        print(f"{Fore.YELLOW} | Thank you for advertising AtomSB! :)"+Fore.RESET)
        em = discord.Embed(title="AtomSB", color=EMBED_COLOUR, url='https://atom-sb.com/')
        em.add_field(name='User', value=f'{self.bot.user.name}#{self.bot.user.discriminator}', inline=False)
        em.add_field(name='Version', value=f'Atom SB v{VERSION}', inline=False)
        em.add_field(name='About', value=f'https://atom-sb.com/', inline=False)
        em.add_field(name='Features', value=f'https://atom-sb.com/Feature-List/', inline=False)
        await ctx.send(embed=em, delete_after=get_auto_delete_timeout())


def setup(bot):
    bot.add_cog(Help(bot))
