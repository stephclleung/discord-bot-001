
import re
import discord
import os
from random import choice
from dotenv import load_dotenv

from discord.ext import commands
import sys, traceback
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

initial_extensions = ['commands.spellitright']

# Here we load our extensions(cogs) listed above in [initial_extensions].
# if __name__ == '__main__':
#     for extension in initial_extensions:
#         try:
#             bot.load_extension(extension)
#         except Exception as e:
#             print(f'Failed to load extension {extension}.', file=sys.stderr)
#             traceback.print_exc()

bot.load_extension((initial_extensions[0]))


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
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send(f'<@{ctx.message.author.id}>, I love you, but you do not have the permissions to do that.')


bot.run(TOKEN)
