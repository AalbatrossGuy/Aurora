# import interactions, asyncio, logging
# from customs.customs import AuroraLogger
#
# # LOG SETTINGS
# logger = AuroraLogger('AuroraLog', 'logs/info.log')
# error_logger = AuroraLogger('AuroraErrorLog', 'logs/aurora.log')
#
# # COMMANDS
# class Admin(interactions.Extension):
#     def __init__(self, client):
#         self.client = client
#
#
#     # Clear Command
#     @interactions.extension_command(
#         name="clear",
#         description="Clear messages in chat.",
#         options = [
#         interactions.Option(
#             name="amount",
#             description="The number of messages you want to delete. By default it's 10.",
#             type=interactions.OptionType.INTEGER,
#             required=False,
#         ),
#      ],
#     )
#     async def _clear_messages(self, ctx, amount=10):
#         try:
#             channel = await ctx.get_channel()
#             await channel.purge(amount=amount+1)
#             await ctx.send(f"Purged {amount} messages!")
#             await asyncio.sleep(2)
#             await ctx.message.delete()
#         except:
#             error_logger.error("Error occured while responding to /clear :-", exc_info=True)
#
#
#     # Kick Command
#     @interactions.extension_command(
#         name="kick",
#         description="Kicks a user from the server.",
#         options = [
#             interactions.Option(
#                 name="member",
#                 description="The member to kick from the server.",
#                 type=interactions.OptionType.USER,
#                 required=True,
#             ),
#             interactions.Option(
#                 name="reason",
#                 description="The reason for kicking a member from the server.",
#                 type=interactions.OptionType.STRING,
#                 required=False,
#             ),
#         ],
#     )
#     async def _kick_member(self, ctx, member: interactions.Member, reason: str = "No reason provided."):
#         try:
#             guild = await ctx.get_guild()
#             guild_id = guild.id
#             if ctx.author.permissions & interactions.Permissions.KICK_MEMBERS:
#                 await member.kick(guild_id=guild_id, reason=reason)
#                 await ctx.send(f"Successfully kicked {member.mention} for `{reason}`")
#             else:
#                 await ctx.send("Oops! you don't have the required permission to run this command.")
#         except:
#             error_logger.error("Error occured while responding to /kick :-", exc_info=True)
#
#
#     # Ban Command
#     @interactions.extension_command(
#         name="ban",
#         description="Bans a user from the server.",
#         options = [
#             interactions.Option(
#                 name="member",
#                 description="The member to ban from the server.",
#                 type=interactions.OptionType.USER,
#                 required=True,
#             ),
#             interactions.Option(
#                 name="reason",
#                 description = "THe reason for banning a member from the server.",
#                 type=interactions.OptionType.STRING,
#                 required=False,
#             ),
#         ],
#     )
#     async def _ban_member(self, ctx, member: interactions.Member, reason: str = "No reason provided."):
#         try:
#             guild = await ctx.get_guild()
#             guild_id = guild.id
#             if ctx.author.permissions & interactions.Permissions.BAN_MEMBERS:
#                 await member.ban(guild_id=guild_id, reason=reason)
#                 await ctx.send(f"Successfully Banned {member.mention} for `{reason}`")
#             else:
#                 await ctx.send("Oops! you don't have the required permission to run this command.")
#         except:
#             error_logger.error("Error occured while responding to /ban :-", exc_info=True)
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
# def setup(client):
#     Admin(client)
