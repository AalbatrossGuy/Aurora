import random
from datetime import timezone

import discord, aiohttp, json, kitsu
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
class ControlsMovie(discord.ui.View):
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

    @discord.ui.button(emoji="<:delete:912359260954984459>", style=discord.ButtonStyle.red)
    async def delete(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.defer()
        await interaction.delete_original_message()

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

    @discord.ui.button(emoji="🔖", style=discord.ButtonStyle.grey)
    async def share_embed(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Sending movie info to dm...", ephemeral=True)
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
        user_dm = await interaction.user.create_dm()
        await user_dm.send(embed=embed)


class ControlsAnime(discord.ui.View):
    def __init__(self, query: str):
        self.query = query
        self.counter = 0
        self.kitsu = kitsu.Client()
        super().__init__()

    @discord.ui.button(emoji="<:left:912268440029528075>", style=discord.ButtonStyle.blurple, disabled=True)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.counter -= 1
            await interaction.response.defer()
            search = await self.kitsu.search_anime(self.query, limit=11)
            if self.counter == 0 or self.counter <= 0:
                button.disabled = True
                await interaction.message.edit(view=self)
            if self.next.disabled is True:
                self.next.disabled = False
                await interaction.message.edit(view=self)
            title = search[self.counter].canonical_title
            synopsis = search[self.counter].synopsis or "N/A"
            anime_type = search[self.counter].subtype or "N/A"
            episode_count = search[self.counter].episode_count or "N/A"
            try:
                start_date = f"<t:{int(search[self.counter].start_date.replace(tzinfo=timezone.utc).timestamp())}:F>(<t:{int(search[self.counter].start_date.replace(tzinfo=timezone.utc).timestamp())}:R>)"
            except AttributeError:
                start_date = "N/A"
            try:
                end_date = f"<t:{int(search[self.counter].end_date.replace(tzinfo=timezone.utc).timestamp())}:F>(<t:{int(search[self.counter].end_date.replace(tzinfo=timezone.utc).timestamp())}:R>)"
            except AttributeError:
                end_date = "N/A"
            try:
                rating_rank = search[self.counter].rating_rank
            except TypeError:
                rating_rank = None
            rating_rank = f"**TOP** {rating_rank:,}" if rating_rank is not None else None
            duration = f"{search[self.counter].episode_length // 60} hour(s) and {search[self.counter].episode_length % 60} minutes" if \
            search[self.counter].episode_length is not None else "N/A"
            poster_image = search[self.counter].poster_image(
                _type="large") or "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/832px-No-Image-Placeholder.svg.png"
            status = search[self.counter].status or "N/A"
            embed = discord.Embed(title=title, timestamp=interaction.created_at, color=discord.Color.blurple(),
                                  description=synopsis, url=f"https://kitsu.io/anime/{search[self.counter].id}")
            embed.add_field(name='❓ Type', value=anime_type)
            embed.add_field(name='💽 Episodes', value=episode_count, inline=True)
            embed.add_field(name='<a:time:906880876451876875> Start Date',
                            value=start_date,
                            inline=False)
            embed.add_field(name="<a:time:906880876451876875> End Date", value=end_date,
                            inline=True)
            embed.add_field(name="⏲️ Duration", value=duration, inline=False)
            embed.add_field(name="<a:status:912965228893978634> Status", value=status, inline=True)
            embed.add_field(name="<a:rating:912929196253257778> Rating", value=rating_rank, inline=True)
            embed.set_image(url=poster_image)
            embed.set_footer(text=f"Earth isn’t the only planet with auroras • Page {self.counter}/10",
                             icon_url=interaction.user.display_avatar)
            await interaction.message.edit(embed=embed)

        except IndexError:
            button.disabled = True
            await interaction.message.edit(embed=discord.Embed(title="No More Info Found :(",
                                                               description="No more information has been found regarding the movie you searched for.",
                                                               color=discord.Color.blurple(),
                                                               timestamp=interaction.created_at), view=self)

    @discord.ui.button(emoji="<:delete:912359260954984459>", style=discord.ButtonStyle.red)
    async def delete(self, interaction: discord.Interaction, button: discord.Button):
        await interaction.response.defer()
        await interaction.delete_original_message()

    @discord.ui.button(emoji="<:right:912268383179919360>", style=discord.ButtonStyle.blurple)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            self.counter += 1
            await interaction.response.defer()
            if self.counter != 0 and self.back.disabled is True:
                self.back.disabled = False
                await interaction.message.edit(view=self)
            search = await self.kitsu.search_anime(self.query, limit=11)
            title = search[self.counter].canonical_title
            synopsis = search[self.counter].synopsis
            anime_type = search[self.counter].subtype or "N/A"
            episode_count = search[self.counter].episode_count or "N/A"
            try:
                start_date = f"<t:{int(search[self.counter].start_date.replace(tzinfo=timezone.utc).timestamp())}:F>(<t:{int(search[self.counter].start_date.replace(tzinfo=timezone.utc).timestamp())}:R>)"
            except AttributeError:
                start_date = "N/A"
            try:
                end_date = f"<t:{int(search[self.counter].end_date.replace(tzinfo=timezone.utc).timestamp())}:F>(<t:{int(search[self.counter].end_date.replace(tzinfo=timezone.utc).timestamp())}:R>)"
            except AttributeError:
                end_date = "N/A"
            try:
                rating_rank = search[self.counter].rating_rank
            except TypeError:
                rating_rank = None
            rating_rank = f"**TOP** {rating_rank:,}" if rating_rank is not None else None
            duration = f"{search[self.counter].episode_length // 60} hour(s) and {search[self.counter].episode_length % 60} minutes" if search[self.counter].episode_length is not None else "N/A"
            poster_image = search[self.counter].poster_image(
                _type="large") or "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/832px-No-Image-Placeholder.svg.png"
            status = search[self.counter].status or "N/A"
            embed = discord.Embed(title=title, timestamp=interaction.created_at, color=discord.Color.blurple(),
                                  description=synopsis, url=f"https://kitsu.io/anime/{search[self.counter].id}")
            embed.add_field(name='❓ Type', value=anime_type)
            embed.add_field(name='💽 Episodes', value=episode_count, inline=True)
            embed.add_field(name='<a:time:906880876451876875> Start Date',
                            value=start_date,
                            inline=False)
            embed.add_field(name="<a:time:906880876451876875> End Date", value=end_date,
                            inline=True)
            embed.add_field(name="⏲️ Duration", value=duration, inline=False)
            embed.add_field(name="<a:status:912965228893978634> Status", value=status, inline=True)
            embed.add_field(name="<a:rating:912929196253257778> Rating", value=rating_rank, inline=True)
            embed.set_image(url=poster_image)
            embed.set_footer(text=f"Earth isn’t the only planet with auroras • Page {self.counter}/10",
                             icon_url=interaction.user.display_avatar)
            await interaction.message.edit(embed=embed)

        except IndexError:
            button.disabled = True
            await interaction.message.edit(embed=discord.Embed(title="No More Info Found :(",
                                                               description="No more information has been found regarding the movie you searched for.",
                                                               color=discord.Color.blurple(),
                                                               timestamp=interaction.created_at), view=self)

    @discord.ui.button(emoji="🔖", style=discord.ButtonStyle.grey)
    async def share_embed(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Sending movie info to dm...", ephemeral=True)
        search = await self.kitsu.search_anime(self.query, limit=11)
        title = search[self.counter].canonical_title
        synopsis = search[self.counter].synopsis
        anime_type = search[self.counter].subtype or "N/A"
        episode_count = search[self.counter].episode_count or "N/A"
        try:
            start_date = f"<t:{int(search[self.counter].start_date.replace(tzinfo=timezone.utc).timestamp())}:F>(<t:{int(search[self.counter].start_date.replace(tzinfo=timezone.utc).timestamp())}:R>)"
        except AttributeError:
            start_date = "N/A"
        try:
            end_date = f"<t:{int(search[self.counter].end_date.replace(tzinfo=timezone.utc).timestamp())}:F>(<t:{int(search[self.counter].end_date.replace(tzinfo=timezone.utc).timestamp())}:R>)"
        except AttributeError:
            end_date = "N/A"
        try:
            rating_rank = search[self.counter].rating_rank
        except TypeError:
            rating_rank = None
        rating_rank = f"**TOP** {rating_rank:,}" if rating_rank is not None else None
        duration = f"{search[self.counter].episode_length // 60} hour(s) and {search[self.counter].episode_length % 60} minutes" if search[self.counter].episode_length is not None else "N/A"
        poster_image = search[self.counter].poster_image(
            _type="large") or "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/No-Image-Placeholder.svg/832px-No-Image-Placeholder.svg.png"
        status = search[self.counter].status or "N/A"
        embed = discord.Embed(title=title, timestamp=interaction.created_at, color=discord.Color.blurple(),
                              description=synopsis, url=f"https://kitsu.io/anime/{search[self.counter].id}")
        embed.add_field(name='❓ Type', value=anime_type)
        embed.add_field(name='💽 Episodes', value=episode_count, inline=True)
        embed.add_field(name='<a:time:906880876451876875> Start Date',
                        value=start_date,
                        inline=False)
        embed.add_field(name="<a:time:906880876451876875> End Date", value=end_date,
                        inline=True)
        embed.add_field(name="⏲️ Duration", value=duration, inline=False)
        embed.add_field(name="<a:status:912965228893978634> Status", value=status, inline=True)
        embed.add_field(name="<a:rating:912929196253257778> Rating", value=rating_rank, inline=True)
        embed.set_image(url=poster_image)
        embed.set_footer(text=f"Earth isn’t the only planet with auroras • Page {self.counter}/10",
                         icon_url=interaction.user.display_avatar)
        user_dm = await interaction.user.create_dm()
        await user_dm.send(embed=embed)


class Search(commands.GroupCog, name="search"):
    def __init__(self, client):
        self.client = client
        self.kitsu = kitsu.Client()
        super().__init__()

    @app_commands.command(name="movie", description="Searches for a movie query")
    @app_commands.describe(
        query="The movie to get info on",
        family_friendly="Whether to show nsfw data or not"
    )
    async def movie_info(self, interaction: discord.Interaction, query: str, family_friendly: bool = True):
        try:
            view = ControlsMovie(query=query, family_friendly=family_friendly)
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

    @app_commands.command(name="anime", description="Searches for an anime query")
    @app_commands.describe(
        query="The anime name to get info on"
    )
    async def anime_info(self, interaction: discord.Interaction, query: str):
        search = await self.kitsu.search_anime(query, limit=10)
        view = ControlsAnime(query=query)
        embed = discord.Embed(title=f"<a:anime:912926884688433152> {search[0].canonical_title}",
                              description=search[0].synopsis, url=f"https://kitsu.io/anime/{search[0].id}",
                              timestamp=interaction.created_at, color=discord.Color.dark_teal())
        embed.add_field(name='❓ Type', value=search[0].subtype)
        embed.add_field(name='💽 Episodes', value=search[0].episode_count, inline=True)
        start_date = int(search[0].start_date.replace(tzinfo=timezone.utc).timestamp())
        embed.add_field(name='<a:time:906880876451876875> Start Date', value=f'<t:{start_date}:F>(<t:{start_date}:R>)',
                        inline=False)
        end_date = int(search[0].start_date.replace(tzinfo=timezone.utc).timestamp())
        embed.add_field(name="<a:time:906880876451876875> End Date", value=f"<t:{end_date}:F>(<t:{end_date}:R>)",
                        inline=True)
        try:
            rr = search[0].rating_rank
        except TypeError:
            rr = None
        rr = f"**TOP** {rr:,}" if rr is not None else None
        embed.add_field(name="⏲️ Duration", value=f"{search[0].episode_length} minutes", inline=False)
        embed.add_field(name="<a:status:912965228893978634> Status", value=search[0].status, inline=True)
        embed.add_field(name="<a:rating:912929196253257778> Rating", value=rr, inline=True)
        embed.set_image(url=search[0].poster_image(_type="large"))
        embed.set_footer(text="Earth isn’t the only planet with auroras • Page 0/10",
                         icon_url=interaction.user.display_avatar)
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name='weather', description="The weather details of a ceratin place")
    @app_commands.describe(
        location="The place whose weather information you want"
    )
    async def weather_details(self, interaction: discord.Interaction, location: str):
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?appid=77f5585dd715ec1e39ba87b818b44498&q={location}"

            async with aiohttp.ClientSession() as session:
                async with session.get(url) as data:
                    data = await data.json()
                    try:
                        longitude = data['coord']['lon']
                        latitude = data['coord']['lat']
                        cloud_type = data['weather'][0]['description']
                        temp = data['main']['temp']
                        feels_like = data['main']['feels_like']
                        temp = (temp - 273.15).__format__('0.2f')
                        feels_like = (feels_like - 273.15).__format__('0.2f')
                        min_temp = data['main']['temp_min']
                        min_temp = (min_temp - 273.15).__format__('0.2f')
                        max_temp = data['main']['temp_max']
                        max_temp = (max_temp - 273.15).__format__('0.2f')
                        pressure = data['main']['pressure']
                        humidity = data['main']['humidity']
                        wind_speed = data['wind']['speed']
                        country = data['sys']['country']
                        city_name = data['name']
                    except KeyError:
                        await interaction.response.send_message("<:hellno:871582891585437759> Please provide a valid location.")
            emojis = ["⛅", "🌩️", "🌧️", "🌨️", "⛈️", "🌦️", "🌤️"]
            embed = discord.Embed(title=f"{random.choice(emojis)} {city_name}'s Weather Info", timestamp=interaction.created_at,
                                  color=discord.Color.blurple())
            embed.set_footer(text="Northern And Southern Lights Might Not Be Symmetrical", icon_url=interaction.user.display_avatar)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/e7/7a/60/e77a6068aa8bb2731e3b6d835c09c84c.gif")

            # content
            embed.add_field(name="City", value=city_name)
            embed.add_field(name="Country", value=country)
            embed.add_field(name="Longitude", value=longitude)
            embed.add_field(name="Latitude", value=latitude)
            embed.add_field(name="Cloud Type", value=cloud_type)
            embed.add_field(name="Temperature", value=f"{temp}℃")
            embed.add_field(name="Feels Like", value=f"{feels_like}℃")
            embed.add_field(name="Minimum Temp", value=f"{min_temp}℃")
            embed.add_field(name="Maximum Temp", value=f"{max_temp}℃")
            embed.add_field(name="Pressure", value=f"{pressure}hPa")
            embed.add_field(name="Wind Speed", value=f"{wind_speed}m/s")
            embed.add_field(name="Humidity", value=f"{humidity}%")
            await interaction.response.send_message(embed=embed)
        except:
            error_logger.error("An error occurred while running weather command:- ", exc_info=True)


async def setup(client):
    await client.add_cog(Search(client))
