import discord, json, re, time
from discord.ext import commands
from discord import app_commands
from customs.log import AuroraLogger
from customs.rpg.entity import Player, Spider, PlayerData

err_log = AuroraLogger("AuroraErrorLog", "logs/errors.log")


class RPG(commands.GroupCog, name="rpg"):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="start", description="Start your rpg adventure!")
    @app_commands.describe(
        player_name="Set your character's name. It shouldn't be more than 15 characters."
    )
    async def register_user(self, interaction: discord.Interaction, player_name: str) -> None:
        try:
            if len(player_name) > 15:
                await interaction.response.send_message(
                    "Name of the player cannot be more than 15 characters in length. (Needs edit)")
            else:
                # await interaction.response.send_message("Done")
                try:
                    data = await self.client.database.fetch_row("SELECT username FROM rpg WHERE user_id = $1",
                                                                interaction.user.id)
                    print(data)
                    if data is None:
                        new_player = json.dumps(Player("Player", 1, 50, 50, 30, 50, 0, 100, player_name).raw())
                        values: tuple = (interaction.user.id, player_name, new_player, json.dumps(PlayerData(0).raw()))
                        print('got values')
                        await self.client.database.execute(
                            "INSERT INTO rpg(user_id, username, base_stats, player_data) VALUES ($1, $2, $3, $4)", values[0], values[1],
                            values[2], values[3])
                        print('executed')
                        embed = discord.Embed(title=f"Welcome to (Name of the Game)",
                                              description=f"_A nice introductory text in italics for first time users_",
                                              timestamp=interaction.created_at, color=discord.Color.magenta())
                        embed.set_footer(text="Footer text here",
                                         icon_url=interaction.user.display_avatar
                                         )
                        embed.set_thumbnail(
                            url="https://cdn.discordapp.com/attachments/1035722927137632307/1035778861327200316/unknown.png")
                        embed.set_image(
                            url="https://cdn.discordapp.com/attachments/1035722927137632307/1035778954734338068/unknown.png")
                        # await interaction.response.send_message("Your Journey starts here! (Needs edit)")
                        await interaction.response.send_message(embed=embed)
                    elif data is not None:
                        print('executed #2')
                        await interaction.response.send_message("You've already started your journey! (Needs edit)")
                    # TODO: add unique violation error.
                except Exception as e:
                    print(f"Exception: {e}")
        except:
            err_log.error("An error occurred while running rpg[start] command:- ", exc_info=True)

    @app_commands.command(name="profile", description="View your profile.")
    async def show_profile(self, interaction: discord.Interaction):
        try:
            # profile = Player()
            data = await self.client.database.fetch_row("SELECT username FROM rpg WHERE user_id = $1",
                                                        interaction.user.id)

            if data is not None:
                player_data = await self.client.database.fetch_row("SELECT base_stats FROM rpg WHERE user_id = $1",
                                                                   interaction.user.id)
                player_data = json.loads(player_data[0])
                # await interaction.response.send_message(player_data)
                embed = discord.Embed(
                    title=f"{player_data['name']}'s profile", timestamp=interaction.created_at,
                    color=discord.Color.random()
                )
                embed.add_field(name="Name", value=player_data["name"])
                embed.add_field(name="Level", value=player_data["level"])
                embed.add_field(name="Experience", value=f"{player_data['current_xp']}/{player_data['max_xp']}")
                embed.add_field(name="Health",
                                value=f"{player_data['current_health']}/{player_data['max_health']}({int(player_data['health_percentage'])}%)")
                embed.add_field(name="Attack", value=player_data["attack"])
                embed.add_field(name="Defence", value=player_data["defense"])
                embed.set_thumbnail(
                    url="https://cdn.discordapp.com/attachments/1035722927137632307/1035778861327200316/unknown.png")
                await interaction.response.send_message(embed=embed)
            if data is None:
                await interaction.response.send_message("Player not registered.")

        except:
            err_log.error("An error occurred while running rpg[profile] command:- ", exc_info=True)

    @app_commands.command(name="raw")
    async def test_duel(self, interaction: discord.Interaction):
        await interaction.response.send_message(Spider().raw())

    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.command(name="explore", description="Wonder into new territories.")
    async def navigation(self, interaction: discord.Interaction):
        start = time.time()
        try:
            # await interaction.response.send_message("Cooldown test")
            get_player = await self.client.database.fetch_row("SELECT username FROM rpg WHERE user_id = $1", interaction.user.id)

            if get_player is not None:
                player_data = await self.client.database.fetch_row("SELECT player_data FROM rpg WHERE user_id = $1", interaction.user.id)
                end = time.time()
                proc_time = (end-start).__format__('0.3f')
                await interaction.response.send_message(f"Current Player Position: {json.loads(player_data[0])['curr_pos']}\nProcess finished in: `{proc_time}`s")
        except:
            err_log.error("An error occurred while running rpg[explore] command:- ", exc_info=True)

    @navigation.error
    async def on_test_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.CommandOnCooldown):
            interval = '.'.join(re.findall(r'\d+', str(error)))
            await interaction.response.send_message(f"❌ Hey! You've walked quite a lot. Take a breather for `{interval}s`", ephemeral=True)


async def setup(client):
    await client.add_cog(RPG(client))
