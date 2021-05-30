import discord
import os
from discord.ext import commands
import trivdata

os.chdir(os.getcwd())


class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command(brief="plant")
    # async def kek(self, ctx):
    #     await ctx.send("cactus")
def setup(bot):
    bot.add_cog(Miscellaneous(bot))
