import discord
from discord.ext import commands
from discord.ext.commands import Context


class Roles(commands.Cog, name="roles"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="racerole",
        description="Adds or removes the race roll.",
    )
    async def racerole(self, context: Context) -> None:
        user_roles = context.author.roles
        for role in user_roles:
            if role.name.lower() == "racing":
                await context.author.remove_roles(role)
                await context.message.add_reaction("👍")
                return
        roles = await context.guild.fetch_roles()
        role = None
        for server_role in roles:
            if server_role.name.lower() == "racing":
                role = server_role
                break
        else:
            role = await context.guild.create_role(name="Racing")
        await context.author.add_roles(role)
        await context.message.add_reaction("👍")


async def setup(bot):
    await bot.add_cog(Roles(bot))
