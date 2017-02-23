import discord
import os
import json
from discord.ext import commands
from Overlord.cogs.utils import permissions

''' proof of concept system, the reputation name is temporary '''
class Reputation:
    def __init__(self, bot):
        self.bot = bot
        if os.path.isfile('data.json'):
            self.load()

    @commands.command(pass_context=True)
    @permissions.checkMod()
    async def addrepdebug(self, ctx, *, amount: int):
        self.addrep(amount, self.bot.user, ctx.message.author)
        await self.bot.say("Added {} reputation!".format(amount))

    @commands.command(pass_context=True)
    @permissions.checkMod()
    async def resetrep(self, ctx):
        count = 0
        for member in ctx.message.mentions:
            self.removerep(self.getrep(member), member)
            count += 1

        await self.bot.say("Reset reputation for {} users!".format( count))

    @commands.command(pass_context=True)
    async def getreputation(self, ctx):
        await self.bot.say("Current Reputation: {}".format(self.getrep(ctx.message.author)))

    @commands.command(pass_context=True)
    async def leaderboard(self, ctx):
        i = 1
        for userid, amount in self.userlist.items():
            if amount != 0:
                await self.bot.say("{}. {}: {}".format(i, ctx.message.server.get_member(userid).name, amount))
                i += 1

    async def on_message(self, message: discord.Message):
        if "thanks" in message.content and len(message.mentions) > 0:
            for member in message.mentions:
                if member != message.author and member != self.bot.user:
                    self.addrep(10, message.author, member)

    def checkuser(self, targetMember: discord.Member):
        if targetMember.id not in self.userlist:
            self.userlist[targetMember.id] = 0

    def addrep(self, amount : int, srcMember: discord.Member, targetMember: discord.Member):
        self.bot.logger.info("Member {} is giving {} reputation to {}".format(srcMember.name, amount, targetMember.name))
        self.checkuser(targetMember)

        self.userlist[targetMember.id] += amount
        self.save()

    def removerep(self, amount : int, targetMember: discord.Member):
        self.bot.logger.info("{} rep removed from {}".format(amount, targetMember.name))
        self.checkuser(targetMember)

        self.userlist[targetMember.id] -= amount
        self.save()

    def getrep(self, targetMember: discord.Member):
        self.checkuser(targetMember)

        return self.userlist[targetMember.id]

    def save(self):
        with open('data.json', 'w') as fp:
            json.dump(self.userlist, fp)

    def load(self):
        with open('data.json', 'r') as fp:
            self.userlist = json.load(fp)

    userlist = {}

def setup(bot):
    bot.add_cog(Reputation(bot))
