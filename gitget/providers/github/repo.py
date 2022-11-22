import json
from datetime import datetime

from disnake import Embed
from github import GithubException

from ...cache import get, set
from ...enums import Emojis
from ...gitstance import gh_instance


async def fill_embed(embed: Embed, owner: str, repo: str) -> Embed:
    owner = owner.lower()
    repo = repo.lower()

    cached_entry = await get(f"{owner}/{repo}")

    if cached_entry is not None:
        return Embed.from_dict(json.loads(cached_entry))

    embed = await fetch_embed(embed, owner, repo)

    await set(f"{owner}/{repo}", json.dumps(embed.to_dict()), expire=60 * 5)

    return embed


async def fetch_embed(embed: Embed, owner: str, repo: str) -> Embed:
    try:
        res = gh_instance.get_repo(f"{owner}/{repo}")

        commits = res.get_commits()
        langs = res.get_languages()
        last_commit = res.get_commit(sha=commits[0].sha)
        branches = res.get_branches()
        contributors = res.get_contributors().get_page(0)

        total_bytes = 0
        for k, v in langs.items():
            total_bytes += v

        if len(langs) > 5:
            langs = dict(list(langs.items())[:5])

        try:
            repo_license = res.get_license()
        except GithubException:
            repo_license = None

        first_line_commit = last_commit.commit.message.splitlines()[0]

        embed.title = f"{Emojis.GITHUB.value} {res.owner.login}/{res.name}"
        embed.url = res.html_url
        embed.description = f"**{last_commit.author.login}** {first_line_commit} [`{last_commit.sha[0:7]}`]({last_commit.html_url})\n> {res.description}"
        embed.timestamp = res.updated_at

        embed.set_footer(text="Last updated")

        license_text = "No license"
        if repo_license is not None:
            license_text = f"[{repo_license.license.name}]({repo_license.html_url})"

        about = {
            "License": license_text,
            "Stars": f"{res.stargazers_count:,}",
            "Forks": f"{res.forks_count:,}",
            "Watchers": f"{res.subscribers_count:,}",
            "Open Issues": f"{res.open_issues_count:,}",
            "Commits": f"{commits.totalCount:,}",
            "Branches": f"{branches.totalCount:,}",
        }

        embed.add_field(
            name="About",
            value="\n".join(
                f"{Emojis.BULLET_POINT.value} **{k}**: {v}" for k, v in about.items()
            ),
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

        if len(contributors) > 5:
            contributors = contributors[:5]

        embed.add_field(
            name="Top Contributors",
            value="\n".join(
                f"{Emojis.BULLET_POINT.value} **{u.login}**: {u.contributions:,} commits"
                for u in contributors
            ),
            inline=True,
        )

        return embed
    except GithubException as e:
        match e.status:
            case 404:
                embed.title = "Repo not found"
            case 409:
                embed.title = "Git Repository is empty"
            case _:
                embed.title = "Unknown error"
                print(e)

    return embed
