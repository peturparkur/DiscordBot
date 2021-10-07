from discord import channel, user
from discord.utils import get
import numpy as np
import discord
import datetime
import string
import os

# permission=8 is admin
# invitation link: https://discord.com/api/oauth2/authorize?client_id=895705102231412776&permissions=469776384&scope=bot - No Cancer
# Check javascript implementation: https://discordjs.guide/

#print(os.getcwd())
#print(os.path.dirname(__file__)) #current directory of script
os.chdir(os.path.dirname(__file__)) ## change working directory to the scripts directory

TOKEN = ""
# We read the token locally as don't want to share on github
with open ("./token2.txt", "r") as f:
    TOKEN = f.read()

#print(TOKEN)

#Get NLP greetings
GREETINGS = ["hi",
            "hello",
            "hey",
            "greetings",
            "good to see you",
            "nice to see you",
            "how you doing",
            "good day",
            "good morning",
            "good afternoon",
            "good evening",
            "good night",
            "yolo"
]

HATED_URL = [
    'https://www.tiktok.com/',
    'https://vm.tiktok.com/'
]

client = discord.Client()

def isTikTok(msg : str):
    if 'https://www.tiktok.com/' in msg: return True
    if 'https://vm.tiktok.com/' in msg: return True
    return False

def inHated(msg : str):
    for x in HATED_URL:
        if x in msg: return True
    return False

@client.event
async def on_ready():
    print(f"We have logged in as {client}")

@client.event
async def on_message(message : discord.Message):
    if message.author == client.user: return #we don't want to check our own message

    author = message.author
    chn = message.channel
    print("msg: ", message.content)
    content = str(message.content)
    norm_content = content.lower() #it's string
    for x in GREETINGS:
        if x in norm_content:
            await chn.send(f"{x.capitalize()} {author.display_name}!")
            break
    
    if inHated(norm_content):
        await chn.send(f"TIKTOK NOT ALLOWED {author.mention}! Go to the corner!")
        await author.add_roles(get(author.guild.roles, name = 'Retard'))
        await message.delete()
        
    #if message.content.startswith("hello"):
    #    await message.channel.send("Hello!!!")

@client.event
async def on_typing(channel, user, when):
    print(f"Time = {when}; User {user} is typing in channel {channel}")

@client.event
async def on_group_join(channel, user): # Doesn't actually detect voice channel join
    print(f"User {user}, joined channel {channel}")

@client.event
async def on_voice_state_update(member, before, after):
    # called when someone connects/disconnects to voice channel
    # member is the user that did the change
    # before, after are the voice channel states
    print(f"voice state changed by member {member.display_name}")

@client.event
async def on_user_update(before, after):
    # called when user updates their profile eg.: avatar, username
    # https://discordpy.readthedocs.io/en/stable/api.html#discord.User
    print(f"user {before.name} has changed their profile")

@client.event
async def on_member_update(before, after):
    # Called when a server user ("Member") changed state
    # eg.: status, activity, nickname, roles, pending
    pass

client.run(TOKEN)