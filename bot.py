from discord import channel, user
from discord.utils import get
from discord.ext import commands
import numpy as np
import discord
from datetime import datetime
import string
import os
import requests
import json # json to dict conversion
import random # for random post

#reddit image load
from PIL import Image
import requests
from io import BytesIO
import asyncio #asynchronous execution


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

async def schedule_task(interval : float, func, *args):
    max_t = 5
    t = 0
    while True:
        await func(*args)
        t += 1
        await asyncio.sleep(interval * 60)
        if t >= max_t: break
    print('schedule completed')

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

async def search_image(channel, author, query : string):
    print('test')
    image_search_url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/ImageSearchAPI"
    image_querystring = {"q":query,"pageNumber":"1","pageSize":"50","autoCorrect":"true"}
    headers = {
        'x-rapidapi-host': "contextualwebsearch-websearch-v1.p.rapidapi.com",
        'x-rapidapi-key': "7195268bd9msheb62269ccbb1c4dp1d8749jsn9d22b0c89a23"
    }
    response = requests.request("GET", image_search_url, headers=headers, params=image_querystring) # send query
    print(json.loads(response.text))
    return response.text

def filter_today_reddit_post(posts):
    utc_now = datetime.utcnow()
    todays = []
    for post in posts:
        data = post['data']
        #print(post.keys())
        #print(post['data'].keys())
        time_posted_utc = datetime.utcfromtimestamp(data['created_utc'])

        delta = utc_now - time_posted_utc
        if delta.days <= 0:
            todays.append(post)
    return todays

async def Trial_Func(channel, author, t : str):
    print(t)

async def GetRedditTodaysTop(channel : discord.channel, author : discord.member, subreddit : str):
    response = requests.request('GET', f"https://www.reddit.com/r/{subreddit}/.json?limit=50", headers= {'User-agent' : 'mathmeme bot v0.01'})
    print(f'Get Subreddit r/{subreddit} top posts today')
    data = json.loads(response.text)
    posts = data['data']['children']

    todays = filter_today_reddit_post(posts)
    post = random.choice(todays)
    # print(post['data'].keys())
    # print(post['data'])
    is_video = post['data']['is_video']
    # print('Video? ', post['data']['is_video'])
    if ('url_overridden_by_dest' in post['data'].keys()) and (not is_video):
        print(post['data']['url_overridden_by_dest'])
        end = post['data']['url_overridden_by_dest'].split('.')[3]

        # print('media' in post['data'])
        #print(post['data']['secure_media'])
        content = requests.get(post['data']['url_overridden_by_dest'], headers = {'User-agent' : 'mathmeme bot v0.01'}).content
        await channel.send(post['data']['title'])
        await channel.send(file = discord.File(BytesIO(content), f'meme.{end}'))
    
    if is_video:
        #print(post['data']['secure_media'].keys())
        #print(post['data']['secure_media']['reddit_video'].keys())
        content = requests.get(post['data']['secure_media']['reddit_video']['fallback_url'], headers = {'User-agent' : 'mathmeme bot v0.01'}).content
        await channel.send(post['data']['title'])
        await channel.send(file = discord.File(BytesIO(content), 'meme.mp4'))

async def GetRedditTop(channel : discord.channel, author, subreddit : str):
    response = requests.request('GET', "https://www.reddit.com/r/mathmemes/.json?limit=10", headers= {'User-agent' : 'mathmeme bot v0.01'})
    # print(f'Get Subreddit r/{subreddit} top posts')
    data = json.loads(response.text)
    posts = data['data']['children']
    #print(data)
    #print(data.keys())
    #print(data['data']['children'][1]['data'])
    #print(data['data']['children'][1]['data']['url_overridden_by_dest'])
    content = requests.get(data['data']['children'][1]['data']['url_overridden_by_dest'], headers={'User-agent' : 'mathmeme bot v0.01'}).content
    # image = Image.open(BytesIO(content))
    await channel.send(file = discord.File(BytesIO(content), 'meme.png'))


async def ScheduleTask(channel : discord.channel, author, command : str, interval : str, *args):
    await schedule_task(float(interval), COMMANDS[command], *(channel, author, *args))
    pass

COMMAND_PREFIX = '!'
COMMANDS = {
    'image' : search_image,
    'test' : Trial_Func,
    #'redditt' : GetRedditTop,
    'reddit' : GetRedditTodaysTop,
    'schedule' : ScheduleTask
}

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
    # await client.change_presence(activity = discord.Activity(type = discord.ActivityType.custom, name = 'Looking for tiktok links'))
    await client.change_presence(activity=discord.Game(name = 'TikTok link lookout'))
    print('completed')

@client.event
async def on_message(message : discord.Message):
    if message.author == client.user: return #we don't want to check our own message

    author = message.author
    chn = message.channel
    print("msg: ", message.content)
    content = str(message.content)
    norm_content = content.lower() #it's string
    #for x in GREETINGS:
    #    if x in norm_content:
    #        await chn.send(f"{x.capitalize()} {author.display_name}!")
    #        break
    if norm_content.startswith(COMMAND_PREFIX):
        splitted = norm_content[1:].split()
        await COMMANDS[splitted[0]](chn, author, *splitted[1:])

    
    if inHated(norm_content):
        await chn.send(f"TIKTOK NOT ALLOWED {author.mention}! Go to the corner!")
        await chn.send(f"{author.mention} You're a retard!", tts = True)
        if get(author.guild.roles, name = 'Retard') is not None:
            await author.add_roles(get(author.guild.roles, name = 'Retard'))
        await message.delete()
        
    #if message.content.startswith("hello"):
    #    await message.channel.send("Hello!!!")

@client.event
async def on_typing(channel : discord.channel, user : discord.member, when):
    print(f"Time = {when}; User {user} is typing in channel {channel}")

@client.event
async def on_group_join(channel : discord.channel, user : discord.member): # Doesn't actually detect voice channel join
    print(f"User {user}, joined channel {channel}")

@client.event
async def on_voice_state_update(member : discord.member, before : discord.VoiceState, after : discord.VoiceState):
    # called when someone connects/disconnects to voice channel
    # member is the user that did the change
    # before, after are the voice channel states
    print(f"voice state changed by member {member.display_name}")
    if (before.channel is None) and (after.channel is not None):
        print(f'{member.display_name} joined channel {after.channel.name}')
    if (after.channel is None) and (before.channel is not None):
        print(f'{member.display_name} left channel {before.channel.name}')

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