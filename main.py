import discord, logging, json, os, asyncio
import discord.ext.commands
from customs.customs import version_info
from discord.ext import commands
from typing import Optional, Literal
from customs.log import AuroraLogger

logger = AuroraLogger('AuroraInfoLog', 'logs/info.log')
error_logger = AuroraLogger('AuroraErrorLog', 'logs/errors.log')

file = open("config.json", "r")
config = json.loads(file.read())
TEST_GUILD = discord.Object(id=config["Aurora"]["TEST_GUILD"])
handler = logging.FileHandler(filename="logs/info.log", encoding="utf-8", mode="w")

intents = discord.Intents.default()
intents.message_content = True
client = commands.AutoShardedBot(command_prefix="!", case_insensitive=True, intents=intents)


@client.command(name="sync")
@commands.is_owner()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object],
               spec: Optional[Literal["~", "*"]] = None) -> None:
    try:
        if not guilds:
            if spec == "~":
                fmt = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                fmt = await ctx.bot.tree.sync(guild=ctx.guild)
            else:
                fmt = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(fmt)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        fmt = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                fmt += 1

        await ctx.send(f"Synced the tree to {fmt}/{len(guilds)} guilds.")
    except:
        error_logger.error("Error occurred while executing !sync:- ", exc_info=True)


@client.tree.command(name="ping", description="Shows the websocket latency and database latency.")
async def show_latency(interaction: discord.Interaction):
    # ws ping
    embed = discord.Embed(title=":ping_pong: Aurora's Latency", color=discord.Colour.dark_gold(),
                          timestamp=interaction.created_at)
    embed.add_field(name=":green_heart: WS Ping", value=f"```py\n{round(client.latency * 1000)} ms```")
    embed.set_footer(text="A Norwegian scientist was the first to explain the aurora phenomenon.",
                     icon_url=interaction.user.display_avatar)
    embed.set_thumbnail(
        url="https://64.media.tumblr.com/be43242341a7be9d50bb2ff8965abf61/tumblr_o1ximcnp1I1qf84u9o1_1280.gif")
    await interaction.response.send_message(embed=embed)


async def main():
    cogs_count = 0
    total_count = 0
    try:
        for filename in os.listdir('./Cogs'):
            if filename.endswith('.py'):
                total_count += 1
                try:
                    await client.load_extension(f'Cogs.{filename[:-3]}')
                except discord.ext.commands.ExtensionFailed:
                    cogs_count -= 1
                    error_logger.error(f"Error occurred while loading cogs:- ", exc_info=True)
                cogs_count += 1
        logger.info(f"Successfully Loaded {cogs_count}/{total_count} Cogs.")
        try:
            await client.login(config["Aurora"]["TOKEN"])
            bot_name = client.user.name
            bot_discriminator = client.user.discriminator
            logger.info(
                f"Logged into discord as {bot_name}#{bot_discriminator}. Last commit ran on {version_info()[1]}")
        except discord.LoginFailure or discord.HTTPException:
            error_logger.critical("LOGIN TO DISCORD UNSUCCESSFUL :-", exc_info=True)
            exit()
        await client.connect()
    except Exception as e:
        if e != KeyboardInterrupt:
            error_logger.error(f"Error occurred while starting the bot:- ", exc_info=True)


client.tree.copy_global_to(guild=TEST_GUILD)
asyncio.run(main())
