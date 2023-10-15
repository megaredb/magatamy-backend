import disnake
import config

from disnake import TextInputStyle
from modules.embed import EmbedGenerator

# Subclassing the modal.
class Whitelist(disnake.ui.Modal):
    def __init__(self, target_channel):
        self.target_channel = target_channel
        components = [
            disnake.ui.TextInput(
                label="Укажи ник своего аккаунта Майнкрафт.",
                placeholder="Напишите Ник сюда.",
                custom_id="Ник Игрока",
                style=TextInputStyle.short,
            ),
            disnake.ui.TextInput(
                label="Сколько тебе лет?",
                placeholder="Напишите ваш ответ сюда.",
                custom_id="Возраст",
                style=TextInputStyle.short,
            ),
            disnake.ui.TextInput(
                label="Откуда узнал о сервере? Сколько тебе лет?",
                placeholder="Напишите ваш ответ сюда.",
                custom_id="О Игроке",
                style=TextInputStyle.short,
            ),
            disnake.ui.TextInput(
                label="Какой опыт игры на приватных серверах?",
                placeholder="Напишите свой ответ сюда.",
                custom_id="Опыт в Майне",
                style=TextInputStyle.short,
            ),
            disnake.ui.TextInput(
                label="Чем планируешь заниматься на сервере?",
                placeholder="Напишите свой ответ сюда.",
                custom_id="Цель на Сервер",
                style=TextInputStyle.paragraph,
            ),
        ]
        super().__init__(title="Whitelist", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        embed = disnake.Embed(title="Whitelist")
        embed.add_field(
            name="Игрок",
            value=inter.author.mention,
            inline=False,
        )
        for key, value in inter.text_values.items():
            value = value.strip()

            if key == "Ник Игрока":
                nikname = value

            embed.add_field(
                name=key.capitalize(),
                value=value[:1024],
                inline=False,
            )
        
        components=[
            disnake.ui.Button(label="Принять", style=disnake.ButtonStyle.success, custom_id=f"Принять|{inter.author.id}|{nikname}"),
            disnake.ui.Button(label="Отклонить", style=disnake.ButtonStyle.success, custom_id=f"Отклонить|{inter.author.id}")
        ]
                
        await inter.response.send_message(content="Вы успешно подали заявку\nВ течении 24 часов ваш запрос будет рассмотрен", ephemeral=True)
        await self.target_channel.send(embed=embed, components=components)
        
class Reject(disnake.ui.Modal):
    def __init__(self, member):
        self.member = member
        components = [
            disnake.ui.TextInput(
                label="Причина отклонения?",
                placeholder="Напишите причину сюда.",
                custom_id="Причина отклонения",
                style=TextInputStyle.paragraph,
            )
        ]
        super().__init__(title="Причина отказа", components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        embed = EmbedGenerator(json_schema=config.all_text["reject"])
        for key, value in inter.text_values.items():
            value = value.strip()
            embed.add_field(
                name=key.capitalize(),
                value=value[:1024],
                inline=False,
            )

        await self.member.send(embed=embed)

        await inter.response.send_message(content=f"Вы отклонили заявку игрока - {self.member.mention}", ephemeral=True)
