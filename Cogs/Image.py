import os

import discord, json, requests
from discord.ext import commands
from discord import app_commands
from customs.log import AuroraLogger
from io import BytesIO
from PIL import Image, ImageOps, ImageFilter
from asyncdagpi import Client, ImageFeatures

file = open("config.json", "r")
config = json.loads(file.read())
error_logger = AuroraLogger("AuroraErrorLog", "logs/errors.log")


# VIEW
class DeleteButton(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(emoji="<:delete:912359260954984459>", style=discord.ButtonStyle.red)
    async def delete(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.defer()
        await interaction.delete_original_message()


class ImageManipulation(commands.GroupCog, name="image"):
    def __init__(self, client):
        self.client = client
        self.dagpi = Client(config["API_KEYS"]["DAGPI_KEY"])

    @app_commands.command(name="b_w", description="Give a black and white version of the image.")
    @app_commands.describe(
        member="The avatar of the member.",
        attachment="The image file which you want to edit."
    )
    async def black_and_white_user(self, interaction: discord.Interaction, member: discord.Member = None,
                                   attachment: discord.Attachment = None):
        view = DeleteButton()
        try:
            if attachment is not None and member is not None:
                await interaction.response.send_message(
                    "<a:alert:997769654141452359> You can give only one option at once!")
            elif member is not None:
                member = member or interaction.user
                avatar_url = member.avatar.with_format('jpeg')
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw).convert("L")

                with BytesIO() as image_bytes:
                    image.save(image_bytes, 'jpeg')
                    image_bytes.seek(0)
                    await interaction.response.send_message(
                        embed=discord.Embed(title="Formatted Image", color=discord.Color.blurple(),
                                            description=f"*Height - {image.height} px\nWidth - {image.width} px*").set_image(
                            url="attachment://image.jpeg"),
                        file=discord.File(fp=image_bytes, filename="image.jpeg"), view=view)
            elif attachment is not None:
                image_url = attachment.url
                image = Image.open(requests.get(url=str(image_url), stream=True).raw).convert("L")

                with BytesIO() as image_bytes:
                    image.save(image_bytes, 'jpeg')
                    image_bytes.seek(0)
                    await interaction.response.send_message(
                        embed=discord.Embed(title="Formatted Image", color=discord.Color.blurple(),
                                            description=f"*Height - {attachment.height} px\nWidth - {attachment.width} px\nContent Type - {attachment.content_type}*").set_image(
                            url="attachment://image.jpeg"),
                        file=discord.File(fp=image_bytes, filename="image.jpeg"), view=view)
            elif attachment is None and member is None:
                member = member or interaction.user
                avatar_url = member.avatar.with_format('jpeg')
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw).convert("L")

                with BytesIO() as image_bytes:
                    image.save(image_bytes, 'jpeg')
                    image_bytes.seek(0)
                    # print(discord.File(fp=image_bytes, filename="image.jpeg"))
                    await interaction.response.send_message(
                        embed=discord.Embed(title="Formatted Image", color=discord.Color.blurple(),
                                            description=f"*Height - {image.height} px\nWidth - {image.width} px*").set_image(
                            url="attachment://image.jpeg"),
                        file=discord.File(fp=image_bytes, filename="image.jpeg"), view=view)

        except:
            error_logger.error("An error occurred while running b_w image command:- ", exc_info=True)

    @app_commands.command(name="negative", description="Gives a negative version of the image.")
    @app_commands.describe(
        member="The member's avatar which you want to edit",
        attachment="The image file which you want to edit"
    )
    async def negative(self, interaction: discord.Interaction, member: discord.Member = None,
                       attachment: discord.Attachment = None):
        await interaction.response.defer()
        view = DeleteButton()
        try:
            if attachment is not None and member is not None:
                await interaction.followup.send(
                    "<a:alert:997769654141452359> You can give only one option at once!")

            elif member is not None:
                member = member or interaction.user
                avatar_url = member.avatar.with_format('jpeg')
                img = await self.dagpi.image_process(ImageFeatures.invert(), url=str(avatar_url))
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw)
                embed = discord.Embed(title="Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://negative.{img.format}")
                embed.set_footer(text=f"Process took {img.process_time} sec(s) to complete",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"negative.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is not None:
                image_url = attachment.url
                img = await self.dagpi.image_process(ImageFeatures.invert(), url=str(image_url))
                image = Image.open(requests.get(url=str(image_url), stream=True).raw)
                embed = discord.Embed(title="Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://negative.{img.format}")
                embed.set_footer(text=f"Process took {img.process_time} sec(s) to complete",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"negative.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is None and member is None:
                member = member or interaction.user
                avatar_url = member.avatar.with_format('jpeg')
                img = await self.dagpi.image_process(ImageFeatures.invert(), url=str(avatar_url))
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw)
                embed = discord.Embed(title="Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://negative.{img.format}")
                embed.set_footer(text=f"Process took {img.process_time} sec(s) to complete",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"negative.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

        except:
            error_logger.error("An error occurred while running b_w image command:- ", exc_info=True)

    @app_commands.command(name="pixel", description="Gives a pixelated version of the image.")
    @app_commands.describe(
        member="The member's avatar which you want to edit",
        attachment="The image file which you want to edit"
    )
    async def pixel(self, interaction: discord.Interaction, member: discord.Member = None,
                    attachment: discord.Attachment = None):
        await interaction.response.defer()
        view = DeleteButton()
        try:
            if attachment is not None and member is not None:
                await interaction.followup.send(
                    "<a:alert:997769654141452359> You can give only one option at once!")

            elif member is not None:
                member = member or interaction.user
                avatar_url = member.avatar.with_format('jpeg')
                img = await self.dagpi.image_process(ImageFeatures.pixel(), url=str(avatar_url))
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw)
                embed = discord.Embed(title="Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://negative.{img.format}")
                embed.set_footer(text=f"Process took {img.process_time} sec(s) to complete",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"negative.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is not None:
                image_url = attachment.url
                img = await self.dagpi.image_process(ImageFeatures.pixel(), url=str(image_url))
                image = Image.open(requests.get(url=str(image_url), stream=True).raw)
                embed = discord.Embed(title="Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://negative.{img.format}")
                embed.set_footer(text=f"Process took {img.process_time} sec(s) to complete",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"negative.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is None and member is None:
                member = member or interaction.user
                avatar_url = member.avatar.with_format('jpeg')
                img = await self.dagpi.image_process(ImageFeatures.pixel(), url=str(avatar_url))
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw)
                embed = discord.Embed(title="Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://negative.{img.format}")
                embed.set_footer(text=f"Process took {img.process_time} sec(s) to complete",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"negative.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

        except:
            error_logger.error("An error occurred while running b_w image command:- ", exc_info=True)


async def setup(client):
    await client.add_cog(ImageManipulation(client))
