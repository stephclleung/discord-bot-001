from discord.ext import commands
from random import choice
import re


class SpellItRight(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if '2dlive' in message.content.lower() or re.search(r'\b2d live\b', message.content.lower()):
            channel = message.channel
            random_filler = [
                f'It is a wonderful day, dear <@{message.author.id}>, but perhaps you meant ***Live2D***.',
                f'Welcome to the Live2D hell,  <@{message.author.id}>, ***Live2D***',
                f'🐶 A puppy gets sad every time someone says `2dlive`. \n'
                f'A puppy gets an extra treat every time someone says ***Live2D*** 🐶',
                f'Beep-bop-beep-bop, robot detected 2dLive, wants to tell <@{message.author.id}> that it is ***Live2D***.s'
            ]

            choice_of_tease = choice(random_filler)
            await channel.send(choice_of_tease)

        await self.bot.process_commands(message)


def setup(bot):
    bot.add_cog(SpellItRight(bot))
