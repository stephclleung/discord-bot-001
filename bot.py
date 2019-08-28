
import re
import discord
import os
from random import choice
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='!')  # subclass, Client is superclass
admin = 'admeeeen'
url = r'(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](' \
      r'?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad' \
      r'|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca' \
      r'|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk' \
      r'|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir' \
      r'|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml' \
      r'|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn' \
      r'|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td' \
      r'|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw' \
      r')/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s(' \
      r')]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](' \
      r'?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad' \
      r'|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca' \
      r'|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk' \
      r'|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir' \
      r'|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml' \
      r'|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn' \
      r'|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td' \
      r'|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw' \
      r')\b/?(?!@))) '


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to discord')


@bot.command(name='create-channel', help='[Admin only] Makes a new channel.')
@commands.has_role(admin)
async def create_channel(ctx, channel_name='unnamed-channel'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)  # if true, a same name channel exists
    if not existing_channel:
        await ctx.message.channel.send(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)


@bot.command(name='tag-posts', help='[Admin only] Tags all posts with attachment. ')
@commands.has_role(admin)
async def tag_posts(ctx):
    channel = ctx.message.channel
    author = ctx.message.author
    count = 0
    if channel:
        msg = await channel.history(limit=50).flatten()
        await channel.send(f'<@{author.id}> commenced post tagging.')
        for m in msg:
            if m.attachments or re.search(url, m.content):
                await m.add_reaction('📌')
                count += 1
        await channel.send(f'Tagged {count} post(s), <@{author.id}>')


@bot.command(name='clean-up', help='[Admin only] Remove all posts without attachments. ')
@commands.has_role(admin)
async def clean_up(ctx):
    channel = ctx.message.channel
    count = 0
    if channel:
        await channel.send(f'📢 Beep-beep. Clean up time. All posts without attachments will be removed.')
        msg = await channel.history(limit=50).flatten()
        for m in msg:
            if not m.reactions:
                count += 1
                await m.delete()
        await channel.send(f'📢 Helpful robot removed {count} post(s). I am so helpful')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if '2dlive' in message.content.lower() or re.search(r'\b2d live\b', message.content.lower()):
        channel = message.channel
        random_filler = [
            f'It is a wonderful day, dear <@{message.author.id}>, but perhaps you meant ***Live2D***.',
            f'Welcome to the Live2D hell,  <@{message.author.id}>, ***Live2D***',
            f'🐶 A puppy gets sad every time someone says `2dlive`. \n'
            f' A puppy gets an extra treat every time someone says ***Live2D*** 🐶',
            f'Beep-bop-beep-bop, robot detected 2dLive, wants to tell <@{message.author.id}> that it is ***Live2D***.s'
        ]

        choice_of_tease = choice(random_filler)
        await channel.send(choice_of_tease)

    await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send(f'<@{ctx.message.author.id}>, I love you, but you do not have the permissions to do that.')


bot.run(TOKEN)
