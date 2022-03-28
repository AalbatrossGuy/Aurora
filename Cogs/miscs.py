import interactions

class Miscs(interactions.Extension):
    def __init__(self, client):
        self.client = client


    @interactions.extension_command(
        name="avatar",
        description="Get the avatar of a member",
        options = [
            interactions.Option(
                name="member",
                description="The member whose avatar you want to get.",
                type=interactions.OptionType.USER,
                required=False,
            )
        ]
    )
    async def _get_avatar_url(self, ctx, member: interactions.Member = None):
        member = member or ctx.author
        await ctx.send(f"[Avatar]({member.user.avatar_url}) of {member.user.username}#{member.user.discriminator}")
        # Embed
        # embed = interactions.Embed(
        #     title = f"Avatar of {member.user.username}#{member.user.discriminator}",
        #     color=12745742,
        #     footer=interactions.EmbedFooter(
        #         text="Captain James Cook named the ‘aurora australis’.",
        #         icon_url=ctx.author.user.avatar_url,
        #     ),
        #     thumbnail=interactions.EmbedImageStruct(
        #         url="https://media.discordapp.net/attachments/831369746855362590/954622807302615050/Aurora_Big.png?width=747&height=74",
        #     )._json,
        #     image=interactions.EmbedImageStruct(
        #         url=member.user.avatar_url,
        #         height=700,
        #         width=500,
        #     )._json,
        # )

    @interactions.extension_command(
        name="minfo",
        description="Shows member information.",
        options = [
            interactions.Option(
                name="member",
                description="The member whose information you want to see.",
                type=interactions.OptionType.USER,
                required=False,
            )
        ]
    )
    async def _get_member_information(self, ctx, member: interactions.Member = None):
        member = member or ctx.author


def setup(client):
    Miscs(client)


# NOTE: f"https://cdn.discordapp.com/avatars/{int(self.client.me.id)}/{self.client.me.icon}"
