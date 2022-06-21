# # Start_info.py
# import subprocess, interactions
# from datetime import datetime
# import logging
#
# loggers = {}
#
# def AuroraLogger(name: str, log_file: str):
#     LOG_FILE = log_file
#     global loggers
#
#     if loggers.get(name):
#         return loggers.get(name)
#     else:
#         logger = logging.getLogger(name)
#         logger.setLevel(logging.INFO)
#         handler = logging.FileHandler(LOG_FILE)
#         formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%d-%b-%y %H:%M:%S")
#         handler.setFormatter(formatter)
#         logger.addHandler(handler)
#         loggers[name] = logger
#
#         return logger
#
#
# def version_info():
#     version = 'No Data'
#     date = 'No Data'
#     gitlog = subprocess.check_output(
#         ['git', 'log', '-n', '1', '--date=iso']).decode()
#     for line in gitlog.split('\n'):
#         if line.startswith('commit'):
#             version = line.split(' ')[1]
#         elif line.startswith('Date'):
#             date = line[5:].strip()
#             date = date.replace(' +', '+').replace(' ', 'T')
#         else:
#             pass
#     return version, date
#
# def createEmbed(title: str, color: int, footer_text: str, footer_icon_url: str, thumbnail_url: str, fields: list, description: str = False, author_name: str = False, author_icon_url: str = False) -> interactions.Embed:
#
#     if author_name and author_icon_url and description:
#             embed = interactions.Embed(
#                 title = title,
#                 description=description,
#                 timestamp=datetime.utcnow().isoformat(),
#                 color=color,
#                 footer=interactions.EmbedFooter(
#                     text=footer_text,
#                     icon_url=footer_icon_url,
#                 ),
#                 thumbnail=interactions.EmbedImageStruct(
#                     url=thumbnail_url,
#                 )._json,
#                 author=interactions.EmbedAuthor(
#                     name=author_name,
#                     icon_url=author_icon_url,
#                 ),
#                 fields=fields,
#             )
#             return embed
#     elif author_name and author_icon_url:
#             embed = interactions.Embed(
#                 title = title,
#                 timestamp=datetime.utcnow().isoformat(),
#                 color=color,
#                 footer=interactions.EmbedFooter(
#                     text=footer_text,
#                     icon_url=footer_icon_url,
#                 ),
#                 thumbnail=interactions.EmbedImageStruct(
#                     url=thumbnail_url,
#                 )._json,
#                 author=interactions.EmbedAuthor(
#                     name=author_name,
#                     icon_url=author_icon_url,
#                 ),
#                 fields=fields,
#             )
#             return embed
#     elif description:
#             embed = interactions.Embed(
#                 title = title,
#                 description=description,
#                 timestamp=datetime.utcnow().isoformat(),
#                 color=color,
#                 footer=interactions.EmbedFooter(
#                     text=footer_text,
#                     icon_url=footer_icon_url,
#                 ),
#                 thumbnail=interactions.EmbedImageStruct(
#                     url=thumbnail_url,
#                 )._json,
#                 fields=fields,
#             )
#             return embed
#     else:
#             embed = interactions.Embed(
#                 title = title,
#                 timestamp=datetime.utcnow().isoformat(),
#                 color=color,
#                 footer=interactions.EmbedFooter(
#                     text=footer_text,
#                     icon_url=footer_icon_url,
#                 ),
#                 thumbnail=interactions.EmbedImageStruct(
#                     url=thumbnail_url,
#                 )._json,
#                 fields=fields,
#             )
#             return embed
#
#
# if __name__ == '__main__':
#     print("Run as import.")
