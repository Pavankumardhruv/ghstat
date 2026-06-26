from collections import Counter
from datetime import datetime

from ghstat.api import Repo, UserProfile, account_age_years


def language_breakdown(repos: list[Repo]) -> list[tuple[str, int, float]]:
    counts = Counter(r.language for r in repos if r.language)
    total = sum(counts.values())
    return [
        (lang, count, round(count / total * 100, 1))
        for lang, count in counts.most_common()
    ]


def top_repos(repos: list[Repo], limit: int = 10) -> list[Repo]:
    scored = sorted(repos, key=lambda r: r.stars * 3 + r.forks * 2, reverse=True)
    return scored[:limit]


def activity_timeline(repos: list[Repo]) -> list[tuple[str, int]]:
    monthly: Counter[str] = Counter()
    for r in repos:
        if not r.pushed_at:
            continue
        dt = datetime.fromisoformat(r.pushed_at.replace("Z", "+00:00"))
        key = dt.strftime("%Y-%m")
        monthly[key] += 1
    return sorted(monthly.items())[-12:]


def profile_summary(user: UserProfile, repos: list[Repo]) -> dict:
    total_stars = sum(r.stars for r in repos)
    total_forks = sum(r.forks for r in repos)
    langs = language_breakdown(repos)
    top_lang = langs[0][0] if langs else "None"
    age = account_age_years(user.created_at)

    return {
        "username": user.login,
        "name": user.name or user.login,
        "bio": user.bio or "-",
        "location": user.location or "-",
        "company": user.company or "-",
        "account_age": f"{age} years",
        "public_repos": len(repos),
        "total_stars": total_stars,
        "total_forks": total_forks,
        "followers": user.followers,
        "following": user.following,
        "top_language": top_lang,
        "languages_used": len(langs),
    }
