import discord
import praw
import random
import requests
import urllib
import urllib.request
import binaryalphabet as ba
import textwrap as tw

client = discord.Client()
reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=CLIENT_USER)

prefix = ",,"
ownerId = '<@111111111111111111>'
    
def gif(kind, source):
    urls = []
    for submission in reddit.subreddit(kind).hot(limit=100):
        if source in submission.url:
            urls.append(submission.url)
    gif = urls[random.randint(0, len(urls)-1)]
    return gif

def getDadJoke():
    posts = []
    count = 0
    for submission in reddit.subreddit('dadjokes').hot(limit=100):
        posts.append(f"{submission.title}\n{submission.selftext}")
    post = posts[random.randint(0, len(posts)-1)]
    return post

def getYouTubeVideo(query):
    query = query.replace(" ", "+")
    apiKey = API_KEY
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&key={apiKey}"
    r = requests.get(url)
    data = r.json()
    videoUrl = f'https://www.youtube.com/watch?v={data["items"][0]["id"]["videoId"]}'
    return videoUrl
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(f'{prefix}help'):  
        msg = '\
**Commands:**\n\
`help` show this\n\
`owner` show bot owner\n\
`invite` invite link\n\
`youtube [search]` get youtube video\n\
`catgif` random cat gif\n\
`coolgif` random cool gif\n\
`satisfyinggif` random oddly satisfying gif\n\
`avatar [user]` get avatar of user\n\
`dadjoke` random dad joke\n\
`circ [message]` display message in circle emojis\n\
`big [message]` display message in big font\n\
`mock [message]` display message in mock format'\
.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith(f'{prefix}owner'):
        msg = f'{ownerId} is my owner!'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith(f'{prefix}catgif'):
        msg = f'{gif("StartledCats", "i.imgur")}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith(f'{prefix}coolgif'):
        msg = f'{gif("mesmerizinggifs", "i.imgur")}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith(f'{prefix}satisfyinggif'):
        msg = f'{gif("oddlysatisfying", "i.imgur")}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith(f'{prefix}invite'):
        msg = "https://discordapp.com/oauth2/authorize?client_id=513850602451894272&scope=bot&permissions=8".format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith(f'{prefix}yt '):
        query = message.content[len(prefix)+3:]
        msg = f'{getYouTubeVideo(query)}'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith(f'{prefix}avatar '):
        for user in message.mentions:
            msg = f"{user.avatar_url}"
        await client.send_message(message.channel, msg)

    if message.content.lower() == (f'haha yes'):
        msg = f"https://i.imgur.com/5YKHW2F.jpg"
        await client.send_message(message.channel, msg)

    if message.content.startswith(f'{prefix}dadjoke'):
        msg = f"{getDadJoke()}"
        await client.send_message(message.channel, msg)

    if message.content.startswith(f'{prefix}circ '):
        text = message.content[len(prefix)+5:]
        if len(text.replace(" ", "")) > 6:
            msg = "Only 6 letters at a time!"
        else:
            circletext = ba.circleText(text, ":red_circle:", ":black_circle:")
            msg = ""
            for item in circletext:
                msg = f"{msg}{item}\n"
        await client.send_message(message.channel, msg)

    if message.content.startswith(f'{prefix}big '):
        text = message.content[len(prefix)+4:].lower().replace(" ", "   ")
        msg = ""
        alphabet = []
        for i in range(26):
            alphabet.append(chr(ord('a') + i))
        for char in text:
            if char in alphabet:
                msg = f"{msg}:regional_indicator_{char}:"
            else:
                msg = f"{msg}{char}"
        await client.send_message(message.channel, msg)

    if message.content.startswith(f'{prefix}mock '):
        msg = message.content[len(prefix)+5:]
        newstr = ""
        for i in range(len(msg)):
            if i % 2 == 0:
                newstr = f"{newstr}{(msg[i].upper())}"
            else:
                newstr = f"{newstr}{(msg[i].lower())}" 
        newstr = f"{newstr} <:mock:486929533652566029>"
        await client.send_message(message.channel, newstr)

@client.event
async def on_member_update(before, after):
    if(before.server.id == "111111111111111111"):
        if str(after.status) == "offline":
            msg = f"{after.display_name} is {after.status}. :red_circle:"
        elif str(after.status) == "online":
            msg = f"{after.display_name} is {after.status}. :evergreen_tree:"
        else:
            msg = f"{after.display_name} is {after.status}. :small_orange_diamond:"
        await client.send_message(discord.Object(id='11111111111111111'), msg)

@client.event
async def on_ready():    
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name=f'{prefix}help | {prefix}owner'))
    msg = f"**--- {client.user.name} is online ---**"
    await client.send_message(discord.Object(id='111111111111111111'), msg)

token = TOKEN
client.run(token)
