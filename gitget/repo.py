from __main__ import bot
from disnake import CommandInteraction, Embed
from disnake.ext.commands import Bot, Cog
from github import GithubException

from .enums import Colors, Emojis, SupportedGitProviders
from .gitstance import gh_instance
from .providers.github.repo import fill_embed as gh_fill_embed


class Repo(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @bot.slash_command(description="Get information about a repository")
    async def repo(
        self,
        inter: CommandInteraction,
        provider: SupportedGitProviders,
        owner: str,
        repo: str,
    ) -> None:
        await inter.response.defer()
        embed = Embed(
            colour=Colors.DARK_MODE_BLEND.value,
        )

        match provider:
            case SupportedGitProviders.GitHub.value:
                embed = await gh_fill_embed(embed, owner, repo)
            case _:
                embed.title = "Unsupported provider"
        await inter.edit_original_message(embed=embed)


def setup(bot: Bot) -> None:
    try:
        bot.add_cog(Repo(bot))
    except Exception as e:
        # add_cog was called twice, this is a bug in disnake i think.
        # TODO: Look into why this is happening
        pass
