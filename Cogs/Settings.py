import discord, time, pathlib, json
from platform import python_version
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
from psutil import Process, virtual_memory
from customs.log import AuroraLogger
from customs.customs import get_uptime

# LOGGER
error_logger = AuroraLogger("AuroraErrorLog", "logs/errors.log")


class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="about", description="Shows information about the bot.")
    async def _bot_information(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(title="About Me", colour=discord.Colour.dark_magenta(),
                                  timestamp=interaction.created_at)
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/910897237037555774/911829151588167700/about_me.jpg")
            embed.set_footer(text="The oldest known record of an aurora date back to 2600 BC",
                             icon_url=interaction.user.display_avatar)
            proc = Process()
            with proc.oneshot():
                uptime = timedelta(seconds=time.time() - proc.create_time())
                cpu_time = timedelta(seconds=(cpu := proc.cpu_times()).system + cpu.user)
                mem_total = virtual_memory().total / (1024 ** 2)
                mem_of_total = proc.memory_percent()
                mem_usage = mem_total * (mem_of_total / 100)
                p = pathlib.Path('./')
                cm = cr = fn = cl = ls = fc = 0
                for f in p.rglob('*.py'):
                    if str(f).startswith("venv"):
                        continue
                    fc += 1
                    with f.open(encoding='utf8') as of:
                        for l in of.readlines():
                            l = l.strip()
                            if l.startswith('class'):
                                cl += 1
                            if l.startswith('def'):
                                fn += 1
                            if l.startswith('async def'):
                                cr += 1
                            if '#' in l:
                                cm += 1
                            ls += 1

            embed.add_field(name="<:python:911833219056402504> Python version", value=python_version(), inline=True)
            embed.add_field(name="<:dpy:911833820028883014> discord.py version", value=discord.__version__, inline=True)
            embed.add_field(name="<:time:959328643987959818> Uptime", value=f"<t:{int(get_uptime().timestamp())}:R>",
                            inline=True)
            embed.add_field(name="<:ram:911834876020408381> Memory usage",
                            value=f"{mem_usage:,.3f} / {mem_total:,.0f} MiB ({mem_of_total:.0f}%)", inline=True)
            embed.add_field(name="<:servers:957628143785619496> Guilds",
                            value=f"{len(list(self.client.guilds))}", inline=True)
            embed.add_field(name="📝 Lines Of Code", value=f"{ls:,}", inline=True)
            embed.add_field(name="📂 Files", value=fc, inline=True)
            embed.add_field(name="<:pythonsus:911840562510975036> Functions", value=fn, inline=True)
            embed.add_field(name="<:pythonsus:911840562510975036> Comments", value=f"{cm:,}", inline=True)
            embed.add_field(name="<:developer:911835252324986980> Developer", value="AalbatrossGuy#5129", inline=True)
            embed.add_field(name="<:tester:911835692945010720> Official Tester",
                            value="Your Friendly Cat Neighbor#3521", inline=True)
            embed.add_field(name='<:pc:911836792603414528> Hosted By', value="4ngel🍁#2769", inline=True)

            buttons = discord.ui.View()
            with open("config.json", mode="r") as file:
                file = json.loads(file.read())
                buttons.add_item(
                    discord.ui.Button(label="Github", style=discord.ButtonStyle.url,
                                      url=file["METADATA"]["GITHUB_REPOSITORY"],
                                      emoji=self.client.get_emoji(851778689648689152))
                )
            buttons.add_item(
                discord.ui.Button(label="Developer", style=discord.ButtonStyle.url,
                                  url=file["Aurora"]["DEVELOPERS"][0]["GITHUB"],
                                  emoji=self.client.get_emoji(911835252324986980))
            )
            buttons.add_item(
                discord.ui.Button(label="Tester", style=discord.ButtonStyle.url,
                                  url=file["Aurora"]["DEVELOPERS"][1]["GITHUB"],
                                  emoji=self.client.get_emoji(911835692945010720))
            )

            await interaction.response.send_message(embed=embed, view=buttons)
        except:
            error_logger.error("An error occurred while running about command:- ", exc_info=True)


async def setup(client):
    await client.add_cog(Settings(client))
