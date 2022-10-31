import json
import random
import subprocess

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

from helpers import checks


class Randomizer(commands.Cog, name="randomizer-dev"):
    def __init__(self, bot):
        self.bot = bot
        self.randomizer_version = "DK64Randomizer-Dev"

    @commands.hybrid_command(
        name="presets_dev",
        description="Lists the presets available.",
    )
    async def presets_dev(self, context: Context):
        preset_data = []
        with open(f"{self.randomizer_version}/static/presets/preset_files.json") as preset_files:
            file_contents = preset_files.read()
            for preset in json.loads(file_contents).get("progression"):
                with open(f"{self.randomizer_version}/static/presets/{preset}") as preset_file_data:
                    preset_content = preset_file_data.read()
                    content = json.loads(preset_content)
                    if str(content.get("description", "")).strip():
                        preset_data_built = {"name": content.get("name"), "description": content.get("description")}
                        preset_data.append(preset_data_built)
        embed = discord.Embed(title="Presets", description="List of available presets:", color=0x9C84EF)
        data = []
        for i in preset_data:
            name = i.get("name")
            description = i.get("description")
            data.append(f"{name} - {description}")
        preset_text = "\n".join(data)
        embed.add_field(name="Current Presets", value=f"```{preset_text}```", inline=False)
        await context.send(embed=embed)

    @commands.hybrid_command(
        name="generate_dev",
        description="Generates a seed with the preset or settings provided.",
    )
    @app_commands.describe(setting="The preset or settings string to use.")
    async def generate_dev(self, context: Context, *, setting: str):
        preset_data = []
        with open(f"{self.randomizer_version}/static/presets/preset_files.json") as preset_files:
            file_contents = preset_files.read()
            for found_preset in json.loads(file_contents).get("progression"):
                with open(f"{self.randomizer_version}/static/presets/{found_preset}") as preset_file_data:
                    preset_content = preset_file_data.read()
                    content = json.loads(preset_content)
                    if str(content.get("description", "")).strip():
                        preset_data.append(str(content.get("name", "")).lower())

        if setting.lower() in preset_data:
            seed = str(random.randint(0, 100000000))
            embed = discord.Embed(title="Generating Seed", description="Please Wait.", color=0x9C84EF)
            await context.send(embed=embed)
            file_name = f"dk64-{seed}.lanky"
            subprocess.call(
                ["python3", "cli.py", "--preset", setting, "--output", file_name, "--seed", seed],
                cwd=f"./{self.randomizer_version}",
            )
            await context.send(file=discord.File(f"./{self.randomizer_version}/{file_name}"))
        else:
            try:
                seed = str(random.randint(0, 100000000))
                embed = discord.Embed(title="Generating Seed", description="Please Wait.", color=0x9C84EF)
                await context.send(embed=embed)
                file_name = f"dk64-{seed}.lanky"
                subprocess.call(
                    ["python3", "cli.py", "--settings_string", setting, "--output", file_name, "--seed", seed],
                    cwd=f"./{self.randomizer_version}",
                )
                await context.send(file=discord.File(f"./{self.randomizer_version}/{file_name}"))
            except Exception:
                raise checks.InvalidPreset


async def setup(bot):
    await bot.add_cog(Randomizer(bot))
