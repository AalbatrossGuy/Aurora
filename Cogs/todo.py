import discord
from discord import app_commands
from discord.ext import commands
from customs.log import AuroraLogger

error_logger = AuroraLogger('AuroraErrorLog', 'logs/errors.log')


# VIEW
class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="✓", style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Confirming...", ephemeral=True)
        self.value = True
        self.stop()

    @discord.ui.button(label="✕", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Cancelling...", ephemeral=True)
        self.value = False
        self.stop()


class Todo(commands.GroupCog, name="todo"):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="add", description="Adds a task to your todo")
    @app_commands.describe(
        task="The task that you want to add to your todo list"
    )
    async def add_task(self, interaction: discord.Interaction, task: str):
        try:
            data = await self.client.database.fetch_row("SELECT task FROM todo WHERE user_id = $1", interaction.user.id)
            if data is None:
                values: tuple = (interaction.user.id, [task])
                await self.client.database.execute("INSERT INTO todo(user_id, task) VALUES ($1, $2)", values[0],
                                                   values[1])
                await interaction.response.send_message(f"<:todo:1003109477375037500> Added task `#1`: `{task}`")
            elif data is not None:
                data = await self.client.database.fetch_row("SELECT task FROM todo WHERE user_id = $1",
                                                            interaction.user.id)
                length = len(data[0])
                formatted_values: list = data[0]
                formatted_values.append(task)
                # print(formatted_values)
                await self.client.database.execute("UPDATE todo set task = $1 WHERE user_id = $2", formatted_values,
                                                   interaction.user.id)

                await interaction.response.send_message(
                    f"<:todo:1003109477375037500> Added task `#{length + 1}`: `{task}`")

        except:
            error_logger.error("An error occurred while running todo[add] command:- ", exc_info=True)

    @app_commands.command(name="view", description="Shows your todo list")
    async def view_tasks(self, interaction: discord.Interaction):
        try:
            try:
                get_list = await self.client.database.fetch_row("SELECT task FROM todo WHERE user_id = $1", interaction.user.id)
                tasks = get_list[0]
                formatted_data = []
                if len(tasks) == 0:
                    await interaction.response.send_message(
                        "<:hellno:871582891585437759> You do not have any task set in your TODO list!")
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
            except TypeError:
                await interaction.response.send_message(
                    "<:hellno:871582891585437759> You do not have any task set in your TODO list!")

        except:
            error_logger.error("An error occurred while running todo[view] command:- ", exc_info=True)

    @app_commands.command(name="remove", description="Remove a todo from the list")
    @app_commands.describe(
        task_number="The task number of the task which you want to remove."
    )
    async def remove_task(self, interaction: discord.Interaction, task_number: int):
        # Get the number of the todo. remove it from the corresponding position of the todo from the list and update it.
        try:
            get_list = await self.client.database.fetch_row("SELECT task FROM todo WHERE user_id = $1",
                                                            interaction.user.id)
            raw_list: list = get_list[0]

            if task_number > len(raw_list) or task_number < 1:
                await interaction.response.send_message("Please give a valid task number!")
            else:
                raw_list.pop(task_number - 1)
                await self.client.database.execute("UPDATE todo SET task = $1 WHERE user_id = $2", raw_list,
                                                   interaction.user.id)
                await interaction.response.send_message(
                    f"<a:tick:1003110258870333520> Successfully removed task `#{task_number}` from your todo list <:todo:1003109477375037500>")
        except:
            error_logger.error("An error occurred while running todo[remove] command:- ", exc_info=True)

    @app_commands.command(name="delete", description="Delete your current todo list")
    async def delete_list(self, interaction: discord.Interaction):
        view = Confirm()
        ConfirmationEmbed = discord.Embed(title="<a:tick:1003110258870333520> Confirmation", description="Are you sure that you want to delete your TODO list? This action cannot be undone.", timestamp=interaction.created_at, color=discord.Color.blurple())
        await interaction.response.send_message(embed=ConfirmationEmbed, view=view)
        await view.wait()

        if view.value is None:
            await interaction.edit_original_message(
                embed=discord.Embed(title="<:pandacop:831800704372178944> Confirmation timed out!",
                                    description="**You did not click on any of the buttons hence the confirmation timed out.**",
                                    color=discord.Colour.red(), timestamp=interaction.created_at))
        elif view.value:
            await self.client.database.execute("DELETE FROM todo WHERE user_id = $1", interaction.user.id)
            await interaction.edit_original_message(content="<a:tick:1003110258870333520> Successfully Deleted your TODO list!", embed=None, view=None)


async def setup(client):
    await client.add_cog(Todo(client))
