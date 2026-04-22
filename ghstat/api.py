import os
from dataclasses import dataclass, field
from datetime import datetime

import httpx

API_BASE = "https://api.github.com"


def _headers() -> dict[str, str]:
    headers = {"Accept": "application/vnd.github.v3+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _get(path: str, params: dict | None = None) -> dict | list:
    url = f"{API_BASE}{path}"
    response = httpx.get(url, headers=_headers(), params=params, timeout=15.0)
    if response.status_code == 404:
        raise ValueError(f"GitHub user or resource not found: {path}")
    if response.status_code == 403:
        raise RuntimeError(
            "GitHub API rate limit exceeded. Set GITHUB_TOKEN to increase your limit:\n"
            "  export GITHUB_TOKEN=your-token-here"
        )
    response.raise_for_status()
    return response.json()


def _get_all_pages(path: str, per_page: int = 100) -> list:
    results = []
    page = 1
    while True:
        data = _get(path, params={"per_page": per_page, "page": page})
        if not data:
            break
        results.extend(data)
        if len(data) < per_page:
            break
        page += 1
    return results


@dataclass
class UserProfile:
    login: str
    name: str | None
    bio: str | None
    company: str | None
    location: str | None
    blog: str | None
    public_repos: int
    followers: int
    following: int
    created_at: str


@dataclass
class Repo:
    name: str
    description: str | None
    language: str | None
    stars: int
    forks: int
    is_fork: bool
    pushed_at: str
    html_url: str
    topics: list[str] = field(default_factory=list)


def fetch_user(username: str) -> UserProfile:
    data = _get(f"/users/{username}")
    return UserProfile(
        login=data["login"],
        name=data.get("name"),
        bio=data.get("bio"),
        company=data.get("company"),
        location=data.get("location"),
        blog=data.get("blog"),
        public_repos=data["public_repos"],
        followers=data["followers"],
        following=data["following"],
        created_at=data["created_at"],
    )


def fetch_repos(username: str) -> list[Repo]:
    data = _get_all_pages(f"/users/{username}/repos")
    repos = []
    for r in data:
        if r.get("fork"):
            continue
        repos.append(Repo(
            name=r["name"],
            description=r.get("description"),
            language=r.get("language"),
            stars=r["stargazers_count"],
            forks=r["forks_count"],
            is_fork=r["fork"],
            pushed_at=r.get("pushed_at", ""),
            html_url=r["html_url"],
            topics=r.get("topics", []),
        ))
    return sorted(repos, key=lambda r: r.stars, reverse=True)


def account_age_years(created_at: str) -> float:
    created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    now = datetime.now(created.tzinfo)
    return round((now - created).days / 365.25, 1)
