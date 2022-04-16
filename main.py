import os
from random import random
from wsgiref.simple_server import server_version
from discord.ext import commands
import discord
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TOKEN')
client = discord.Client()
server_name = os.getenv("SERVER_NAME")
bot = commands.Bot(command_prefix='\\', help_command=None)
print("Connecting to", server_name + "...")


@bot.command(name='help')
async def help(ctx):
    await ctx.send("Aiuto!")


@client.event
async def on_ready():
    print(f'{client.user} connected!')


@client.event
async def on_message(msg):
    if msg.author == client.user:
        return
    if isinstance(msg.channel, discord.channel.DMChannel):
        if msg.content.startswith('.anon'):
            try:
                gender = msg.content.split(" ")[1].lower()
                if gender != 'm' and gender != 'f':
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

            target_channel = msg.channel
            for server in client.guilds:
                if server.name == server_name:
                    for channel in server.channels:
                        if channel.name == os.getenv("TARGET_CHANNEL"):
                            target_channel = channel
                            break
            embed = discord.Embed(
                title=genere, description="{} anni".format(eta), color=0xd43008)
            embed.set_author(name="InSegreto-Bot", url="https://discordapp.com/users/718914869709242448 ",
                             icon_url="https://cdn.discordapp.com/avatars/964799440282087424/bb34795239dbf80a2aab6cb99d9255f3.webp?size=80 ")
            embed.set_thumbnail(
                url="https://media.istockphoto.com/illustrations/top-secret-rubber-stamp-illustration-id504757412?k=20&m=504757412&s=170667a&w=0&h=TZF0bkIu7erwjTKCO72mfwg5Eiw9rRb-gScHY-heT3c=")
            embed.add_field(name="Scrive:", value="***{}***".format(
                messaggio), inline=False)
            embed.set_footer(text="Italy-Empire")
            await target_channel.send(embed=embed)
        else:
            await msg.channel.send(
                "**Ciao! Digita** `.anon <genere> <età> <messaggio>` **per inviare un messaggio anonimo nel canale del server Discord!**")


client.run(token)