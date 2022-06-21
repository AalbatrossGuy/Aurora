# import interactions, os
# from customs.customs import version_info
#
# # COMMANDS
# class OnReady(interactions.Extension):
#     def __init__(self, client):
#         self.client = client
#
#     # @interactions.extension_command(name="cog", description="This is running from a cog", scope=903225083072495646)
#     # async def cog_slash_command(self, ctx):
#     #     await ctx.send("Sent from a cog!")
#
#     @interactions.extension_listener()
#     async def on_ready(self):
#         version = version_info()[0][:7]
#         date = version_info()[1]
#         bot_id = self.client.me.id
#         bot_name = self.client.me.name
#         print('')
#         print(f'Logged in as: {bot_name}(ID: {bot_id})')
#         print(f'Running on branch {version} commited on {date}')
#         print('==================================================')
#         print('')
#         cogs = [x[:-3] for x in os.listdir('./Cogs')]
#         for cogsname in cogs:
#             if cogsname == "__pycach":
#                 continue
#             else:
#                 try:
#                     print(f"Loaded cogs.{cogsname} successfully!")
#                 except:
#                     pass
#         print('')
#         print('==================================================')
#         print('')
#         print('Bot up and running stable! (Errors will be logged in the logs folder.)')
#
# def setup(client):
#     OnReady(client)
