
import discord
from discord import voice_client
from discord.embeds import Embed
from discord.ext import commands
import json
import asyncio
from discord_components import DiscordComponents, Button, Select, SelectOption, Component
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
    
    print('We have logged in as {0.user}'.format(client))
    DiscordComponents(client)





        


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
    with open("database/json/waitingroom_configs.json", "r") as file:
        setupdata = json.load(file)
    b1_setup = Button(style=ButtonStyle.blue, label="Setup", emoji="💻")
    b2_start = Button(style=ButtonStyle.green, label="join", emoji="💽") # not in use pls ignore
    b3_disconnect = Button(style=ButtonStyle.red, label="Disconnect", emoji="🔌")
    b4_radio_stop = Button(style=ButtonStyle.grey, label="Stop the Radio", emoji="📻")
    b5_radio_start = Button(style=ButtonStyle.green, label="Start the Radio",emoji="📻")
    embed = discord.Embed(color=0x4e4040, title=f"Menu for Waitingroom",
                           description=f"> ***Prefix*** : `{data['prefix']}`")
    embed.add_field(name=f"`help` or `menu`", value=f"Shows all commands and aliases.", inline=False)
    embed.add_field(name=f"`setup`", value=f"Configure the Waitingroom (as often as you want).", inline=False)
    embed.add_field(name=f"`start` or `join`", value=f"The Bot will connect to the Waitingroom and play his custom mp3 file.", inline=False)
    embed.add_field(name=f"`radio`", value=f"The Bot will connect to the Waitingroom and play Radio.", inline=False)
    embed.add_field(name=f"`stop`", value=f"The Bot stop the Radio.", inline=False)
    embed.add_field(name=f"`disconnect` or `leave`", value=f"Disconnect the Bot from the Waitingroom.", inline=False)
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.set_footer(text=ctx.guild.name, icon_url=ctx.guild.icon_url)
    msg = await ctx.send(embed=embed, components=[b1_setup,b3_disconnect, b4_radio_stop, b5_radio_start])
    loop= True
    while loop:
        res = await client.wait_for("button_click")
        if res.component.label == "Setup":
            await res.respond(
                type=7,
                components = []
                )
            await ctx.invoke(setup)


        if res.component.label == "Disconnect":
            embed = Embed(title="Disconnect🔌", description=f"Please use the " + data["prefix"] + "`disconnect` command instead!")
            await res.respond(
                type=7,
                components = []
                )
            await res.channel.send(embed=embed)

            
        if res.component.label == "Radio":
            await res.respond(
                type=7,
                components = []
                )
            await ctx.invoke(start)
            
        if res.component.label == "Stop the Radio":
            await res.respond(
                type=7,
                components = []
            )
            await ctx.invoke(stop)
        if res.component.label == "Start the Radio":
            await res.respond(
                type=7,
                components = []
            )
            await ctx.invoke(radio)
                    

                    
                # do join, disconnect, radio and mp3





@client.command()
async def start(ctx):
    with open("database/json/waitingroom_configs.json", "r") as file:
        setupdata = json.load(file)

    songLoop = True
    while songLoop:
        global player1
        channel = client.get_channel(setupdata["channel-ids"])
        player1 = await channel.connect()
        player1.play(FFmpegPCMAudio("song.mp3"))
    else:
        await ctx.send("You are not in a Voice Channel! Join a Voice channel to run this Command")


@client.command()
async def radio(ctx, url: str = ''):
    with open("database/json/waitingroom_configs.json", "r") as file:
        setupdata = json.load(file)

    radios = [
        {"radiourl" : "https://streams.ilovemusic.de/iloveradio109.mp3", "type" : "Hits 2021"},
        {"radiourl" : "https://streams.ilovemusic.de/iloveradio17.mp3", "type" : "Chillhop"},
        {"radiourl" : "https://streams.ilovemusic.de/iloveradio13.mp3", "type" : "US Rap only"}]

    em = Embed(title="Radio📻", description="Choose the Radio you want to listen!")
    em1 = Embed(title="Hits 2021", description="You are now listening to the Hits of 2021")
    em2 = Embed(title="US Rap only", description="You are now listening to US Rap only")
    em3 = Embed(title="Chillhop", description="You are now listening to Chillhop radio")

    await ctx.send(embed=em,
    components=[Select(placeholder="Choose your Radio!", options=[
        SelectOption(
            label="Hits 2021",
            value="Listen to the Hits of 2021.",
            description="Listen to the Hits of 2021!",
            emoji="🥳"
        ),
        SelectOption(
            label="US Rap only",
            value="Listen to a Radio which is plaing US Rap only.",
            description="Listen to a Radio which is plaing US Rap only!",
            emoji="🎵"
        ),
        SelectOption(
            label="Chillhop",
            value="Listen to the Chillhop Radio.",
            description="Listen to the Chillhop Radio!",
            emoji="💫"
        )
    ])])
    while True:
        try:
            res = await client.wait_for("select_option")

            label = res.component[0].label

            if label == "Hits 2021":
                await res.respond(
                    type=InteractionType.ChannelMessageWithSource,
                    ephemeral=False,
                    embed=em1
                )
                channel = client.get_channel(setupdata["channel-ids"])
                global player

                player = await channel.connect()

                player.play(FFmpegPCMAudio("https://streams.ilovemusic.de/iloveradio109.mp3"))
            
            if label == "US Rap only":
                await res.respond(
                    type=InteractionType.ChannelMessageWithSource,
                    ephemeral=False,
                    embed=em2
                )
            
                channel = client.get_channel(setupdata["channel-ids"])
                
                player = await channel.connect()

                player.play(FFmpegPCMAudio('https://streams.ilovemusic.de/iloveradio13.mp3'))

            if label == "Chillhop":
                await res.respond(
                    type=InteractionType.ChannelMessageWithSource,
                    ephemeral=False,
                    embed=em3
                )

                channel = client.get_channel(setupdata["channel-ids"])
                
                player = await channel.connect()

                player.play(FFmpegPCMAudio('https://streams.ilovemusic.de/iloveradio17.mp3'))
        
        except discord.NotFound:
            print("error!")



@client.command()
async def stop(ctx):
    try:
        player.stop()
        await ctx.send("Stopped the Radio!")
        
    except commands.CommandInvokeError:
        await ctx.send("Wasnt able to stop the Radio")


    


@client.command(aliases=['leave'])
async def disconnect(ctx):
    await ctx.guild.voice_client.disconnect()


client.run(data["token"])


# Contact Svaxyy#0859 if there are any issues! This Waitingroom Bot was for testing!
