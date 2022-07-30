import discord, asyncpg
from discord.ext import commands
from discord import app_commands
from customs.log import AuroraLogger

error_logger = AuroraLogger('AuroraErrorLog', 'logs/errors.log')


class Todo(commands.GroupCog, name="todo"):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="add", description="Adds a task to your todo")
    async def add_task(self, interaction: discord.Interaction, task: str):
        try:
            data = await self.client.database.fetch_row("SELECT task FROM todo WHERE user_id = $1", interaction.user.id)
            if data is None:
                values: tuple = (interaction.user.id, [task])
                await self.client.database.execute("INSERT INTO todo(user_id, task) VALUES ($1, $2)", values[0],
                                                   values[1])
                await interaction.response.send_message(f"Added task `#1`: `{task}`")
            elif data is not None:
                data = await self.client.database.fetch_row("SELECT task FROM todo WHERE user_id = $1",
                                                            interaction.user.id)
                length = len(data[0])
                formatted_values: list = data[0]
                formatted_values.append(task)
                # print(formatted_values)
                await self.client.database.execute("UPDATE todo set task = $1 WHERE user_id = $2", formatted_values,
                                                   interaction.user.id)

                await interaction.response.send_message(f"Added task `#{length + 1}`: `{task}`")

        except:
            error_logger.error("An error occurred while running todo[add] command:- ", exc_info=True)

    @app_commands.command(name="view", description="Shows your todo list")
    async def view_tasks(self, interaction: discord.Interaction):
        get_list = await self.client.database.fetch_row("SELECT task FROM todo WHERE user_id = $1", interaction.user.id)
        tasks = get_list[0]
        formatted_data = []
        if len(tasks) == 0:
            todo = "```markdown\n0. N/A```"
        elif len(tasks) >= 1:
            for i, k in enumerate(tasks, start=1):
                formatted_data.append(f"{i}. {k}")
            raw = '\n'.join(formatted_data)
            todo = f"```markdown\n{raw}```"
            embed = discord.Embed(title=f"{interaction.user.name}'s Todo", description=todo,
                                  color=discord.Color.brand_green(), timestamp=interaction.created_at)
            embed.set_thumbnail(
                url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/GNOME_Todo_icon_2019.svg/1200px-GNOME_Todo_icon_2019.svg.png")
            embed.set_footer(text="It is the southern cousin to the aurora borealis.",
                             icon_url=interaction.user.display_avatar)
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="remove", description="Remove a todo from the list")
    async def remove_task(self, interaction: discord.Interaction, task_number: int):
        # Get the number of the todo. remove it from the corresponding position of the todo from the list and update it.
        pass


async def setup(client):
    await client.add_cog(Todo(client))
