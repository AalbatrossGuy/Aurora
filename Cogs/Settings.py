import discord
from discord.ext import commands


#
class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client


#
#     @interactions.extension_command(
#         name="about",
#         description="Shows information about the bot.",
#     )
#     async def _bot_information(self, ctx):
#         bot = interactions.User(**await self.client._http.get_self())._json
#         #client = interactions.User(**await self.client._http.get_self())
#         guilds = len(self.client._http.cache.self_guilds.values)
#         name = bot['username'] + '#' + bot['discriminator']
#         # avatar = client.avatar_url
#         id = bot['id']
#         mfa_enabled = bot['mfa_enabled']
#         with open('config.json') as file:
#             file = json.load(file)
#             version = file['Aurora']['VERSION']
#             github = file['METADATA']['GITHUB_REPOSITORY']
#             license = file['METADATA']['LICENSE']
#             lead_dev = file['Aurora']['DEVELOPERS'][0]['DISCORD']
#             co_dev = file['Aurora']['DEVELOPERS'][1]['DISCORD']
#
#         proc = Process()
#         with proc.oneshot():
#             mem_total = virtual_memory().total / (1024**2)
#             thread_counts = proc.num_threads()
#             cpus = cpu_percent()
#             cpu = f"{cpus}%\n({thread_counts} Threads)"
#             mem_of_total = proc.memory_percent()
#             mem_usage = mem_total * (mem_of_total / 100)
#             p = pathlib.Path('./')
#             cm = cr = fn = cl = ls = fc = 0
#             for f in p.rglob('*.py'):
#                 if str(f).startswith("venv"):
#                     continue
#                 fc += 1
#                 with f.open(encoding='utf8') as of:
#                     for l in of.readlines():
#                         l = l.strip()
#                         if l.startswith('class'):
#                             cl += 1
#                         if l.startswith('def'):
#                             fn += 1
#                         if l.startswith('async def'):
#                             cr += 1
#                         if '#' in l:
#                             cm += 1
#                         ls += 1
#
#         # Embed
#
#         fields = [
#             interactions.EmbedField(name="📛 Name", value=name, inline=True),
#             interactions.EmbedField(name="🆔 ID", value=f"{id[:8]}...", inline=True),
#             interactions.EmbedField(name="<:bot:957452828157313096> Version", value=version, inline=True),
#             interactions.EmbedField(name="<:python:911833219056402504> Python Version", value=python_version(), inline=True),
#             interactions.EmbedField(name="<:cpu1:957924151753068544> CPU", value=cpu, inline=True),
#             interactions.EmbedField(name="<:ram:911834876020408381> Memory Usage", value=f"{mem_usage:,.3f} / {mem_total:,.0f} MiB ({mem_of_total:.0f}%)", inline=True),
#             interactions.EmbedField(name="📝 Lines of Code", value=f"{ls:,}", inline=True),
#             interactions.EmbedField(name="<:servers:957628143785619496> Guilds", value=guilds, inline=True),
#             interactions.EmbedField(name="📂 Files", value=fc, inline=True),
#             interactions.EmbedField(name="<:pythonsus:911840562510975036> Functions", value=fn, inline=True),
#             interactions.EmbedField(name="<:pythonsus:911840562510975036> Comments", value=f"{cm:,}", inline=True),
#             interactions.EmbedField(name="<:developer:911835252324986980> Lead Developer", value=lead_dev, inline=True),
#             interactions.EmbedField(name="<:developer:911835252324986980> Co-Developer", value=co_dev, inline=True),
#             interactions.EmbedField(name="License", value=license, inline=False)
#         ]
#
#         embed = createEmbed(title="About AuroraBot", color=15844367, footer_text="A Norwegian scientist was the first to explain the aurora phenomenon.",
#             footer_icon_url="https://media.discordapp.net/attachments/831369746855362590/954622807302615050/Aurora_Big.png?width=747&height=747",
#             thumbnail_url="https://media.discordapp.net/attachments/831369746855362590/954622807302615050/Aurora_Big.png?width=747&height=747",
#             fields=fields
#         )
#
#         github = interactions.Button(
#             style=interactions.ButtonStyle.LINK,
#             label="Github",
#             emoji=await self.client._http.get_guild_emoji(guild_id=763737869482328074, emoji_id=851778689648689152),
#             url="https://github.com/AalbatrossGuy/Aurora"
#         )
#
#         dev_1 = interactions.Button(
#             style=interactions.ButtonStyle.LINK,
#             label="Dev #1",
#             emoji=await self.client._http.get_guild_emoji(guild_id=903225083072495646, emoji_id=911835252324986980),
#             url="https://github.com/AalbatrossGuy"
#         )
#
#         dev_2 = interactions.Button(
#             style=interactions.ButtonStyle.LINK,
#             label="Dev #2",
#             emoji=await self.client._http.get_guild_emoji(guild_id=903225083072495646, emoji_id=911835252324986980),
#             url="https://github.com/Catto-YFCN"
#         )
#
#         # await ctx.send(f"{name}, {bio}, {id}, {mfa_enabled}, {version}, {github},  {license}, {devs}")
#         await ctx.send(embeds=embed, components=[github, dev_1, dev_2])
#
#
async def setup(client):
    await client.add_cog(Settings(client))
