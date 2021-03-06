import os
from pydoc import describe
from random import random
from secrets import choice
from tkinter import HIDDEN
from wsgiref.simple_server import server_version
from discord.ext import commands
import discord
from dotenv import load_dotenv
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
import time


load_dotenv()
token = os.getenv('TOKEN')
server_name = os.getenv("SERVER_NAME")
bot = commands.Bot(command_prefix="/")
slash = SlashCommand(bot, sync_commands=True)
print("Connecting to", server_name + "...")
guilds = []


@bot.event
async def on_ready():
    for server in bot.guilds:
        print(server.name, server.id)
        guilds.append(server.id)
    print(f'{bot.user} connected!')


@slash.slash(
    name="anon",
    description="/anon <genere> <età> <messaggio> per inviare un messaggio anonimo!",
    guild_ids=[389094224106225674],
    options=[
        create_option(
            name="genere",
            description="Genere",
            required=True,
            option_type=3,
            choices=[
                create_choice(
                    name="Indefinito",
                    value="i"
                ),
                create_choice(
                    name="Ragazzo",
                    value="m"
                ),
                create_choice(
                    name="Ragazza",
                    value="f"
                )

            ]
        ),
        create_option(
            name="age",
            description="Età",
            required=True,
            option_type=3
        ),
        create_option(
            name="messaggio",
            description="Messaggio da condividere",
            required=True,
            option_type=3
        )
    ]
)
async def _anon(ctx: SlashContext, genere: str, age: int, messaggio: str):

    if int(age) <= 10:
        await ctx.send(":x: **Età non valida!**", hidden=True)
        return 1
    if int(age) >= 100:
        await ctx.send(":x: **Età non valida!**", hidden=True)
        return 1

    banned = []
    with open("parolebandite.txt") as file:
        banned = [line.rstrip() for line in file]

    bwords = []
    isbanned = False
    for bword in banned:
        if bword in messaggio.lower():
            bwords.append(bword)
            isbanned = True

    if isbanned == True:
        await ctx.send(":warning: **ATTENZIONE!**", hidden=True)
        await ctx.send("`STAI USANDO PAROLE NON CONSENTITE:`", hidden=True)
        for bword in bwords:
            await ctx.send("`» {}`".format(bword), hidden=True)

        return 2

    await ctx.send(":white_check_mark: **OK! Invio il tuo messaggio...**", hidden=True)

    eta = int(age)
    if genere == 'm':
        genere = "Ragazzo 👨"
    elif genere == 'f':
        genere = "Ragazza 👧"
    elif genere == 'i':
        genere = "Indefinito 👌"

    target_channel = ctx.channel
    for server in bot.guilds:
        if server.name == server_name:
            for channel in server.channels:
                if channel.id == int(os.getenv("TARGET_CHANNEL")):
                    target_channel = channel
                    break

    embed = discord.Embed(
        title=genere, description="{} anni".format(eta), color=0xd43008)
    embed.set_author(name="InSegreto-Bot", url="https://discordapp.com/users/718914869709242448 ",
                     icon_url="https://cdn.discordapp.com/avatars/964799440282087424/bb34795239dbf80a2aab6cb99d9255f3.webp?size=80 ")
    embed.add_field(name="Scrive:", value="***{}***".format(
        messaggio), inline=False)
    embed.set_footer(text="Italian-Empire")
    await target_channel.send(embed=embed)


@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return

    if msg.channel.id == int(os.getenv("TARGET_CHANNEL")):
        if msg.author != bot.user:
            await msg.delete()

    if isinstance(msg.channel, discord.channel.DMChannel):
        if msg.content.startswith('.anon') or msg.content.startswith('/anon'):
            try:
                gender = msg.content.split(" ")[1].lower()
                if gender != 'm' and gender != 'f' and gender != 'i':
                    raise Exception("Genere non valido!")
            except:
                await msg.channel.send(":x: **Genere non valido!**")
                return 1

            try:
                age = msg.content.split(" ")[2]
                if age.isnumeric() == False:
                    raise Exception("Età non valida!")
                if int(age) <= 10:
                    raise Exception("Neonato alert")
                if int(age) >= 100:
                    raise Exception("EXTRABoomer alert")
            except:
                await msg.channel.send(":x: **Età non valida!**")
                return 1

            messaggio = msg.content.partition(" ")[2].partition(" ")[
                2].partition(" ")[2]

            banned = []
            with open("parolebandite.txt") as file:
                banned = [line.rstrip() for line in file]

            bwords = []
            isbanned = False
            for bword in banned:
                if bword in messaggio.lower():
                    bwords.append(bword)
                    isbanned = True

            if isbanned == True:
                await msg.channel.send(":warning: **ATTENZIONE!**")
                await msg.channel.send("`STAI USANDO PAROLE NON CONSENTITE:`")
                for bword in bwords:
                    await msg.channel.send("`» {}`".format(bword))

                return 2

            await msg.channel.send(":white_check_mark: **OK! Invio il tuo messaggio...**")

            genere = ""
            eta = int(age)
            if gender == 'm':
                genere = "Ragazzo 👨"
            elif gender == 'f':
                genere = "Ragazza 👧"
            elif gender == 'i':
                genere = "Indefinito 👌"

            target_channel = msg.channel
            for server in bot.guilds:
                if server.name == server_name:
                    for channel in server.channels:
                        if channel.id == int(os.getenv("TARGET_CHANNEL")):
                            target_channel = channel
                            break
            embed = discord.Embed(
                title=genere, description="{} anni".format(eta), color=0xd43008)
            embed.set_author(name="InSegreto-Bot", url="https://discordapp.com/users/718914869709242448 ",
                             icon_url="https://cdn.discordapp.com/avatars/964799440282087424/bb34795239dbf80a2aab6cb99d9255f3.webp?size=80 ")
            embed.add_field(name="Scrive:", value="***{}***".format(
                messaggio), inline=False)
            embed.set_footer(text="Italian-Empire")
            await target_channel.send(embed=embed)
        else:
            await msg.channel.send(
                "**Ciao! Digita** `.anon <genere> <età> <messaggio>` **per inviare un messaggio anonimo nel canale del server Discord!**")

bot.run(token)
