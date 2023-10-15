import disnake
from disnake.ext import commands
from disnake.embeds import Embed

class On_ready(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener("on_ready")
    async def help_listener(self):
        print("Bot is Ready!")

def setup(client):
    client.add_cog(On_ready(client))