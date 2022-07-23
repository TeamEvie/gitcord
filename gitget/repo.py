from __main__ import github

import disnake
from disnake import CommandInteraction
from disnake.ext.commands import Cog, Bot
from github import GithubException

from .enums import Emojis, Colors
from .gitstance import gh_instance


class Repo(Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @github.sub_command()
    async def repo(self, inter: CommandInteraction, owner: str, repo: str) -> None:
        try:
            repo = gh_instance.get_repo(f"{owner}/{repo}")

            commits = repo.get_commits()
            langs = repo.get_languages()
            last_commit = repo.get_commit(sha=commits[0].sha)
            branches = repo.get_branches()
            contributors = repo.get_contributors()

            total_bytes = 0
            for k, v in langs.items():
                total_bytes += v

            if len(langs) > 5:
                langs = list(langs.items())
                langs.sort(key=lambda x: x[1], reverse=True)
                langs = langs[:5]

            try:
                repo_license = repo.get_license()
            except GithubException:
                repo_license = None

            description = f"**{last_commit.author.login}** {last_commit.commit.message} [`{last_commit.sha[0:7]}`]({last_commit.html_url})\n> {repo.description}"

            embed = disnake.Embed(
                title=f"{Emojis.GITHUB.value} {repo.owner.login}/{repo.name}",
                url=repo.html_url,
                description=description,
                timestamp=repo.updated_at,
                colour=Colors.DARK_MODE_BLEND.value
            )

            embed.set_footer(text="Last updated")

            license_text = "No license"
            if repo_license is not None:
                license_text = f"[{repo_license.license.name}]({repo_license.html_url})"

            about = {
                "License": license_text,
                "Stars": repo.stargazers_count,
                "Forks": repo.forks_count,
                "Watchers": repo.subscribers_count,
                "Open Issues": repo.open_issues_count,
                "Commits": commits.totalCount,
                "Branches": branches.totalCount,
            }

            embed.add_field(
                name="About",
                value="\n".join(f"{Emojis.BULLET_POINT.value} **{k}**: {v}" for k, v in about.items()),
                inline=True,
            )
            if len(langs) > 0:
                embed.add_field(
                    name=f"Languages ({len(langs)})",
                    value="\n".join(
                        f"{Emojis.BULLET_POINT.value} **{k}**: {v / total_bytes * 100:.2f}%"
                        for k, v in langs.items()
                    ),
                    inline=True,
                )

            if contributors.totalCount > 5:
                contributors = contributors[:5]

            embed.add_field(
                name="Top Contributors",
                value="\n".join(
                    f"{Emojis.BULLET_POINT.value} **{u.login}**: {u.contributions} commits"
                    for u in contributors
                ),
                inline=True,
            )

            await inter.edit_original_message(embed=embed)
        except GithubException as e:
            match e.status:
                case 404:
                    await inter.edit_original_message("repo not found")
                case 409:
                    await inter.edit_original_message("Git Repository is empty.")
                case _:
                    await inter.edit_original_message("unknown error")
                    print(e)


def setup(bot: Bot) -> None:
    bot.add_cog(Repo(bot))
