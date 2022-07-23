import os
import traceback

from disnake import CommandInteraction
from disnake.ext.commands import InteractionBot
from dotenv import load_dotenv

load_dotenv()

# Core handles registering commands, sync_commands should not be used.
if os.environ.get("PROXY_URL") is not None:
    print("Using proxy")
    bot = InteractionBot(sync_commands=False, proxy=os.environ["PROXY_URL"])
else:
    print("Not using proxy")
    bot = InteractionBot(sync_commands=False)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


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

bot.load_extension("repo")

bot.run(os.environ["DISCORD_TOKEN"])
