import os
import traceback

import disnake.http as http
from disnake import CommandInteraction
from disnake.ext.commands import InteractionBot

bot = InteractionBot()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


async def on_error(
    inter: CommandInteraction,
    exception: Exception,
):
    await inter.edit_original_message("something went wrong")
    traceback.print_exception(exception)


bot.on_slash_command_error = lambda inter, exception: on_error(inter, exception)

bot.load_extension("gitget.repo")

bot.run(os.environ["DISCORD_TOKEN"])
