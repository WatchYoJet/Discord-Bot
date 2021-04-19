import discord
from discord import Embed, PermissionOverwrite, Intents
from discord.ext import commands
import random
import time
import os
from dotenv import load_dotenv
import asyncio
from discord.utils import get
from discord import Embed, PermissionOverwrite, Intents
from discord.ext import commands
from discord.utils import get
import os
import json
import cryptocompare

client = commands.Bot(command_prefix='$')

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('with BrawlHouse!'))

    print('Connected to bot: {}'.format(client.user.name))
    print('Bot ID: {}'.format(client.user.id))


def is_it_me(ctx):
    return ctx.author.id in [
        563001852971712523, 250715544209063936, 107793741871329280,
        192014009749209088, 192012933281087489
    ]


def crazy_ones(ctx):
    return ctx.author.id in [
        583687913720512538, 192012933281087489, 250715544209063936
    ]


def close_friends(ctx):
    return ctx.author.id in [
        692488790069215324, 637336776867971083, 192012933281087489
    ]


@client.command(name='create-channel')
async def create_channel(ctx, channel_name='test channel'):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_voice_channel(channel_name)


@client.command(pass_context=True)
async def sudo(ctx, role: discord.Role, member: discord.Member = None):
    member = member or ctx.message.author
    await client.add_roles(member, role)
    await ctx.channel.purge(1)


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            print('Ola!')


@client.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, id="717660267726766112")
    await client.add_roles(member, role)


@client.event
async def on_member_join(member):
    print(f'{member} has joined!')


@client.event
async def on_member_remove(member):
    print(f'{member} has left!')


@client.command()
async def ping(ctx):
    await ctx.send(f'ping: {round(client.latency * 1000)}ms')


@client.command()
async def nword(ctx):
    await ctx.send('ni||ce ca||r')


@client.command()
@commands.check(crazy_ones)
async def mariana(ctx):
    await ctx.send('Cala-te')
    time.sleep(1)
    await ctx.send('**Puta**')
    await ctx.send('https://tenor.com/view/spit-ew-gross-saliva-gif-16510204')
    time.sleep(0.5)
    await ctx.send('**Rebola**')
    time.sleep(0.5)
    await ctx.send('**Transformer**')
    await ctx.send('https://media.giphy.com/media/xM2Y96rO1d5VRLCYEG/giphy.gif'
                   )


@client.command()
async def pedro(ctx):
    await ctx.send('Lindo <3')


@client.command()
@commands.check(close_friends)
async def miguel(ctx):
    await ctx.send('Send feet pics!')


@client.command()
async def dinis(ctx):
    await ctx.send('Stfu CringeMan')
    time.sleep(5)
    await ctx.send('JK I SIMP DINIS')


@client.command()
async def hi(ctx):
    await ctx.send(f'Hi {ctx.author}!')


@client.command()
@commands.check(is_it_me)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)


@client.command(aliases=["user-info", "User-Info", "UserInfo", "ui"])
async def userinfo(ctx, member: discord.Member = None):
    member = ctx.author if not member else member
    roles = [role for role in member.roles]

    embed = discord.Embed(colour=member.color,
                          timestamp=ctx.message.created_at)

    embed.set_author(name=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}",
                     icon_url=ctx.author.avatar_url)

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Guild name:", value=member.display_name)

    embed.add_field(
        name="Created at:",
        value=member.created_at.strftime("%a, %d %B %Y, %I:%M %p UTC"))
    embed.add_field(
        name="Joined at:",
        value=member.joined_at.strftime("%a, %d %B %Y, %I:%M %p UTC"))

    embed.add_field(name=f"Roles ({len(roles)})",
                    value=" ".join([role.mention for role in roles]))
    embed.add_field(name="Top role:", value=member.top_role.mention)

    embed.add_field(name="Bot?", value=member.bot)

    await ctx.send(embed=embed)


@client.command()
async def bat(ctx):
    price = cryptocompare.get_price('BAT', 'EUR')
    await ctx.send(price['BAT']['EUR'], "€")


client.run(TOKEN)