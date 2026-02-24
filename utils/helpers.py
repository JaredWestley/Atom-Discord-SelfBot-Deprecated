import discord
import random
import string
import subprocess
import platform
import datetime


EMBED_COLOUR = 0xff0084

VERSION = 1.4

start_time = datetime.datetime.utcnow()

def get_hwid():
    if platform.system() != "Windows":
        return "None"
    cmd = subprocess.Popen("wmic useraccount where name='%username%' get sid", stdout=subprocess.PIPE, shell=True)
    (suppost_sid, error) = cmd.communicate()
    suppost_sid = suppost_sid.split(b'\n')[1].strip()
    return suppost_sid.decode()


def RandomColor():
    return discord.Color(random.randint(0x000000, 0xFFFFFF))


def RandString():
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(random.randint(14, 32)))


def Nitro():
    code = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    return f'https://discord.gift/{code}'


def generate_nonce():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))


def format_user_info(user: discord.Member) -> dict:
    date_format = "%a, %d %b %Y %I:%M %p"
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
    role_string = ' '.join([r.mention for r in user.roles][1:]) if len(user.roles) > 1 else "None"
    
    return {
        "name": str(user),
        "joined": user.joined_at.strftime(date_format),
        "registered": user.created_at.strftime(date_format),
        "permissions": perm_string,
        "roles": role_string,
        "role_count": len(user.roles) - 1
    }


def create_embed(title: str, description: str = None, **kwargs) -> discord.Embed:
    em = discord.Embed(
        title=title,
        description=description,
        colour=EMBED_COLOUR,
        url='https://atom-sb.com/'
    )
    if 'thumbnail' in kwargs:
        em.set_thumbnail(url=kwargs['thumbnail'])
    else:
        em.set_thumbnail(url="https://media.discordapp.net/attachments/760906690177531925/776124378001834054/AtomSBanimated.gif?width=300&height=300")
    
    if 'footer' in kwargs:
        em.set_footer(text=f'AtomSB v{VERSION}', icon_url=kwargs['footer'])
    else:
        em.set_footer(text=f'AtomSB v{VERSION}', icon_url="https://media.discordapp.net/attachments/760906690177531925/776124378001834054/AtomSBanimated.gif?width=300&height=300")
    
    return em


languages = {
    'hu': 'Hungarian, Hungary',
    'nl': 'Dutch, Netherlands',
    'no': 'Norwegian, Norway',
    'pl': 'Polish, Poland',
    'pt-BR': 'Portuguese, Brazilian, Brazil',
    'ro': 'Romanian, Romania',
    'fi': 'Finnish, Finland',
    'sv-SE': 'Swedish, Sweden',
    'vi': 'Vietnamese, Vietnam',
    'tr': 'Turkish, Turkey',
    'cs': 'Czech, Czechia, Czech Republic',
    'el': 'Greek, Greece',
    'bg': 'Bulgarian, Bulgaria',
    'ru': 'Russian, Russia',
    'uk': 'Ukranian, Ukraine',
    'th': 'Thai, Thailand',
    'zh-CN': 'Chinese, China',
    'ja': 'Japanese',
    'zh-TW': 'Chinese, Taiwan',
    'ko': 'Korean, Korea'
}


locales = [
    "da", "de", "en-GB", "en-US", "es-ES", "fr", "hr", "it", "lt", "hu",
    "nl", "no", "pl", "pt-BR", "ro", "fi", "sv-SE", "vi", "tr", "cs",
    "el", "bg", "ru", "uk", "th", "zh-CN", "ja", "zh-TW", "ko"
]


m_numbers = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:"]

m_offsets = [
    (-1, -1), (0, -1), (1, -1),
    (-1, 0), (1, 0),
    (-1, 1), (0, 1), (1, 1)
]


conversion_code = {
    'A': 'Z', 'B': 'Y', 'C': 'X', 'D': 'W', 'E': 'V', 'F': 'U',
    'G': 'T', 'H': 'S', 'I': 'R', 'J': 'Q', 'K': 'P', 'L': 'O',
    'M': 'N', 'N': 'M', 'O': 'L', 'P': 'K', 'Q': 'J', 'R': 'I',
    'S': 'H', 'T': 'G', 'U': 'F', 'V': 'E', 'W': 'D', 'X': 'C',
    'Y': 'B', 'Z': 'A',
    'a': 'z', 'b': 'y', 'c': 'x', 'd': 'w', 'e': 'v', 'f': 'u',
    'g': 't', 'h': 's', 'i': 'r', 'j': 'q', 'k': 'p', 'l': 'o',
    'm': 'n', 'n': 'm', 'o': 'l', 'p': 'k', 'q': 'j', 'r': 'i',
    's': 'h', 't': 'g', 'u': 'F', 'v': 'e', 'w': 'd', 'x': 'c',
    'y': 'b', 'z': 'a'
}


def encode_string(text: str) -> str:
    converted_data = ""
    for i in range(0, len(text)):
        if text[i] in conversion_code.keys():
            converted_data += conversion_code[text[i]]
        else:
            converted_data += text[i]
    import base64
    decoded_stuff = base64.b64encode('{}'.format(converted_data).encode('ascii'))
    encoded_stuff = str(decoded_stuff)
    return encoded_stuff[2:len(encoded_stuff)-1]


def decode_string(text: str) -> str:
    import codecs
    strOne = (text).encode("ascii")
    pad = len(strOne) % 4
    strOne += b"=" * pad
    encoded_stuff = codecs.decode(strOne.strip(), 'base64')
    decoded_stuff = str(encoded_stuff)
    decoded_stuff = decoded_stuff[2:len(decoded_stuff)-1]
    
    converted_data = ""
    for i in range(0, len(decoded_stuff)):
        if decoded_stuff[i] in conversion_code.keys():
            converted_data += conversion_code[decoded_stuff[i]]
        else:
            converted_data += decoded_stuff[i]
    return converted_data
