import discord, datetime

class Embed():
    def __init__(self):
        pass
    
    def create_embed(self, title, description: str=None, url: str=None, footer: str='CHANGE ME bot/utils/embed.py!'):
        embed = discord.Embed(title=title, description=description)
        embed.set_footer(text=footer)
        embed.url = url
        embed.timestamp = datetime.datetime.now()
        return embed