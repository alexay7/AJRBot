"""Main file"""

import os
import json
import discord
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True
djtbot = commands.Bot(command_prefix='.', intents=intents, help_command=None)
client = discord.Client()

with open("cogs/myguild.json") as json_file:
    data_dict = json.load(json_file)
    trusted_server_ids = data_dict["trusted_server_ids"]


@djtbot.event
async def on_message(message):
    """Activates when message detected"""
    if(len(message.content) > 0):
        if(message.content[0] == "$"):
            channel = message.channel
            await channel.send("Ahora mis comandos empiezan por .", delete_after=10.0)
    for cog in djtbot.cogs:
        cog = djtbot.get_cog(cog)
        try:
            await cog.searchAnilist(message)
        except AttributeError:
            continue
    await djtbot.process_commands(message)


@djtbot.check
def check_guild(ctx):
    """Checks if the guild is allowed to run the bot"""
    try:
        return ctx.guild.id in trusted_server_ids
    except AttributeError:
        return True


# def connect_db():
#     try:
#         client = MongoClient(os.getenv("MONGOURL"),
#                              serverSelectionTimeoutMS=10000)
#         client.server_info()
#         return client
#     except errors.ServerSelectionTimeoutError:
#         print("Ha ocurrido un error intentando conectar con la base de datos.")
#         exit(1)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and not filename.startswith("nocog"):
        print(filename)
        djtbot.load_extension(f'cogs.{filename[:-3]}')
        print(f"Loaded cog {filename}")

djtbot.run(os.getenv("BOT_TOKEN"))
