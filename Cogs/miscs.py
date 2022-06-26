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
            embed = discord.Embed(title=f"{member.display_name}'s Avatar", description="*Click below to get the avatar in different formats.*", colour=discord.Colour.brand_green(), timestamp=interaction.created_at)
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
#
#
#     @interactions.extension_command(
#         name="avatar",
#         description="Get the avatar of a member",
#         options = [
#             interactions.Option(
#                 name="member",
#                 description="The member whose avatar you want to get.",
#                 type=interactions.OptionType.USER,
#                 required=False,
#             )
#         ]
#     )
#     async def _get_avatar_url(self, ctx, member: interactions.Member = None):
#         member = member or ctx.author
#         await ctx.send(f"[Avatar]({member.user.avatar_url}) of {member.user.username}#{member.user.discriminator}")
#         # Embed
#         # embed = interactions.Embed(
#         #     title = f"Avatar of {member.user.username}#{member.user.discriminator}",
#         #     color=12745742,
#         #     footer=interactions.EmbedFooter(
#         #         text="Captain James Cook named the ‘aurora australis’.",
#         #         icon_url=ctx.author.user.avatar_url,
#         #     ),
#         #     thumbnail=interactions.EmbedImageStruct(
#         #         url="https://media.discordapp.net/attachments/831369746855362590/954622807302615050/Aurora_Big.png?width=747&height=74",
#         #     )._json,
#         #     image=interactions.EmbedImageStruct(
#         #         url=member.user.avatar_url,
#         #         height=700,
#         #         width=500,
#         #     )._json,
#         # )
#
#     @interactions.extension_command(
#         name="minfo",
#         description="Shows member information.",
#         scope=903225083072495646,
#         options = [
#             interactions.Option(
#                 name="member",
#                 description="The member whose information you want to see.",
#                 type=interactions.OptionType.USER,
#                 required=False,
#             )
#         ]
#     )
#     async def _get_member_information(self, ctx, member: interactions.Member = None):
#         member = member or ctx.author
#         member_obj = await self.client._http.get_member(guild_id=ctx.guild_id, member_id=member.user.id)
#         # guild_role = await self.client._http.get_all_roles(guild_id=ctx.guild_id)
#         top_role = member_obj['roles'][0] if len(member_obj['roles']) > 0 else "N/A"
#         # print(top_role)
#         avatar = member.user.avatar_url
#         name, id = member.user.username, member_obj['user']['id']
#         discriminator = member.user.discriminator
#         nickname = member_obj['nick'] if member_obj['nick'] != None else None
#         joined_at = member_obj['joined_at']
#         convert = pandas.to_datetime(joined_at)
#         joined_at = f"<t:{int(datetime.timestamp(convert))}:R>(<t:{int(datetime.timestamp(convert))}:F>)"
#         mute = member_obj['mute']
#         deaf = member_obj['deaf']
#         username = name+"#"+discriminator
#         embed_title = f"{nickname if nickname != None else username}'s Information."
#         format_role = f"<@&{int(top_role)}>" if top_role != "N/A" else "No Roles Assigned."
#         # Embed
#         fields = [
#             interactions.EmbedField(name="<:member:911835068144685056> Username", value=username),
#             interactions.EmbedField(name="🆔 ID", value=id),
#             interactions.EmbedField(name="<:time:959328643987959818> Joined At", value=joined_at),
#             interactions.EmbedField(name="<:roleicon:959329430428327936> Top Role", value=format_role)
#             # interactions.EmbedField(name="<:deaf:959325547605938196> Is Deafened?", value=deaf),
#             # interactions.EmbedField(name="<:muted:959325547975045160> Is Muted?", value=mute),
#         ]
#         embed = createEmbed(title=embed_title, color=10181046,
#             footer_text="Aurora's are visible from space!", footer_icon_url = "https://media.discordapp.net/attachments/831369746855362590/954622807302615050/Aurora_Big.png",
#             thumbnail_url=avatar,
#             fields=fields
#         )
#         await ctx.send(embeds=embed)
#

async def setup(client):
    await client.add_cog(Miscs(client))
#
#
# # NOTE: f"https://cdn.discordapp.com/avatars/{int(self.client.me.id)}/{self.client.me.icon}"
