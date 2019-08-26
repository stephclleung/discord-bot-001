import discord
import os

from dotenv import load_dotenv

load_dotenv()

client = discord.Client()
TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')
print(TOKEN)
print(GUILD)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)
    elif message.content.startswith('!pinthis'):
        perms = discord.Permissions()
        perms.update(manage_messages=True)
        await message.pin()


# def client.event(func):
# ....conditions...
# ... func()
# .......

# async def on_message(message):
#   ..stuff..
# on_message = client.event(on_message)


@client.event
async def on_ready():
    # print('Logged in as')
    #     # print(client.user.name)
    #     # print(client.user.id)
    #     # print('----------------')
    #guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following :'
        f'{guild.name} (id : {guild.id})'
    )


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to discord server!'
    )


client.run(TOKEN)
