import disnake
import config

from disnake.ext import commands
from modules.embed import EmbedGenerator

class Whitelist_msg(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command()
    @commands.has_permissions(administrator=True)
    async def whitelist_msg(self, inter: disnake.ApplicationCommandInteraction):
        whitelist_send = config.all_text["just_text"]["whitelist_send"]
        button_send = config.all_text["buttons"]["whitelist_send"]
        whitelist_msg = config.all_text["whitelist_msg"]

        await inter.response.send_message(whitelist_send, ephemeral=True)

        await inter.channel.send(
            embed=EmbedGenerator(json_schema=whitelist_msg),
            components=[disnake.ui.Button(label=button_send, style=disnake.ButtonStyle.success, custom_id=button_send)]
        )

def setup(client):
    client.add_cog(Whitelist_msg(client))