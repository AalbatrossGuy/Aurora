from discord.ext import commands
import discord
from discord import app_commands
from customs.log import AuroraLogger

# LOGGER
error_logger = AuroraLogger("AuroraErrorLog", "logs/errors.log")


class Miscs(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="avatar", description="Gives the member's avatar in different file format.")
    @app_commands.describe(
        member="The member whose avatar you wish to view."
    )
    async def _display_avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        try:
            member = member or interaction.user
            embed = discord.Embed(title=f"{member.display_name}'s Avatar",
                                  description="*Click below to get the avatar in different formats.*",
                                  colour=discord.Colour.brand_green(), timestamp=interaction.created_at)
            embed.set_footer(text="The Northern Lights")
            base_avatar = member.display_avatar
            avatar_png = member.avatar.with_format('png')
            avatar_jpg = member.avatar.with_format('jpg')
            avatar_webp = member.avatar.with_format('webp')
            buttons = discord.ui.View()
            buttons.add_item(
                discord.ui.Button(label="PNG", style=discord.ButtonStyle.url, url=str(avatar_png), emoji="📸")
            )
            buttons.add_item(
                discord.ui.Button(label="JPG", style=discord.ButtonStyle.url, url=str(avatar_jpg), emoji="📸")
            )
            buttons.add_item(
                discord.ui.Button(label="WEBP", style=discord.ButtonStyle.url, url=str(avatar_webp), emoji="📸")
            )
            embed.set_image(url=base_avatar)
            await interaction.response.send_message(embed=embed, view=buttons)
        except:
            error_logger.error("Error occurred while running avatar command:- ", exc_info=True)


async def setup(client):
    await client.add_cog(Miscs(client))
