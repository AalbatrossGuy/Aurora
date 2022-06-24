import discord, logging, json, os, asyncio
from discord.ext import commands
from typing import Optional, Literal

file = open("config.json", "r")
config = json.loads(file.read())
TEST_GUILD = discord.Object(id=config["Aurora"]["TEST_GUILD"])
handler = logging.FileHandler(filename="logs/aurora.log", encoding="utf-8", mode="w")

client = commands.AutoShardedBot(command_prefix="!", case_insensitive=True, intents=discord.Intents.default())


@client.command(name="sync")
@commands.is_owner()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object],
               spec: Optional[Literal["~", "*"]] = None) -> None:
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
    for filename in os.listdir('./Cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'Cogs.{filename[:-3]}')

    await client.start(config["Aurora"]["TOKEN"])


client.tree.copy_global_to(guild=TEST_GUILD)
asyncio.run(main())
