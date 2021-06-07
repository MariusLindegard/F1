import discord, requests, datetime
from discord.ext import commands, tasks

def create_embed(title, description: str=None, url: str=None, footer: str='Formula 1!'):
    embed = discord.Embed(title=title, description=description)
    embed.set_footer(text=footer)
    embed.url = url
    embed.timestamp = datetime.datetime.now()
    embed.color = discord.Color.gold()
    return embed

def get_info():
    return requests.get('http://ergast.com/api/f1/current.json').json()


class RaceInformation:
    def __init__(self, info):
        self.config = info
        self.race_info()

    def race_info(self):
        self.races = []
        for race in self.config['MRData']['RaceTable']['Races']:
            self.races.append(race)
        
        return self.races

    def next_race(self):
        index = 0
        current_day = datetime.datetime.now()

        # check next race and return

        for race in self.races:
            date = self.races[index]['date']
            next_date = datetime.datetime.strptime(date, '%Y-%m-%d')

            days_since = next_date - current_day

            if days_since.days > 0:
                return self.races[index]
                break

            index += 1
            

    def current_race(self):
        """
        fetch current race (pos, time)
        this is for the embed in the discord
        """

class FormulaOne(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('FormulaOne cog has been loaded')
        self.config = get_info()
        self.race = RaceInformation(self.config)
        self.update_config.start()


    @tasks.loop(minutes=5)
    async def update_config(self):
        matches = get_info()
        self.race.config = matches

    @commands.command()
    async def season(self, ctx):
        embed = create_embed('Races this season', 'These are the races this season')

        for race in self.race.race_info():
            embed.add_field(name=race['Circuit']['Location']['locality'], value=f'**Date:** {race["date"]}\n**Race num:** {race["round"]}')

        await ctx.send(embed=embed)
    
    @commands.command()
    async def next_race(self, ctx):
        race_data = self.race.next_race()
        embed = create_embed(race_data["raceName"], f'**Round:** {race_data["round"]}\n**Circuit:** {race_data["Circuit"]["circuitName"]}\n**Date:** {race_data["date"]}\n**Time:** {race_data["time"]}')

        await ctx.send(embed=embed)
        

def setup(bot):
    bot.add_cog(FormulaOne(bot))