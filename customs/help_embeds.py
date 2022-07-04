import discord
import json

file = open("config.json", mode="r")
config = json.loads(file.read())
avatar = config["METADATA"]["AURORA_LOGO_LINK"]

# MODERATION EMBED
embedModeration = discord.Embed(title="<:mod:992770697921310780> Moderation Category", colour=discord.Colour.dark_green())
embedModeration.set_footer(text="<> = Required | [] = Optional", icon_url=avatar)
embedModeration.add_field(name="• `help`", value="Shows this message", inline=False)
embedModeration.add_field(name="• `clear [amount=10]`", value="Deletes Channel Messages of the amount specified.", inline=False)
embedModeration.add_field(name="• `kick <member> [reason]`", value="Kicks member from the guild.", inline=False)
embedModeration.add_field(name="• `ban <member> [reason]`", value="Bans member from the guild.", inline=False)
embedModeration.add_field(name="• `unban <member>`", value="Unbans a banned user from the server. Either pass in username#123 or ID.", inline=False)

# SETTINGS EMBED
embedSettings = discord.Embed(title="<:settings:957629477087760436> Settings Category", color=discord.Colour.dark_gold())
embedSettings.set_footer(text="<> = Required | [] = Optional", icon_url=avatar)
embedSettings.add_field(name="• `about`", value="Shows information about the bot", inline=False)
embedSettings.add_field(name="• Coming Soon...", value="Coming soon...")

# UTILITY EMBED
embedUtility = discord.Embed(title="<:utilitywhat:992784837205311498> Utility Category", color=discord.Colour.dark_teal())
embedUtility.set_footer(text="<> = Required | [] = Optional", icon_url=avatar)
embedUtility.add_field(name="• `avatar [member]`", value="Shows the avatar of the member mentioned. If nothing is provided, the avatar of the author is shown.", inline=False)
embedUtility.add_field(name="• Coming Soon...", value="Coming soon ...")
