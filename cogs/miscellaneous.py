import discord
import os
from discord.ext import commands
import trivdata

os.chdir(os.getcwd())


class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief = "Plant")
    async def kek(self, ctx):
        await ctx.send("Cactus")
        
def setup(bot):
    bot.add_cog(Miscellaneous(bot))
