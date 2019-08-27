import asyncio
import re
import discord
import os
from random import choice
from dotenv import load_dotenv

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(command_prefix='!')  # subclass, Client is superclass


@bot.event
async def on_ready():
   print(f'{bot.user.name} has connected to discord')


@bot.command(name="hello", help="gives a random quote")
async def hello(ctx):
    random_quotes = [
        f'Beep bop beep',
        (
            'Yap yap yap aypa yap,\n'
            'Bop bop bop'
        )
    ]
    response = choice(random_quotes)
    await ctx.send(response)


# arguments to a Command function are by default "str"
# need to use converter.
@bot.command(name='roll_dice', help='Pretends to rol a dice')
# async def roll(ctx, num_dice, num_sides):
async def roll(ctx, num_dice: int, num_sides: int):
    dice = [str(choice(range(1, num_sides + 1))) for _ in range(num_dice)]
    await ctx.send(', '.join(dice))


@bot.command(name='create-channel', help='make new channel')
@commands.has_role('admeeeen')
async def create_channel(ctx, channel_name='real-bot-channel'):
    guild = ctx.guild
    print(guild.channels)
    existing_channel = discord.utils.get(guild.channels, name=channel_name)  # if true, a same name channel exists
    print(f'Utils.get : {existing_channel}')
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print(message)
    print(f'Pin this {message.content}')
    print(f' Message has attachment? {message.attachments}')
    # elif message.content.startswith('durhurhur'):
    print('-----------------------------')

    if message.content.startswith('history'):
        msg = await message.channel.history(limit=50).flatten()
        with_attachments = [];
        print(f'After getting msgs {msg}')
        for m in msg:
            if m.attachments:
                print(f'This m : {m.content}')
                print(f'Found attachment {m.attachments}')
                with_attachments.append(m)
        print('--------------------------------------')
        print(f'After filter, {with_attachments}')
        await message.channel.send()
    elif message.content.startswith('react'):

    #     channel = message.channel
    #
    #     await channel.send('Thumbs up me pls :3 ')
    #
    #     def check(reaction, user):
    #         return user == message.author and str(reaction.emoji) == '👍'
    #
    #     try:
    #         reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
    #     except asyncio.TimeoutError:
    #         await channel.send(':(')
    #     else:
    #         await channel.send(f'I <3 you too, <@{message.author.id}>')
    # elif message.content.startswith('pin this'):
    #     print(message)
    #     print(f'Pin this {message.content}')
    #     print(f' Message has attachment? {message.attachments}')
    # elif '2dlive' in message.content.lower() or re.search(r'\b2d live\b', message.content):
    #     #     print(f'found 2d live ', message.content)
    #     #     channel = message.channel
    #     #     random_filler = [
    #     #         f'It is a wonderful day, dear <@{message.author.id}>, but perhaps you meant ***Live2D***.',
    #     #         f'Welcome to the Live2D hell,  <@{message.author.id}>, ***Live2D***',
    #     #         f'A puppy gets sad every time someone says 2dlive. A puppy gets an extra treat every time someone says ***Live2D***',
    #     #         f'Beep-bop-beep-bop, robot detected 2dLive, wants to tell <@{message.author.id}> that it is ***Live2D***.s'
    #     #     ]
    #     #
    #     #     choice_of_tease = choice(random_filler)
    #     #     await channel.send(choice_of_tease)




@bot.event
async def on_command_error(ctx, error):
    print("Got an error...")
    print(error)
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the permissions to do this.')




@bot.event
async def on_error(event_method, *args, **kwargs):
    print("Got event error...")
    print(event_method)
    print(args)
    print(kwargs)

bot.run(TOKEN)
