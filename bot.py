import asyncio

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
@commands.has_role('admeeeen')
async def on_message(message):
    print(message)

    if message.content.startswith('durhurhur'):
        channel = message.channel

        await channel.send('Thumbs up me pls :3 ')

        def check(reaction, user):
            return user == message.author and str(reaction.emoji) == '👍'

        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await channel.send(':(')
        else:
            await channel.send(f'I <3 you too, <@{message.author.id}>')


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
