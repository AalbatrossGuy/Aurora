from typing import Tuple, Any

import discord, aiohttp, json
from discord import app_commands
from discord.ext import commands
from requests.utils import requote_uri
from customs.log import AuroraLogger

file = open("config.json", "r")
config = json.loads(file.read())
error_logger = AuroraLogger("AuroraErrorLog", "logs/errors.log")


# CUSTOM FUNCTIONS
async def get_movie_info(query: str, count: int, family_friendly: bool = True) -> dict | str:
    base_url = "https://api.themoviedb.org/3/search/movie?api_key="
    api_key = config["API_KEYS"]["MOVIE_API"]
    query = requote_uri(query)
    url = base_url + api_key + "&language=en-US&query=" + query + "&page=1&include_adult=" + str(family_friendly)

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as data:
            result = await data.json()
            # print(f"Length of total value : {len(result['results'])}")
            try:
                return result["results"][count]
            except IndexError:
                raise IndexError


# VIEWS
class Movements(discord.ui.View):
    def __init__(self, query: str, family_friendly: bool):
        super().__init__()
        self.value = None
        self.counter = 0
        self.query = query
        self.nsfw_check = family_friendly

    @discord.ui.button(emoji="<:left:912268440029528075>", style=discord.ButtonStyle.blurple, disabled=True)
    async def before(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.counter -= 1
        await interaction.response.defer()
        data = await get_movie_info(query=self.query, family_friendly=self.nsfw_check, count=self.counter)
        if self.counter == 0 or self.counter <= 0:
            button.disabled = True
            await interaction.message.edit(view=self)
        if self.next.disabled is True:
            self.next.disabled = False
            await interaction.message.edit(view=self)
        try:
            nsfw = data["adult"] or "N/A"
            language = data["original_language"] or "N/A"
            original_title = data["original_title"] or "N/A"
            overview = data["overview"] or "N/A"
            popularity = data["popularity"] or "N/A"
            if data["poster_path"] is not None:
                poster = "https://image.tmdb.org/t/p/w500" + data["poster_path"]
            else:
                poster = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/832px-No-Image-Placeholder.svg.png"
            release_date = data["release_date"] or "N/A"
            title = data["title"] or "N/A"
            vote_average = data["vote_average"] or "N/A"
            vote_count = data["vote_count"] or "N/A"
            embed = discord.Embed(title=original_title, color=discord.Color.blurple(), timestamp=interaction.created_at)
            embed.set_footer(text=f"The most common aurora colours are red and green • Page {self.counter}",
                             icon_url=interaction.user.display_avatar)
            embed.set_image(url=poster)
            embed.add_field(name="<:owdcinema:996728312510562365> Title", value=title, inline=True)
            embed.add_field(name="<:owdcinema:996728312510562365> Language", value=language, inline=True)
            embed.add_field(name="<:adultsonly:996729151673352222> Is Nsfw?", value=nsfw, inline=True)
            embed.add_field(name="<:heppy:996729953259356252> Popularity", value=popularity, inline=True)
            embed.add_field(name="<a:mcclock:995517509430161498> Release Date", value=release_date, inline=True)
            embed.add_field(name="<:owdcinema:996728312510562365> Movie Overview", value=overview, inline=False)
            embed.add_field(name="<:pepeupvote:996729520893722715>Vote Average", value=vote_average, inline=True)
            embed.add_field(name="<:pepeupvote:996729520893722715> Vote Count", value=vote_count, inline=True)
            await interaction.message.edit(embed=embed)
        except IndexError:
            button.disabled = True
            await interaction.followup.edit(embed=discord.Embed(title="No More Info Found :(",
                                                                description="No more information has been found regarding the movie you searched for.",
                                                                color=discord.Color.blurple(),
                                                                timestamp=interaction.created_at), view=self)

    @discord.ui.button(emoji="<:right:912268383179919360>", style=discord.ButtonStyle.blurple)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.counter += 1
        await interaction.response.defer()
        if self.counter != 0 and self.before.disabled is True:
            self.before.disabled = False
            await interaction.message.edit(view=self)

        try:
            data = await get_movie_info(query=self.query, family_friendly=self.nsfw_check, count=self.counter)
            nsfw = data["adult"] or "N/A"
            language = data["original_language"] or "N/A"
            original_title = data["original_title"] or "N/A"
            overview = data["overview"] or "N/A"
            popularity = data["popularity"] or "N/A"
            if data["poster_path"] is not None:
                poster = "https://image.tmdb.org/t/p/w500" + data["poster_path"]
            else:
                poster = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/832px-No-Image-Placeholder.svg.png"
            release_date = data["release_date"] or "N/A"
            title = data["title"] or "N/A"
            vote_average = data["vote_average"] or "N/A"
            vote_count = data["vote_count"] or "N/A"
            embed = discord.Embed(title=original_title, color=discord.Color.blurple(), timestamp=interaction.created_at)
            embed.set_footer(text=f"The most common aurora colours are red and green • Page {self.counter}",
                             icon_url=interaction.user.display_avatar)
            embed.set_image(url=poster)
            embed.add_field(name="<:owdcinema:996728312510562365> Title", value=title, inline=True)
            embed.add_field(name="<:owdcinema:996728312510562365> Language", value=language, inline=True)
            embed.add_field(name="<:adultsonly:996729151673352222> Is Nsfw?", value=nsfw, inline=True)
            embed.add_field(name="<:heppy:996729953259356252> Popularity", value=popularity, inline=True)
            embed.add_field(name="<a:mcclock:995517509430161498> Release Date", value=release_date, inline=True)
            embed.add_field(name="<:owdcinema:996728312510562365> Movie Overview", value=overview, inline=False)
            embed.add_field(name="<:pepeupvote:996729520893722715> Vote Average", value=vote_average, inline=True)
            embed.add_field(name="<:pepeupvote:996729520893722715> Vote Count", value=vote_count, inline=True)
            await interaction.message.edit(embed=embed)
        except IndexError:
            button.disabled = True
            await interaction.message.edit(embed=discord.Embed(title="No More Info Found :(",
                                                               description="No more information has been found regarding the movie you searched for.",
                                                               color=discord.Color.blurple(),
                                                               timestamp=interaction.created_at), view=self)


class Search(commands.GroupCog, name="search"):
    def __init__(self, client):
        self.client = client
        super().__init__()

    @app_commands.command(name="movie", description="Searches for a movie query")
    @app_commands.describe(
        query="The movie to get info on",
        family_friendly="Whether to show nsfw data or not"
    )
    async def movie_info(self, interaction: discord.Interaction, query: str, family_friendly: bool = True):
        try:
            # example url  = https://api.themoviedb.org/3/search/movie?api_key=b4f5becc87666f456bcfc4267c2995e8&language=en-US&query=fast%20and%20furious&page=1&include_adult=false
            # example image url = https://image.tmdb.org/t/p/w500/xxiwm75ADoHu0NCDObRG1AnHi02.jpg --> till w/500 is base url
            # await interaction.response.send_message("movie found", view=view)
            # # await view.wait()
            # await interaction.edit_original_message(content=f"{view.counter}")

            view = Movements(query=query, family_friendly=family_friendly)
            data = await get_movie_info(query=query, count=0)
            nsfw = data["adult"]
            language = data["original_language"]
            original_title = data["original_title"]
            overview = data["overview"]
            popularity = data["popularity"]
            poster = "https://image.tmdb.org/t/p/w500" + data["poster_path"]
            release_date = data["release_date"]
            title = data["title"]
            vote_average = data["vote_average"]
            vote_count = data["vote_count"]
            embed = discord.Embed(title=original_title, color=discord.Color.blurple(), timestamp=interaction.created_at)
            embed.set_footer(text=f"The most common aurora colours are red and green • Page 0",
                             icon_url=interaction.user.display_avatar)
            embed.set_image(url=poster)
            embed.add_field(name="<:owdcinema:996728312510562365> Title", value=title, inline=True)
            embed.add_field(name="<:owdcinema:996728312510562365> Language", value=language, inline=True)
            embed.add_field(name="<:adultsonly:996729151673352222> Is Nsfw?", value=nsfw, inline=True)
            embed.add_field(name="<:heppy:996729953259356252> Popularity", value=popularity, inline=True)
            embed.add_field(name="<a:mcclock:995517509430161498>Release Date", value=release_date, inline=True)
            embed.add_field(name="<:owdcinema:996728312510562365> Movie Overview", value=overview, inline=False)
            embed.add_field(name="<:pepeupvote:996729520893722715> Vote Average", value=vote_average, inline=True)
            embed.add_field(name="<:pepeupvote:996729520893722715> Vote Count", value=vote_count, inline=True)
            await interaction.response.send_message(embed=embed, view=view)

        except:
            error_logger.error(f"Error occurred while running movie_info command:- ", exc_info=True)


async def setup(client):
    await client.add_cog(Search(client))
