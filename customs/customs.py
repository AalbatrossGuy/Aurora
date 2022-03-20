# Start_info.py
import subprocess, interactions
from datetime import datetime

def version_info():
    version = 'No Data'
    date = 'No Data'
    gitlog = subprocess.check_output(
        ['git', 'log', '-n', '1', '--date=iso']).decode()
    for line in gitlog.split('\n'):
        if line.startswith('commit'):
            version = line.split(' ')[1]
        elif line.startswith('Date'):
            date = line[5:].strip()
            date = date.replace(' +', '+').replace(' ', 'T')
        else:
            pass
    return version, date

def createEmbed(title: str, color: int, footer_text: str, footer_icon_url: str, thumbnail_url: str, description: str = None, author_name: str = None, author_icon_url: str = None) -> interactions.Embed:

    if author_name & author_icon_url & description != None:
            embed = interactions.Embed(
                title = title,
                description=description,
                color=color,
                footer=interactions.EmbedFooter(
                    text=footer_text,
                    icon_url=footer_icon_url,
                ),
                thumbnail=interactions.EmbedImageStruct(
                    url=thumbnail_url,
                )._json,
                author=interactions.EmbedAuthor(
                    name=author_name,
                    icon_url=author_icon_url,
                ),
            )
            return embed
    elif author_name & author_icon_url != None:
            embed = interactions.Embed(
                title = title,
                color=color,
                footer=interactions.EmbedFooter(
                    text=footer_text,
                    icon_url=footer_icon_url,
                ),
                thumbnail=interactions.EmbedImageStruct(
                    url=thumbnail_url,
                )._json,
                author=interactions.EmbedAuthor(
                    name=author_name,
                    icon_url=author_icon_url,
                ),
            )
            return embed
    elif description != None:
            embed = interactions.Embed(
                title = title,
                description=description,
                color=color,
                footer=interactions.EmbedFooter(
                    text=footer_text,
                    icon_url=footer_icon_url,
                ),
                thumbnail=interactions.EmbedImageStruct(
                    url=thumbnail_url,
                )._json,
            )
            return embed
    else:
            embed = interactions.Embed(
                title = title,
                color=color,
                footer=interactions.EmbedFooter(
                    text=footer_text,
                    icon_url=footer_icon_url,
                ),
                thumbnail=interactions.EmbedImageStruct(
                    url=thumbnail_url,
                )._json,
            )
            return embed


if __name__ == '__main__':
    print("Run as import.")
