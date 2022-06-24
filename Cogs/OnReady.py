from discord.ext import commands
from customs.customs import version_info


class OnReady(commands.Cog):
    def __int__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        version = version_info()[0][:7]
        date = version_info()[1]
        print(f'Running on branch {version} committed on {date}')
        print('Running Aurora...')


async def setup(client):
    await client.add_cog(OnReady(client))
