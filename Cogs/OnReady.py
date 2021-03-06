from discord.ext import commands
from customs.customs import version_info, set_uptime
import datetime


class OnReady(commands.Cog):
    def __int__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        version = version_info()[0][:7]
        date = version_info()[1]
        print(f'Running on branch {version} committed on {date}')
        set_uptime(datetime.datetime.now())
        print('Running Aurora...')


async def setup(client):
    await client.add_cog(OnReady(client))
