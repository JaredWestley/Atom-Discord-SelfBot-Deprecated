import sys
import json as jsond
import requests
import binascii
from uuid import uuid4
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad
import platform
import os
import time
from colorama import Fore

if platform.system() == "Windows":
    KEYSAVE_PATH = "C:\\ProgramData\\AtomSBkeysave.txt"
else:
    KEYSAVE_PATH = "/usr/AtomSBkeysave.txt"


class user_data_class:
    key = ""
    expiry = None
    level = 0


class KeyAuthAPI:
    name = ownerid = secret = version = ""
    
    def __init__(self, name, ownerid, secret, version):
        self.name = name
        self.ownerid = ownerid
        self.secret = secret
        self.version = version
        self.session_id = ""
        self.session_iv = ""
        self.user_data = user_data_class()
        
    def init(self):
        print(f"{Fore.YELLOW}Initializing KeyAuth...{Fore.RESET}")
        try:
            self.session_iv = str(uuid4())[:8]
            init_iv = SHA256.new(self.session_iv.encode()).hexdigest()
            
            post_data = {
                "type": binascii.hexlify(("init").encode()),
                "ver": self.encrypt(self.version, self.secret, init_iv),
                "name": binascii.hexlify(self.name.encode()),
                "ownerid": binascii.hexlify(self.ownerid.encode()),
                "init_iv": init_iv
            }
            
            response = self.do_request(post_data)
            
            if response == "program_doesnt_exist":
                print("The application doesnt exist")
                sys.exit()
                
            response = self.decrypt(response, self.secret, init_iv)
            
            json_data = jsond.loads(response)
            
            if not json_data["success"]:
                print(json_data["message"])
                sys.exit()
        except Exception as e:
            print(f"{Fore.YELLOW}This was the old implementation of auth, it has since been deprecated and no longer works.")
            print(f"Skipping KeyAuth initialization...{Fore.RESET}")
            time.sleep(3)
            
    def register(self, user, password, license_key, hwid=None):
        if hwid is None:
            hwid = get_hwid()
        
        self.session_iv = str(uuid4())[:8]
        init_iv = SHA256.new(self.session_iv.encode()).hexdigest()
        
        post_data = {
            "type": binascii.hexlify(("register").encode()),
            "username": self.encrypt(user, self.secret, init_iv),
            "pass": self.encrypt(password, self.secret, init_iv),
            "key": self.encrypt(license_key, self.secret, init_iv),
            "hwid": self.encrypt(hwid, self.secret, init_iv),
            "name": binascii.hexlify(self.name.encode()),
            "ownerid": binascii.hexlify(self.ownerid.encode()),
            "init_iv": init_iv
        }
        
        response = self.do_request(post_data)
        response = self.decrypt(response, self.secret, init_iv)
        
        json_data = jsond.loads(response)
        
        if json_data["success"]:
            print("successfully registered")
        else:
            print(json_data["message"])
            sys.exit()
            
    def upgrade(self, user, license_key):
        self.session_iv = str(uuid4())[:8]
        init_iv = SHA256.new(self.session_iv.encode()).hexdigest()
        
        post_data = {
            "type": binascii.hexlify(("upgrade").encode()),
            "username": self.encrypt(user, self.secret, init_iv),
            "key": self.encrypt(license_key, self.secret, init_iv),
            "name": binascii.hexlify(self.name.encode()),
            "ownerid": binascii.hexlify(self.ownerid.encode()),
            "init_iv": init_iv
        }
        
        response = self.do_request(post_data)
        response = self.decrypt(response, self.secret, init_iv)
        
        json_data = jsond.loads(response)
        
        if json_data["success"]:
            print("successfully upgraded user")
        else:
            print(json_data["message"])
            sys.exit()
            
    def login(self, user, password, hwid=None):
        if hwid is None:
            hwid = get_hwid()
        
        self.session_iv = str(uuid4())[:8]
        init_iv = SHA256.new(self.session_iv.encode()).hexdigest()
        
        post_data = {
            "type": binascii.hexlify(("login").encode()),
            "username": self.encrypt(user, self.secret, init_iv),
            "pass": self.encrypt(password, self.secret, init_iv),
            "hwid": self.encrypt(hwid, self.secret, init_iv),
            "name": binascii.hexlify(self.name.encode()),
            "ownerid": binascii.hexlify(self.ownerid.encode()),
            "init_iv": init_iv
        }
        
        response = self.do_request(post_data)
        response = self.decrypt(response, self.secret, init_iv)
        
        json_data = jsond.loads(response)
        
        if json_data["success"]:
            print("successfully logged in")
        else:
            print(json_data["message"])
            sys.exit()
            
    def license(self, key, hwid=None):
        if hwid is None:
            hwid = get_hwid()
        
        self.session_iv = str(uuid4())[:8]
        init_iv = SHA256.new(self.session_iv.encode()).hexdigest()
        
        post_data = {
            "type": binascii.hexlify(("license").encode()),
            "key": self.encrypt(key, self.secret, init_iv),
            "hwid": self.encrypt(hwid, self.secret, init_iv),
            "name": binascii.hexlify(self.name.encode()),
            "ownerid": binascii.hexlify(self.ownerid.encode()),
            "init_iv": init_iv
        }
        
        response = self.do_request(post_data)
        response = self.decrypt(response, self.secret, init_iv)
        
        json_data = jsond.loads(response)
        
        if json_data["success"]:
            self.load_user_data(json_data["info"])
            print("successfully logged into license")
        else:
            print(json_data["message"])
            if os.path.exists(KEYSAVE_PATH):
                os.remove(KEYSAVE_PATH)
                import time
                time.sleep(5)
            sys.exit()
            
    def var(self, name, hwid=None):
        if hwid is None:
            hwid = get_hwid()
        
        self.session_iv = str(uuid4())[:8]
        init_iv = SHA256.new(self.session_iv.encode()).hexdigest()
        
        post_data = {
            "type": binascii.hexlify(("var").encode()),
            "key": self.encrypt(self.user_data.key, self.secret, init_iv),
            "varid": self.encrypt(name, self.secret, init_iv),
            "hwid": self.encrypt(hwid, self.secret, init_iv),
            "name": binascii.hexlify(self.name.encode()),
            "ownerid": binascii.hexlify(self.ownerid.encode()),
            "init_iv": init_iv
        }
        
        response = self.do_request(post_data)
        response = self.decrypt(response, self.secret, init_iv)
        
        json_data = jsond.loads(response)
        
        if json_data["success"]:
            return json_data["response"]
        else:
            print(json_data["message"])
            import time
            time.sleep(5)
            sys.exit()
            
    def do_request(self, post_data):
        headers = {"User-Agent": "KeyAuth"}
        try:
            rq_out = requests.post(
                "https://keyauth.com/api/v7/", 
                data=post_data, 
                headers=headers, 
                verify=False  # SSL verification disabled
            )
            return rq_out.text
        except Exception as e:
            return ""
            
    def load_user_data(self, data):
        self.user_data.key = data["key"]
        self.user_data.expiry = data["expiry"]
        self.user_data.level = data["level"]
        
    def encrypt(self, message, enc_key, iv):
        try:
            _key = SHA256.new(enc_key.encode()).hexdigest()[:32]
            _iv = SHA256.new(iv.encode()).hexdigest()[:16]
            return self.encrypt_string(message.encode(), _key.encode(), _iv.encode()).decode()
        except:
            print("Invalid Application Information")
            sys.exit()
            
    def decrypt(self, message, enc_key, iv):
        try:
            _key = SHA256.new(enc_key.encode()).hexdigest()[:32]
            _iv = SHA256.new(iv.encode()).hexdigest()[:16]
            return self.decrypt_string(message.encode(), _key.encode(), _iv.encode()).decode()
        except:
            print("Invalid Application Information")
            sys.exit()
            
    def encrypt_string(self, plain_text, key, iv):
        plain_text = pad(plain_text, 16)
        aes_instance = AES.new(key, AES.MODE_CBC, iv)
        raw_out = aes_instance.encrypt(plain_text)
        return binascii.hexlify(raw_out)
        
    def decrypt_string(self, cipher_text, key, iv):
        cipher_text = binascii.unhexlify(cipher_text)
        aes_instance = AES.new(key, AES.MODE_CBC, iv)
        cipher_text = aes_instance.decrypt(cipher_text)
        return unpad(cipher_text, 16)


def get_hwid():
    import subprocess
    import platform
    if platform.system() != "Windows":
        return "None"
    cmd = subprocess.Popen("wmic useraccount where name='%username%' get sid", stdout=subprocess.PIPE, shell=True)
    (suppost_sid, error) = cmd.communicate()
    suppost_sid = suppost_sid.split(b'\n')[1].strip()
    return suppost_sid.decode()


keyauthapp = KeyAuthAPI("add-your-own-app-name", "add-your-own-owner-id", "add-your-own-api-key", "add-your-own-version")
