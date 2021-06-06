import discord, requests
from discord.ext import commands


class FormulaOne(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(FormulaOne(bot))