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
            await interaction.response.defer(thinking=True, ephemeral=True)
            deleted_messages = await interaction.channel.purge(limit=amount)
            await interaction.followup.send(f"<:salute:831807820118622258> Deleted {len(deleted_messages)} Messages!")
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

    @app_commands.command(name="unban", description="Unbans a banned user.")
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.describe(
        member="The member to unban. Either give ID or complete username with discriminator(#)."
    )
    async def _unban_member(self, interaction: discord.Interaction, member: str):

        if member.isdigit():
            try:
                try:
                    member_obj = await self.client.fetch_user(member)
                    await interaction.guild.unban(user=member_obj)
                    await interaction.response.send_message(f"Successfully unbanned **{member_obj}**!")
                except discord.NotFound:
                    await interaction.response.send_message(
                        f"User with id {member} was not found in the banned entries.")
            except:
                error_logger.error("Error occurred while running unban command[INTEGER_INPUT]:- ", exc_info=True)

        elif isinstance(member, str) and "#" in member:

            try:
                banned_users = interaction.guild.bans()
                member_name, member_discriminator = member.split('#')
                async for ban_entry in banned_users:
                    user = ban_entry.user
                    if (user.name, user.discriminator) == (member_name, member_discriminator):
                        await interaction.guild.unban(user=user)
                        await interaction.response.send_message(f"Successfully unbanned **{member}**!")
            except:
                error_logger.error(f"Error occurred while running unban command[STRING_INPUT]:- ", exc_info=True)


async def setup(client):
    await client.add_cog(Admin(client))
