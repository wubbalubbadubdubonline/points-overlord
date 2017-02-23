import discord
import os
from discord.ext import commands
from Overlord.cogs.utils import permissions
import json

''' proof of concept system, the reputation name is temporary '''
class Coins:
    def __init__(self, bot):
        self.bot = bot
        if os.path.isfile('data.json'):
            self.load()

    @commands.command(pass_context=True)
    @permissions.checkMod()
    async def repdebug(self, ctx, *, amount : int):
        self.addrep(amount, self.bot.user, ctx.message.author)
        await self.bot.say("Added {} reputation!".format(amount))

    @commands.command(pass_context=True)
    async def getrep(self, ctx):
        await self.bot.say("Current Reputation: {}".format(self.userlist[ctx.message.author.id]))

    @commands.command(pass_context=True)
    async def leaderboard(self, ctx):
        i = 1
        for userid, amount in self.userlist.items():
            await self.bot.say("{}. {}: {}".format(i, ctx.message.server.get_member(userid).name, amount))
            i += 1

    def addrep(self, amount : int, srcMemeber : discord.Member, targetMember : discord.Member):
        self.bot.logger.info("Memeber {} is giving {} reputation to {}".format(srcMemeber.name, amount, targetMember.name))
        if targetMember.id not in self.userlist:
            self.userlist[targetMember.id] = 0

        self.userlist[targetMember.id] += amount
        self.save()

    def save(self):
        with open('data.json', 'w') as fp:
            json.dump(self.userlist, fp)

    def load(self):
        with open('data.json', 'r') as fp:
            self.userlist = json.load(fp)

    userlist = {}

def setup(bot):
    bot.add_cog(Coins(bot))
