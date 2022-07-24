import os
import traceback

import disnake.http as http
from disnake import CommandInteraction
from disnake.ext.commands import InteractionBot

# Core handles registering commands, sync_commands should not be used.

proxy_on = os.environ.get("REST_PROXY") is not None

if proxy_on:
    http.Route.BASE = os.environ.get("REST_PROXY")
    print("Using proxy")
else:
    print("Not using proxy")

bot = InteractionBot(sync_commands=False)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Gateway: {await bot.http.get_gateway()}")
    print(f"Base: {http.Route.BASE}")


@bot.slash_command(
    name="github",
)
async def github(inter: CommandInteraction):
    await inter.response.defer()
    pass


async def on_error(
        inter: CommandInteraction,
        exception: Exception,
):
    await inter.edit_original_message("something went wrong")
    traceback.print_exception(exception)


bot.on_slash_command_error = lambda inter, exception: on_error(inter, exception)

bot.load_extension("gitget.repo")

if proxy_on:
    bot.run("evie")
else:
    bot.run(os.environ["DISCORD_TOKEN"])
