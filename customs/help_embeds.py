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
embedUtility.add_field(name="• meminfo [member]", value="Shows information of the member from the current guild. If nothing is provided, the information of the author is shown.", inline=False)

# IMAGE EMBED
embedImage = discord.Embed(title="<:photo:995519248006905896> Image Category", color=discord.Color.dark_magenta())
embedImage.set_footer(text="<> = Required | [] = Optional", icon_url=avatar)
embedImage.add_field(name="• b_w [member] [attachment]", value="Gives a black and white version of the [member]'s avatar or the image given as an [attachment].", inline=False)
embedImage.add_field(name="• negative [member] [attachment]", value="Gives an inverted version of the [member]'s avatar or the image given as an [attachment].", inline=False)
embedImage.add_field(name="• pixel [member] [attachment]", value="Gives a pixelated version of the [member]'s avatar or the image given as an [attachment].", inline=False)
embedImage.add_field(name="• colors [member] [attachment]", value="Gives the constituent colors of the [member]'s avatar or the image given as an [attachment].", inline=False)
embedImage.add_field(name="• triggered [member] [attachment]", value="Gives a triggered GIF version of the [member]'s avatar or the image given as an [attachment].", inline=False)
embedImage.add_field(name="• expand [member] [attachment]", value="Gives a expanding GIF version of the [member]'s avatar or the image given as an [attachment].", inline=False)
embedImage.add_field(name="• wasted [member] [attachment]", value="Gives a wasted GIF version of the [member]'s avatar or the image given as an [attachment].", inline=False)
embedImage.add_field(name="• petpat [member] [attachment]", value="Gives a petpat GIF version of the [member]'s avatar or the image given as an [attachment].", inline=False)
embedImage.add_field(name="• bonk [member] [attachment]", value="Gives a bonk GIF version of the [member]'s avatar or the image given as an [attachment].", inline=False)
embedImage.add_field(name="• hog [member] [attachment]", value="Gives the histogram of oriented gradients, hog for short, of the [member]'s avatar or the image given as an [attachment].", inline=False)
embedImage.add_field(name="• blur <blur_radius> [member] [attachment]", value="Gives a blurred version of the [member]'s avatar or the image given as an [attachment] with a radius of <blur_radius>.", inline=False)
embedImage.add_field(name="• pixel [member] [attachment]", value="Gives a pixelated version of the [member]'s avatar or the image given as an [attachment].", inline=False)
embedImage.add_field(name="• rgb [member] [attachment]", value="Gives the rgb graph of the [member]'s avatar or the image given as an [attachment].", inline=False)
embedImage.add_field(name="• lego [member] [attachment]", value="Gives a lego-ed version of the [member]'s avatar or the image given as an [attachment].", inline=False)
embedImage.add_field(name="• album [member] [attachment]", value="Gives a song album version of the [member]'s avatar or the image given as an [attachment].", inline=False)

# SEARCH EMBED
embedSearch = discord.Embed(title="<:search:997798789354107030> Search Category", color=discord.Color.green())
embedSearch.set_footer(text="<> = Required | [] = Optional", icon_url=avatar)
embedSearch.add_field(name="• movie <query>", value="Gives information related to a movie, i.e., the <query>", inline=False)
embedSearch.add_field(name="• anime <query>", value="Gives information related to an anime, i.e., the <query>", inline=False)