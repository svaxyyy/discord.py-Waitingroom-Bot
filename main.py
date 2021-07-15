
import discord

from discord.ext import commands
import json
import asyncio


from discord_components import DiscordComponents, Button, Select, SelectOption, component

from discord_components import *


from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio



intents = discord.Intents.default()
intents.members = True




# json


def load():
    with open("database/json/bot_config.json", "r") as file:
        return json.load(file)


data = load()

client = client.Bot(command_prefix=data["prefix"], intents=intents)
client.remove_command("help")

ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
}

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)

# app code


@client.event
async def on_ready():
    DiscordComponents(client)
    print('We have logged in as {0.user}'.format(client))





        


@client.command()
async def setup(ctx):
    with open("database/json/waitingroom_configs.json", "r") as file:
        setupdata = json.load(file)
        
    if not ctx.guild.id in setupdata:
        setupdata = {}
        setupdata["guild-id"] = int(ctx.guild.id)
        setupdata["channel-ids"] = 0
    b1_botvc = Button(style=ButtonStyle.green, label="I Joined it")
    msg = await ctx.send("Join the Voicechannel where the bot should stay in!", components=[b1_botvc])
    res = await client.wait_for("button_click")
    if (res.component.label) == "I Joined it":
        if (ctx.author.voice):
            setupdata["channel-ids"] = int(ctx.author.voice.channel.id)
            await ctx.send("Finished the Setup")
            await msg.edit(components=[])
            await msg.add_reaction("✅")
            await res.respond(type=6)
        else:
            await ctx.send("Setup failed! You are not in a Voicechannel please do the setup again.")
            await msg.edit(components=[])
            await msg.add_reaction("❌")
            await res.respond(type=6)
    with open("database/json/waitingroom_configs.json", "w") as file:
        json.dump(setupdata, file)
            
        
@client.command(aliases=["menu"])
async def help(ctx):
    b1_setup = Button(style=ButtonStyle.blue, label="Setup", emoji="💻")
    b2_start = Button(style=ButtonStyle.green, label="Start", emoji="💽")
    b3_disconnect = Button(style=ButtonStyle.red, label="Disconnect", emoji="🔌")
    embed = discord.Embed(color=0x4e4040, title=f"Menu for Waitingroom",
                           description=f"> ***Prefix*** : `{data['prefix']}`")
    embed.add_field(name=f"`help` or `menu`", value=f"Shows all commands and aliases.", inline=False)
    embed.add_field(name=f"`setup`", value=f"Configure the Waitingroom.", inline=False)
    embed.add_field(name=f"`start` or `join`", value=f"The Bot will connect to the Waitingroom.", inline=False)
    embed.add_field(name=f"`disconnect` or `leave`", value=f"Disconnect the Bot from the Waitingroom.", inline=False)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
    msg = await ctx.send(embed=embed, components=[b1_setup, b2_start, b3_disconnect])
    loop= True
    while loop:
        try:
            res = await client.wait_for("button_click")#
    
        except asyncio.TimeoutError:
            await ctx.send("Timeout Error!")
        else:
            if res.component.label == "Setup":
                await res.respond(type=6)
                await ctx.invoke(setup)


            if res.component.label == "Start":
                await res.respond(type=6)
                await ctx.invoke(start)


            
            if res.component.label == "Disconnect":
                if (res.voice_client):
                    await res.guild.voice_client.disconnect()
                else:
                    await res.channel.send("I am not in a Voice Channel!")
                    await res.respond(type=6)


            else:
                print("Mhhh! Something went wrong! (help command)")
        



@client.command(aliases=['join'])
async def start(ctx):
    with open("database/json/waitingroom_configs.json", "r") as file:
        setupdata = json.load(file)

    songLoop = True
    while songLoop:
        channel = client.get_channel(setupdata["channel-ids"])
        voice = await channel.connect()
        source= FFmpegPCMAudio("song.mp3")
        voice.play(source)
    else:
        await ctx.send("You are not in a Voice Channel! Join a Voice channel to run this Command")



    


@client.command(aliases=['leave'])
async def disconnect(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()


client.run(data["token"])
