import config
import disnake

from disnake.ext import commands
from modules.embed import EmbedGenerator

class On_button_click(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.modals = client.modals
        self.rcon = client.rcon


    @commands.Cog.listener("on_button_click")
    async def help_listener(self, inter: disnake.MessageInteraction):
        data = inter.component.custom_id.split("|")
        role = inter.guild.get_role(config.role_id_add)
        private_message_approve = config.all_text["private_message_approve"]
        button_send = config.all_text["buttons"]["whitelist_send"]
        approve = config.all_text["just_text"]["approve"]
        not_mamber = config.all_text["just_text"]["not_mamber"]

        if inter.component.custom_id == button_send:
            channel = inter.guild.get_channel(config.chanel_whitelist)

            await inter.response.send_modal(modal=self.modals.Whitelist(channel))

        elif inter.component.custom_id.startswith("Принять"):
            id = int(data[1])
            member = inter.guild.get_member(id)
            nickname = data[2]

            if member and member.id == id:
                await member.add_roles(role)
                await member.edit(nick=nickname)
                await member.send(embed=EmbedGenerator(json_schema=private_message_approve))
                self.rcon.whitelist_add(nickname)

                await inter.response.send_message(content=approve % member.mention, ephemeral=True)
                await inter.message.edit(components=[])

            else: 
                await inter.response.send_message(content=not_mamber, ephemeral=True)
                await inter.message.delete()

        elif inter.component.custom_id.startswith("Отклонить"):
            id = int(data[1])
            member = inter.guild.get_member(id)

            if member and member.id == id:
                await inter.response.send_modal(modal=self.modals.Reject(member))
                await inter.message.edit(components=[])

            else:
                await inter.response.send_message(content=not_mamber, ephemeral=True)
                await inter.message.delete()


def setup(client):
    client.add_cog(On_button_click(client))