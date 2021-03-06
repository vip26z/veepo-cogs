import contextlib
import zlib

from redbot.core import commands, Config
from redbot.core.utils.mod import check_permissions
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from typing import Literal
import discord

import aiohttp
import random

khalai = 'https://static.wikia.nocookie.net/starcraft/images/5/5d/Khalai_SC2-LotV_Logo1.jpg'
nerazim = 'https://static.wikia.nocookie.net/starcraft/images/c/c1/Nerazim_SC2-LotV_Logo1.jpg'
taldarim = 'https://static.wikia.nocookie.net/starcraft/images/6/6a/Tal%27darim_SC2-LotV_Logo2.jpg'
purifiers = 'https://static.wikia.nocookie.net/starcraft/images/6/62/Purifiers_SC2-LotV_Logo1.jpg'
xelnaga = 'https://vignette.wikia.nocookie.net/starcraftrpg/images/0/07/Xel%27Naga_Art.png'

class ProtossTribe(commands.Cog):
    """Lookup information about the Harry Potter Universe"""

    __author__ = "dsmoth"

    async def red_delete_data_for_user(
        self,
        *,
        requester: Literal["discord_deleted_user", "owner", "user", "user_strict"],
        user_id: int,
    ):
        """This cog stores a user ID to match them to their Harry Potter house,
        this will wipe their saved house from the cog"""
        await self.config.user_from_id(user_id).clear()


    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession(loop=self.bot.loop)
        self.config = Config.get_conf(self, 376564057439483943818, force_registration=True)

        default_user = {"tribe": None}

        self.config.register_user(**default_user)

    def _get_tribe_from_string(self, inp):
        rng = random.Random(inp)
        tribes = [
            'Khalai',
            'Nerazim',
            "Tal'darim",
            'Purifiers'
        ]
        return rng.choice(tribes)

    def get_tribe_from_string(self, inp):
        houses = {
            '00': 'Khalai',
            '01': 'Nerazim',
            '10': "Tal'darim",
            '11': 'Purifiers'
        }
        inp = str.encode(str(inp), 'utf-8')
        adler = zlib.adler32(inp)
        key = bin(adler)[-2:]
        return houses[key]

    @commands.bot_has_permissions(embed_links=True)
    @commands.command()
    async def tribesort(self, ctx, user=None, tribe=None):
        """Find your Protoss Tribe"""
        is_lookup = bool(user)
        if is_lookup:
            member = ctx.guild.get_member_named(user)
            if not member:
                try:
                    member = ctx.message.mentions[0]
                except IndexError:
                    await ctx.send('No user by that name was found')
                    return
        else:
            member = ctx.author
        member_config = self.config.user(member)
        is_owner = await check_permissions(ctx, {})
        if not is_owner or not tribe:
            if await member_config.tribe() is None:
                tribe = self.get_tribe_from_string(member.id)
            else:
                tribe = await member_config.tribe()
        color = await ctx.embed_color()
        if tribe == "Khalai":
            image = khalai
            embed = discord.Embed(
                title="Find your Protoss Tribe", description=tribe, color=color
            )
            embed.set_thumbnail(url=image)
        elif tribe == "Nerazim":
            image = nerazim
            embed = discord.Embed(
                title="Find your Protoss Tribe", description=tribe, color=color
            )
            embed.set_thumbnail(url=image)
        elif tribe == "Tal'darim":
            image = taldarim
            embed = discord.Embed(
                title="Find your Protoss Tribe", description=tribe, color=color
            )
            embed.set_thumbnail(url=image)
        elif tribe == "Purifiers":
            image = purifiers
            embed = discord.Embed(
                title="Find your Protoss Tribe", description=tribe, color=color
            )
            embed.set_thumbnail(url=image)
        elif tribe == "Xel'Naga":
            image = xelnaga
            embed = discord.Embed(
                title="Find your Protoss Tribe", description=tribe, color=color
            )
            embed.set_thumbnail(url=image)
        else:
            ctx.send("Invalid tribe")
            return
        if is_owner:
            await member_config.tribe.set(tribe)
            tribes = ["Khalai","Nerazim","Tal'darim","Purifiers",
                      "Xel'Naga"]
            for tribe_role in [i for i in member.roles if i.name in tribes]:
                print(tribe_role)
                await member.remove_roles(tribe_role)
            new_tribe_role = discord.utils.get(ctx.guild.roles, name=tribe)
            if new_tribe_role:
                await member.add_roles(discord.utils.get(ctx.guild.roles, name=tribe))
        await ctx.send(embed=embed)

    def cog_unload(self):
        self.bot.loop.create_task(self.session.close())
