import discord, requests, json, datetime
from discord.ext import commands, tasks

def get_info():
    return requests.get('http://ergast.com/api/f1/current.json').json()


class RaceInformation:
    def __init__(self, config):
        self.config = config
        self.races = []

        for race in config['MRData']['RaceTable']['Races']:
            self.races.append(race)

    def next_race(self):
        for race in self.races['date']:
            if datetime.datetime.now() > datetime.timedelta(race):
                print('Race has not begun')

class FormulaOne(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('FormulaOne cog has been loaded')
        self.config = get_info()
        self.race = RaceInformation(self.config)


    @tasks.loop(minutes=5)
    async def update_config(self):
        matches = get_info()
        self.race.config = matches
        

def setup(bot):
    bot.add_cog(FormulaOne(bot))