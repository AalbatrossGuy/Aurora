from discord.ext import commands
import discord
from discord import app_commands
from datetime import timezone
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
                discord.ui.Button(label="PNG", style=discord.ButtonStyle.url, url=str(avatar_png), emoji=self.client.get_emoji(995519549057282108))
            )
            buttons.add_item(
                discord.ui.Button(label="JPG", style=discord.ButtonStyle.url, url=str(avatar_jpg), emoji=self.client.get_emoji(995519549057282108))
            )
            buttons.add_item(
                discord.ui.Button(label="WEBP", style=discord.ButtonStyle.url, url=str(avatar_webp), emoji=self.client.get_emoji(995519549057282108))
            )
            embed.set_image(url=base_avatar)
            await interaction.response.send_message(embed=embed, view=buttons)
        except:
            error_logger.error("Error occurred while running avatar command:- ", exc_info=True)

    @app_commands.command(name="meminfo", description="Shows information about the member")
    @app_commands.describe(
        member="The member whose info you wish to see."
    )
    async def _display_member_info(self, interaction: discord.Interaction, member: discord.Member = None):
        try:
            member = member or interaction.user
            member_id = member.id
            member_name = member.name
            member_avatar_url = member.display_avatar
            member_nickname = member.nick
            is_bot = member.bot
            member_top_role = member.top_role.mention
            member_created_at = int(member.created_at.replace(tzinfo=timezone.utc).timestamp())
            member_joined_at = int(member.joined_at.replace(tzinfo=timezone.utc).timestamp())
            if member.display_avatar.is_animated() is True:
                member_has_nitro = True
            else:
                member_has_nitro = False

            embed = discord.Embed(title=f"{member_nickname if member_nickname is not None else member_name}'s Profile", description="<:damn:993688550119850015> *A nice profile you got kid!*", timestamp=interaction.created_at, color=member.color)
            embed.set_footer(text="*Nitro is checked based on user's pfp", icon_url=interaction.user.display_avatar)
            embed.set_thumbnail(url=member_avatar_url)
            embed.add_field(name="<:lilgrux:995515614275829760> Name", value=member_name)
            embed.add_field(name="<:lilgrux:995515614275829760> ID", value=member_id)
            embed.add_field(name="<:top:995516251357073480> Top Role", value=member_top_role)
            embed.add_field(name="<a:mcclock:995517509430161498> Joined At", value=f"<t:{member_joined_at}:F>\n(<t:{member_joined_at}:R>)")
            embed.add_field(name="<a:mcclock:995517509430161498> Created At", value=f"<t:{member_created_at}:F>\n(<t:{member_created_at}:R>)")
            embed.add_field(name="<a:nitrobaby:836902390766108694> Nitro?*", value=member_has_nitro)
            permissions = dict(member.top_role.permissions)
            lst = []
            for keys, values in permissions.items():
                if values:
                    lst.append(f"• {keys}")
                else:
                    continue

            before_len = len(lst)
            if len(lst) > 5:
                lst = lst[:5]
                left = before_len - 5
                lst.append(f"+{left} more...")
            embed.add_field(name="<:roleicon:959329430428327936> Top Role Perms", value="\n".join(lst))

            await interaction.response.send_message(embed=embed)
        except:
            error_logger.error("Error occurred while running member_info command:- ", exc_info=True)


async def setup(client):
    await client.add_cog(Miscs(client))
