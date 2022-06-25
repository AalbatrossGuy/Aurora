import discord, asyncio
from discord.ext import commands
from discord import app_commands
from customs.log import AuroraLogger

# LOGGER
error_logger = AuroraLogger('AuroraErrorLog', 'logs/errors.log')


#  COMMANDS
class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="clear", description="Delete messages from a channel.")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(
        amount="The amount of messages to clear. The default is 10"
    )
    async def _clear_messages(self, interaction: discord.Interaction, amount: int = 10):
        try:
            deleted_messages = await interaction.channel.purge(limit=amount)
            await interaction.response.send_message(f"Deleted {len(deleted_messages)} Messages!")
            await asyncio.sleep(3)
            await interaction.delete_original_message()
        except:
            error_logger.error(f"Error occurred while running clear command:- ", exc_info=True)

    @app_commands.command(name="kick", description="Kick a Member from the guild.")
    @app_commands.checks.has_permissions(kick_members=True)
    @app_commands.describe(
        member="The member to kick from the guild.",
        reason="The reason for kicking from the guild."
    )
    async def _kick_member(self, interaction: discord.Interaction, member: discord.Member, reason: str = "N/A"):
        try:
            embed = discord.Embed(title="<:kick:989811114567168051> Kicked", color=discord.Colour.dark_gold(),
                                  timestamp=interaction.created_at,
                                  description=f"You have been **kicked** from the server **{interaction.guild.name}** for the reason `{reason}`")
            embed.set_footer(text="Auroras constantly change shape.",
                             icon_url=interaction.user.display_avatar)
            embed.set_thumbnail(
                url="https://i.gifer.com/Bwtn.gif")
            user_channel = await member.create_dm()
            await user_channel.send(embed=embed)
            await member.kick(reason=reason)
            await interaction.response.send_message(f"Successfully kicked {member.mention} from the server!")
            await asyncio.sleep(3)
            await interaction.delete_original_message()
        except:
            error_logger.error(f"Error occurred while running kick command:- ", exc_info=True)

    @app_commands.command(name="ban", description="Ban a Member from the guild.")
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.describe(
        member="The member to ban from the guild.",
        reason="The reason for banning from the guild."
    )
    async def _ban_member(self, interaction: discord.Interaction, member: discord.Member, reason: str = "N/A"):
        try:
            embed = discord.Embed(title="<:kick:989811114567168051> Banned", color=discord.Colour.dark_gold(),
                                  timestamp=interaction.created_at,
                                  description=f"You have been **banned** from the server **{interaction.guild.name}** for the reason `{reason}`")
            embed.set_footer(text="The term ‘aurora borealis’ was coined in 1619",
                             icon_url=interaction.user.display_avatar)
            embed.set_thumbnail(
                url="https://c.tenor.com/TbfChfHKkOUAAAAM/ban-button.gif")
            user_channel = await member.create_dm()
            await user_channel.send(embed=embed)
            await member.ban(reason=reason)
            await interaction.response.send_message(f"Successfully banned {member.mention} from the server!")
            await asyncio.sleep(3)
            await interaction.delete_original_message()
        except:
            error_logger.error(f"Error occurred while running ban command:- ", exc_info=True)
#
#
#     # Unban Command
#     @interactions.extension_command(
#         name="unban",
#         description="Unbans a user from the server.",
#         options = [
#             interactions.Option(
#                 name="member_id",
#                 description="The member to unban from the server.",
#                 type=interactions.OptionType.STRING,
#                 required=True,
#             ),
#         ],
#     )
#     async def _unban_member(self, ctx, member_id: str) -> None:
#         try:
#             member_id = int(member_id) if len(member_id) == 18 else 0
#             guild = await ctx.get_guild()
#             # print(f"Guild = {guild} & {guild.id}")
#             if member_id != 0:
#                 print(guild)
#                 _member = await self.client._http.get_member(guild_id=guild.id, member_id=member_id)
#                 member = interactions.User(**_member)
#                 if ctx.author.permissions & interactions.Permissions.BAN_MEMBERS:
#                     await guild.remove_ban(user_id=member_id)
#                     await ctx.send(f"Successfully Unbanned <@{member_id}>.")
#                 else:
#                     await ctx.send("Oops! you don't have the required permission to run this command.")
#             else:
#                 await ctx.send("Please provide a valid Member ID to unban!")
#         except:
#             error_logger.error("Error occured while responding to /unban :-", exc_info=True)
#
#
async def setup(client):
    await client.add_cog(Admin(client))
