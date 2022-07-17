import os
import time

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
                start_time = time.time()
                member = member or interaction.user
                avatar_url = member.avatar.with_format('jpeg')
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw).convert("L")

                with BytesIO() as image_bytes:
                    image.save(image_bytes, 'jpeg')
                    image_bytes.seek(0)
                    embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                          description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                          timestamp=interaction.created_at)
                    embed.set_image(url="attachment://black_and_white.jpeg")
                    runtime = time.time() - start_time
                    embed.set_footer(text=f"Image took {runtime.__format__('0.2f')} sec(s) to generate",
                                     icon_url=interaction.user.display_avatar)
                    file_obj = discord.File(fp=image_bytes, filename="black_and_white.jpeg")
                    await interaction.response.send_message(embed=embed, view=view, file=file_obj)

            elif attachment is not None:
                start_time = time.time()
                image_url = attachment.url
                image = Image.open(requests.get(url=str(image_url), stream=True).raw).convert("L")

                with BytesIO() as image_bytes:
                    image.save(image_bytes, 'jpeg')
                    image_bytes.seek(0)
                    embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                          description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                          timestamp=interaction.created_at)
                    embed.set_image(url="attachment://black_and_white.jpeg")
                    runtime = time.time() - start_time
                    embed.set_footer(text=f"Image took {runtime.__format__('0.2f')} sec(s) to generate",
                                     icon_url=interaction.user.display_avatar)
                    file_obj = discord.File(fp=image_bytes, filename="black_and_white.jpeg")
                    await interaction.response.send_message(embed=embed, view=view, file=file_obj)

            elif attachment is None and member is None:
                start_time = time.time()
                member = member or interaction.user
                avatar_url = member.avatar.with_format('jpeg')
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw).convert("L")

                with BytesIO() as image_bytes:
                    image.save(image_bytes, 'jpeg')
                    image_bytes.seek(0)
                    embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                          description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                          timestamp=interaction.created_at)
                    embed.set_image(url="attachment://black_and_white.jpeg")
                    runtime = time.time() - start_time
                    embed.set_footer(text=f"Image took {runtime.__format__('0.2f')} sec(s) to generate",
                                     icon_url=interaction.user.display_avatar)
                    file_obj = discord.File(fp=image_bytes, filename="black_and_white.jpeg")
                    await interaction.response.send_message(embed=embed, view=view, file=file_obj)

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
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://negative.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"negative.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is not None:
                image_url = attachment.url
                img = await self.dagpi.image_process(ImageFeatures.invert(), url=str(image_url))
                image = Image.open(requests.get(url=str(image_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://negative.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"negative.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is None and member is None:
                member = member or interaction.user
                avatar_url = member.avatar.with_format('jpeg')
                img = await self.dagpi.image_process(ImageFeatures.invert(), url=str(avatar_url))
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://negative.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"negative.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

        except:
            error_logger.error("An error occurred while running negative image command:- ", exc_info=True)

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
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://pixel.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"pixel.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is not None:
                image_url = attachment.url
                img = await self.dagpi.image_process(ImageFeatures.pixel(), url=str(image_url))
                image = Image.open(requests.get(url=str(image_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://pixel.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"pixel.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is None and member is None:
                member = member or interaction.user
                avatar_url = member.avatar.with_format('jpeg')
                img = await self.dagpi.image_process(ImageFeatures.pixel(), url=str(avatar_url))
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://pixel.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"pixel.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

        except:
            error_logger.error("An error occurred while running pixel image command:- ", exc_info=True)

    @app_commands.command(name="colors", description="Gives the constituent colors of the image.")
    @app_commands.describe(
        member="The member's avatar whose color info you want to get",
        attachment="The image file whose color info you want to get"
    )
    async def colors(self, interaction: discord.Interaction, member: discord.Member = None,
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
                img = await self.dagpi.image_process(ImageFeatures.colors(), url=str(avatar_url))
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://colors.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"colors.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is not None:
                image_url = attachment.url
                img = await self.dagpi.image_process(ImageFeatures.colors(), url=str(image_url))
                image = Image.open(requests.get(url=str(image_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://colors.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"colors.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is None and member is None:
                member = member or interaction.user
                avatar_url = member.avatar.with_format('jpeg')
                img = await self.dagpi.image_process(ImageFeatures.colors(), url=str(avatar_url))
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://colors.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"colors.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

        except:
            error_logger.error("An error occurred while running colors image command:- ", exc_info=True)

    @app_commands.command(name="triggered", description="Gives the image edited into a triggered GIF.")
    @app_commands.describe(
        member="The member's avatar which you want to edit",
        attachment="The image file which you want to edit"
    )
    async def triggered(self, interaction: discord.Interaction, member: discord.Member = None,
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
                img = await self.dagpi.image_process(ImageFeatures.triggered(), url=str(avatar_url))
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://triggered.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"triggered.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is not None:
                image_url = attachment.url
                img = await self.dagpi.image_process(ImageFeatures.triggered(), url=str(image_url))
                image = Image.open(requests.get(url=str(image_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://triggered.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"triggered.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is None and member is None:
                member = member or interaction.user
                avatar_url = member.avatar.with_format('jpeg')
                img = await self.dagpi.image_process(ImageFeatures.triggered(), url=str(avatar_url))
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://negative.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"triggered.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

        except:
            error_logger.error("An error occurred while running triggered image command:- ", exc_info=True)

    @app_commands.command(name="expand", description="Gives an expanded version of the image.")
    @app_commands.describe(
        member="The member's avatar which you want to edit",
        attachment="The image file which you want to edit"
    )
    async def expand(self, interaction: discord.Interaction, member: discord.Member = None,
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
                img = await self.dagpi.image_process(ImageFeatures.expand(), url=str(avatar_url))
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://expand.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"expand.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is not None:
                image_url = attachment.url
                img = await self.dagpi.image_process(ImageFeatures.expand(), url=str(image_url))
                image = Image.open(requests.get(url=str(image_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://expand.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"expand.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is None and member is None:
                member = member or interaction.user
                avatar_url = member.avatar.with_format('jpeg')
                img = await self.dagpi.image_process(ImageFeatures.expand(), url=str(avatar_url))
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://expand.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"expand.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

        except:
            error_logger.error("An error occurred while running expand image command:- ", exc_info=True)

    @app_commands.command(name="wasted", description="Gives a wasted version of the image.")
    @app_commands.describe(
        member="The member's avatar which you want to edit",
        attachment="The image file which you want to edit"
    )
    async def wasted(self, interaction: discord.Interaction, member: discord.Member = None,
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
                img = await self.dagpi.image_process(ImageFeatures.wasted(), url=str(avatar_url))
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://wasted.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"wasted.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is not None:
                image_url = attachment.url
                img = await self.dagpi.image_process(ImageFeatures.wasted(), url=str(image_url))
                image = Image.open(requests.get(url=str(image_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://wasted.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"wasted.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is None and member is None:
                member = member or interaction.user
                avatar_url = member.avatar.with_format('jpeg')
                img = await self.dagpi.image_process(ImageFeatures.wasted(), url=str(avatar_url))
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://wasted.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"wasted.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

        except:
            error_logger.error("An error occurred while running wasted image command:- ", exc_info=True)

    @app_commands.command(name="petpat", description="Gives a petpat version of the image.")
    @app_commands.describe(
        member="The member's avatar which you want to edit",
        attachment="The image file which you want to edit"
    )
    async def petpat(self, interaction: discord.Interaction, member: discord.Member = None,
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
                img = await self.dagpi.image_process(ImageFeatures.petpet(), url=str(avatar_url))
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://petpat.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"petpat.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is not None:
                image_url = attachment.url
                img = await self.dagpi.image_process(ImageFeatures.petpet(), url=str(image_url))
                image = Image.open(requests.get(url=str(image_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://petpat.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"petpat.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is None and member is None:
                member = member or interaction.user
                avatar_url = member.avatar.with_format('jpeg')
                img = await self.dagpi.image_process(ImageFeatures.petpet(), url=str(avatar_url))
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://petpat.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"petpat.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

        except:
            error_logger.error("An error occurred while running petpat image command:- ", exc_info=True)

    @app_commands.command(name="bonk", description="Gives a bonked version of the image.")
    @app_commands.describe(
        member="The member's avatar which you want to edit",
        attachment="The image file which you want to edit"
    )
    async def bonk(self, interaction: discord.Interaction, member: discord.Member = None,
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
                img = await self.dagpi.image_process(ImageFeatures.bonk(), url=str(avatar_url))
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://bonk.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"bonk.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is not None:
                image_url = attachment.url
                img = await self.dagpi.image_process(ImageFeatures.bonk(), url=str(image_url))
                image = Image.open(requests.get(url=str(image_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://bonk.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"bonk.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is None and member is None:
                member = member or interaction.user
                avatar_url = member.avatar.with_format('jpeg')
                img = await self.dagpi.image_process(ImageFeatures.bonk(), url=str(avatar_url))
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://bonk.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"bonk.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

        except:
            error_logger.error("An error occurred while running bonk image command:- ", exc_info=True)

    @app_commands.command(name="hog", description="Gives a histogram of oriented gradients of the image.")
    @app_commands.describe(
        member="The member's avatar which you want to edit",
        attachment="The image file which you want to edit"
    )
    async def hog(self, interaction: discord.Interaction, member: discord.Member = None,
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
                img = await self.dagpi.image_process(ImageFeatures.hog(), url=str(avatar_url))
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://hog.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"hog.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is not None:
                image_url = attachment.url
                img = await self.dagpi.image_process(ImageFeatures.hog(), url=str(image_url))
                image = Image.open(requests.get(url=str(image_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://hog.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"hog.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is None and member is None:
                member = member or interaction.user
                avatar_url = member.avatar.with_format('jpeg')
                img = await self.dagpi.image_process(ImageFeatures.hog(), url=str(avatar_url))
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://hog.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"hog.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

        except:
            error_logger.error("An error occurred while running hog image command:- ", exc_info=True)

    @app_commands.command(name="blur", description="Gives a blurred version of the image.")
    @app_commands.describe(
        member="The member's avatar which you want to edit",
        attachment="The image file which you want to edit",
        blur_radius="The intensity of the blur in int"
    )
    async def blur(self, interaction: discord.Interaction, blur_radius: int, member: discord.Member = None,
                   attachment: discord.Attachment = None):
        await interaction.response.defer()
        view = DeleteButton()
        try:
            if attachment is not None and member is not None:
                await interaction.followup.send(
                    "<a:alert:997769654141452359> You can give only one option at once!")

            elif member is not None:
                start_time = time.time()
                member = member or interaction.user
                avatar_url = member.avatar.with_format('jpeg')
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw)
                blurred_image = image.filter(ImageFilter.GaussianBlur(radius=blur_radius))

                with BytesIO() as image_bytes:
                    blurred_image.save(image_bytes, 'jpeg')
                    image_bytes.seek(0)
                    embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                          description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                          timestamp=interaction.created_at)
                    embed.set_image(url=f"attachment://blur.jpeg")
                    runtime = time.time() - start_time
                    embed.set_footer(text=f"Image took {runtime.__format__('0.2f')} sec(s) to generate",
                                     icon_url=interaction.user.display_avatar)
                    file_obj = discord.File(fp=image_bytes, filename=f"blur.jpeg")

                    await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is not None:
                start_time = time.time()
                image_url = attachment.url
                image = Image.open(requests.get(url=str(image_url), stream=True).raw)
                blurred_image = image.filter(ImageFilter.GaussianBlur(radius=blur_radius))

                with BytesIO() as image_bytes:
                    blurred_image.save(image_bytes, 'jpeg')
                    image_bytes.seek(0)
                    embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                          description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                          timestamp=interaction.created_at)
                    embed.set_image(url=f"attachment://blur.jpeg")
                    runtime = time.time() - start_time
                    embed.set_footer(text=f"Image took {runtime.__format__('0.2f')} sec(s) to generate",
                                     icon_url=interaction.user.display_avatar)
                    file_obj = discord.File(fp=image_bytes, filename=f"blur.jpeg")

                    await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is None and member is None:
                start_time = time.time()
                member = member or interaction.user
                avatar_url = member.avatar.with_format('jpeg')
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw)
                blurred_image = image.filter(ImageFilter.GaussianBlur(radius=blur_radius))

                with BytesIO() as image_bytes:
                    blurred_image.save(image_bytes, 'jpeg')
                    image_bytes.seek(0)
                    embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                          description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                          timestamp=interaction.created_at)
                    embed.set_image(url=f"attachment://blur.jpeg")
                    runtime = time.time() - start_time
                    embed.set_footer(text=f"Image took {runtime.__format__('0.2f')} sec(s) to generate",
                                     icon_url=interaction.user.display_avatar)
                    file_obj = discord.File(fp=image_bytes, filename=f"blur.jpeg")

                    await interaction.followup.send(embed=embed, file=file_obj, view=view)

        except:
            error_logger.error("An error occurred while running blur image command:- ", exc_info=True)

    @app_commands.command(name="rgb", description="Gives a rgb graph of the image's colors.")
    @app_commands.describe(
        member="The member's avatar which you want to edit",
        attachment="The image file which you want to edit"
    )
    async def rgb(self, interaction: discord.Interaction, member: discord.Member = None,
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
                img = await self.dagpi.image_process(ImageFeatures.rgb(), url=str(avatar_url))
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://rgb.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"rgb.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is not None:
                image_url = attachment.url
                img = await self.dagpi.image_process(ImageFeatures.rgb(), url=str(image_url))
                image = Image.open(requests.get(url=str(image_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://rgb.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"rgb.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is None and member is None:
                member = member or interaction.user
                avatar_url = member.avatar.with_format('jpeg')
                img = await self.dagpi.image_process(ImageFeatures.rgb(), url=str(avatar_url))
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://rgb.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"rgb.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

        except:
            error_logger.error("An error occurred while running rgb image command:- ", exc_info=True)

    @app_commands.command(name="lego", description="Gives a lego version of the image.")
    @app_commands.describe(
        member="The member's avatar which you want to edit",
        attachment="The image file which you want to edit"
    )
    async def lego(self, interaction: discord.Interaction, member: discord.Member = None,
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
                img = await self.dagpi.image_process(ImageFeatures.lego(), url=str(avatar_url))
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://lego.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"lego.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is not None:
                image_url = attachment.url
                img = await self.dagpi.image_process(ImageFeatures.lego(), url=str(image_url))
                image = Image.open(requests.get(url=str(image_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://lego.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"lego.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is None and member is None:
                member = member or interaction.user
                avatar_url = member.avatar.with_format('jpeg')
                img = await self.dagpi.image_process(ImageFeatures.lego(), url=str(avatar_url))
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://lego.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"lego.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

        except:
            error_logger.error("An error occurred while running lego image command:- ", exc_info=True)

    @app_commands.command(name="album", description="Gives a music album version of the image.")
    @app_commands.describe(
        member="The member's avatar which you want to edit",
        attachment="The image file which you want to edit"
    )
    async def album(self, interaction: discord.Interaction, member: discord.Member = None,
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
                img = await self.dagpi.image_process(ImageFeatures.album(), url=str(avatar_url))
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://album.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"album.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is not None:
                image_url = attachment.url
                img = await self.dagpi.image_process(ImageFeatures.album(), url=str(image_url))
                image = Image.open(requests.get(url=str(image_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> <:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://album.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"album.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

            elif attachment is None and member is None:
                member = member or interaction.user
                avatar_url = member.avatar.with_format('jpeg')
                img = await self.dagpi.image_process(ImageFeatures.album(), url=str(avatar_url))
                image = Image.open(requests.get(url=str(avatar_url), stream=True).raw)
                embed = discord.Embed(title="<:photo:995519248006905896> Formatted Image", color=discord.Color.blurple(),
                                      description=f"*Height - {image.height} px\nWidth - {image.width} px*",
                                      timestamp=interaction.created_at)
                embed.set_image(url=f"attachment://album.{img.format}")
                embed.set_footer(text=f"Image took {img.process_time} sec(s) to generate",
                                 icon_url=interaction.user.display_avatar)
                file_obj = discord.File(fp=img.image, filename=f"album.{img.format}")
                await interaction.followup.send(embed=embed, file=file_obj, view=view)

        except:
            error_logger.error("An error occurred while running album image command:- ", exc_info=True)


async def setup(client):
    await client.add_cog(ImageManipulation(client))
