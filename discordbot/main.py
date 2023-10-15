import config
import os
import disnake
import json


from disnake.ext import commands
from modules import modals, rcon

intents = disnake.Intents.all()
client = commands.Bot(command_prefix=config.command_prefix, test_guilds=config.test_guilds, intents=intents)
client.modals = modals
client.rcon = rcon.Rcon(config.server_ip, config.server_port, config.rcon_password)

config.all_text = json.load(open(f"all_text.json", encoding='utf-8-sig'))

print('Loaded extensions:')
for files in os.listdir("./cogs"):
    if files.endswith(".py"):
        client.load_extension(f'cogs.{files[:-3]}')
        print('✔', files[:-3])

if __name__ == '__main__':
    print('Starting...')
    client.run(config.bot_token)