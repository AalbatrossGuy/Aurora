import interactions, asyncio


class Admin(interactions.Extension):
    def __init__(self, client):
        self.client = client

    @interactions.extension_command(
        name="clear",
        description="Clear messages in chat.",
        scope=903225083072495646,
        options = [
        interactions.Option(
            name="amount",
            description="The number of messages you want to delete. By default it's 10.",
            type=interactions.OptionType.INTEGER,
            required=False,
        ),
     ],
    )
    async def _clear_messages(self, ctx, amount=10):
        channel = await ctx.get_channel()
        await channel.purge(amount=amount+1)
        await ctx.send(f"Purged {amount} messages!")
        await asyncio.sleep(2)
        await ctx.message.delete()

    @interactions.extension_command(
        name="kick",
        description="Kicks a user from the server.",
        scope=903225083072495646,
        options = [
            interactions.Option(
                name="member",
                description="The member to kick from the server.",
                type=interactions.OptionType.USER,
                required=True,
            ),
            interactions.Option(
                name="reason",
                description="The reason for kicking a member from the server.",
                type=interactions.OptionType.STRING,
                required=False,
            ),
        ],
    )
    async def _kick_member(self, ctx, member: interactions.Member, reason: str = "No reason provided."):
        guild = await ctx.get_guild()
        guild_id = guild.id
        if ctx.author.permissions & interactions.Permissions.KICK_MEMBERS:
            await member.kick(guild_id=guild_id, reason=reason)
            await ctx.send(f"Successfully kicked {member.mention} for `{reason}`")
        else:
            await ctx.send("Oops! you don't have the required permission to run this command.")


    @interactions.extension_command(
        name="ban",
        description="Bans a user from the server.",
        scope=903225083072495646,
        options = [
            interactions.Option(
                name="member",
                description="The member to ban from the server.",
                type=interactions.OptionType.USER,
                required=True,
            ),
            interactions.Option(
                name="reason",
                description = "THe reason for banning a member from the server.",
                type=interactions.OptionType.STRING,
                required=False,
            ),
        ],
    )
    async def _ban_member(self, ctx, member: interactions.Member, reason: str = "No reason provided."):
        guild = await ctx.get_guild()
        guild_id = guild.id
        if ctx.author.permissions & interactions.Permissions.BAN_MEMBERS:
            await member.ban(guild_id=guild_id, reason=reason)
            await ctx.send(f"Successfully Banned {member.mention} for `{reason}`")
        else:
            await ctx.send("Oops! you don't have the required permission to run this command.")


def setup(client):
    Admin(client)