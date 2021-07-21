from discord import channel, user
import numpy as np
import discord
import datetime
import string
import os

#print(os.getcwd())
#print(os.path.dirname(__file__)) #current directory of script
os.chdir(os.path.dirname(__file__)) ## change working directory to the scripts directory

TOKEN = ""
# We read the token locally as don't want to share on github
with open ("./token.txt", "r") as f:
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

client = discord.Client()

@client.event
async def on_ready():
    print(f"We have logged in as {client}")

@client.event
async def on_message(message):
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
        
    #if message.content.startswith("hello"):
    #    await message.channel.send("Hello!!!")

@client.event
async def on_typing(channel, user, when):
    print(f"Time = {when}; User {user} is typing in channel {channel}")

@client.event
async def on_group_join(channel, user):
    print(f"User {user}, joined channel {channel}")

client.run(TOKEN)