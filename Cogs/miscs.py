from discord.ext import commands
import discord, json
from discord import app_commands
from datetime import timezone
from customs.log import AuroraLogger
from asyncdagpi import Client

file = open("config.json", "r")
config = json.loads(file.read())
# LOGGER
error_logger = AuroraLogger("AuroraErrorLog", "logs/errors.log")


# VIEWS
class RightButton(discord.ui.View):
    def __init__(self):
        self.dagpi = Client(config["API_KEYS"]["DAGPI_KEY"])
        self.counter = 0
        super(RightButton, self).__init__()

    @discord.ui.button(emoji="<:delete:912359260954984459>", style=discord.ButtonStyle.red)
    async def delete(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.defer()
        await interaction.delete_original_message()

    @discord.ui.button(emoji="<:right:912268383179919360>", style=discord.ButtonStyle.blurple)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.counter += 1
        if self.counter == 10:
            button.disabled = True
            await interaction.message.edit(view=self)
        await interaction.response.defer()
        waifu_data = await self.dagpi.waifu()
        waifu_picture = waifu_data["display_picture"]
        waifu_name = waifu_data["name"]
        waifu_site = waifu_data["url"]
        waifu_appeared_in = waifu_data["appearances"][0]['name']
        waifu_original_name = waifu_data["original_name"] or "N/A"
        embed = discord.Embed(title=f"<:okawaiikoto:998161222497226803> Random Waifu",
                              description=f"Name - {waifu_name}\nOriginal Name - {waifu_original_name}\nAppeared In - {waifu_appeared_in}",
                              url=waifu_site, timestamp=interaction.created_at, color=discord.Color.magenta())
        embed.set_footer(text=f"The colors are about more than just looks • Page {self.counter}/10", icon_url=interaction.user.display_avatar)
        embed.set_image(url=waifu_picture)
        await interaction.message.edit(embed=embed)


class Miscs(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.dagpi = Client(config["API_KEYS"]["DAGPI_KEY"])

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
                discord.ui.Button(label="PNG", style=discord.ButtonStyle.url, url=str(avatar_png),
                                  emoji=self.client.get_emoji(995519549057282108))
            )
            buttons.add_item(
                discord.ui.Button(label="JPG", style=discord.ButtonStyle.url, url=str(avatar_jpg),
                                  emoji=self.client.get_emoji(995519549057282108))
            )
            buttons.add_item(
                discord.ui.Button(label="WEBP", style=discord.ButtonStyle.url, url=str(avatar_webp),
                                  emoji=self.client.get_emoji(995519549057282108))
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

            embed = discord.Embed(title=f"{member_nickname if member_nickname is not None else member_name}'s Profile",
                                  description="<:damn:993688550119850015> *A nice profile you got kid!*",
                                  timestamp=interaction.created_at, color=member.color)
            embed.set_footer(text="*Nitro is checked based on user's pfp", icon_url=interaction.user.display_avatar)
            embed.set_thumbnail(url=member_avatar_url)
            embed.add_field(name="<:lilgrux:995515614275829760> Name", value=member_name)
            embed.add_field(name="<:lilgrux:995515614275829760> ID", value=member_id)
            embed.add_field(name="<:top:995516251357073480> Top Role", value=member_top_role)
            embed.add_field(name="<a:mcclock:995517509430161498> Joined At",
                            value=f"<t:{member_joined_at}:F>\n(<t:{member_joined_at}:R>)")
            embed.add_field(name="<a:mcclock:995517509430161498> Created At",
                            value=f"<t:{member_created_at}:F>\n(<t:{member_created_at}:R>)")
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

    @app_commands.command(name="waifu", description="Get a random waifu")
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    async def get_random_waifu(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            waifu_data = await self.dagpi.waifu()
            waifu_picture = waifu_data["display_picture"]
            waifu_name = waifu_data["name"]
            waifu_site = waifu_data["url"]
            waifu_appeared_in = waifu_data["appearances"][0]['name']
            waifu_original_name = waifu_data["original_name"] or "N/A"
            embed = discord.Embed(title=f"<:okawaiikoto:998161222497226803> Random Waifu",
                                  description=f"Name - {waifu_name}\nOriginal Name - {waifu_original_name}\nAppeared In - {waifu_appeared_in}",
                                  url=waifu_site, timestamp=interaction.created_at, color=discord.Color.magenta())
            embed.set_footer(text="The colors are about more than just looks • Page 0/10", icon_url=interaction.user.display_avatar)
            embed.set_image(url=waifu_picture)
            view = RightButton()
            await interaction.followup.send(embed=embed, view=view)
        except:
            error_logger.error("An error occurred while running waifu command:- ", exc_info=True)

    @get_random_waifu.error
    async def on_get_random_waifu_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(embed=discord.Embed(title="<:hellno:871582891585437759> Rate Limited", description="You're on Cooldown! Please wait `5.0` seconds before running this command again.", color=discord.Color.blurple(), timestamp=interaction.created_at).set_footer(text="Dude, slow down...Take a chill pill"))


async def setup(client):
    await client.add_cog(Miscs(client))
