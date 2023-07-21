import discord
import logging as logger

from discord import app_commands
from discord.ext import commands
from datetime import datetime


class logging(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.bot.tree.on_error = self.on_error
        self.log = logger.getLogger("discord.app_command.error")

    @commands.Cog.listener()
    async def on_app_command_completion(self, interaction: discord.Interaction, command: app_commands.Command):
        embed = discord.Embed(color=0x47e0ff, title=f"/{command.name}")
        embed.set_author(name=f"{interaction.user.display_name} ({interaction.user.name})", icon_url=interaction.user.display_avatar)
        if interaction.guild_id:
            embed.set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon)
        else:
            embed.set_footer(text="dms")
        embed.timestamp = datetime.now()
        if "options" in interaction.data:
            for option in interaction.data['options']:
                embed.add_field(name=option['name'], value=option['value'])
        await self.bot.get_channel(1065611483897147502).send(embed=embed)

    async def on_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        await interaction.followup.send(content="An error occured in your command, please report this to the support server: https://discord.com/channels/1041775602576928809/1128795919945584801")
        embed = discord.Embed(color=0xFF0000, title=f"/{interaction.command.name}", description=error)
        embed.set_author(name=f"{interaction.user.display_name} ({interaction.user.name})", icon_url=interaction.user.display_avatar)
        if interaction.guild_id:
            embed.set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon)
        else:
            embed.set_footer(text="dms")
        embed.timestamp = datetime.now()
        if "options" in interaction.data:
            for option in interaction.data['options']:
                embed.add_field(name=option['name'], value=option['value'])
        msg = await self.bot.get_channel(1065611483897147502).send(content=f"{error} <@169497208406802432>", embed=embed)
        self.log.error('Ignoring exception in command %r', interaction.command.name, exc_info=error)
        await msg.edit(content="<@169497208406802432>")

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        embed = discord.Embed(color=0x97F9D8, title=f"joined {guild.name}")
        embed.add_field(name="members", value=guild.member_count)
        embed.set_author(name=f"{guild.owner.display_name} ({guild.owner.name})", icon_url=guild.owner.display_avatar)
        embed.set_thumbnail(url=guild.icon)
        await self.bot.get_channel(1065611483897147502).send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        embed = discord.Embed(color=0xF44336, title=f"left {guild.name}")
        embed.add_field(name="members", value=guild.member_count)
        embed.set_author(name=f"{guild.owner.display_name} ({guild.owner.name})", icon_url=guild.owner.display_avatar)
        embed.set_thumbnail(url=guild.icon)
        await self.bot.get_channel(1065611483897147502).send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(logging(bot))
