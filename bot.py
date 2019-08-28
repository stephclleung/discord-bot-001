import asyncio
import datetime
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


@bot.command(name='create-channel', help='Makes a new channel. Admin only.')
@commands.has_role('admeeeen')
async def create_channel(ctx, channel_name='unnamed-channel'):
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
    if message.content.startswith('tag_posts'):
        msg = await message.channel.history(limit=50).flatten()
        await message.channel.send(f'<@{message.author.id}> commenced post tagging.')
        for m in msg:
            if m.attachments:
                await m.add_reaction('📌')
        await message.channel.send(f'Tagging completed, <@{message.author.id}>')

    elif message.content.startswith('clean_up_posts'):
        msg = await message.channel.history(limit=50).flatten()
        await message.channel.send(f'📢 Beep-beep. Clean up time. All posts without attachments will be removed.')
        for m in msg:
            if not m.reactions:
                await m.delete()
        await message.channel.send('📢 All posts without attachments have now been removed. I am so helpful.')

    elif message.content.startswith('remove react'):
        msg = await message.channel.history(limit=50).flatten()
        print(f'After getting msgs {msg}')
        for m in msg:
            if m.reactions:
                print(f'This m : {m.content}')
                print(f'Found reactions {m.reactions}')
                await m.remove_reaction('📌', bot.user)

    elif '2dlive' in message.content.lower() or re.search(r'\b2d live\b', message.content):
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


bot.run(TOKEN)
