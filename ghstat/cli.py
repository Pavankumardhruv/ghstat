import typer
from rich.console import Console

from ghstat.analytics import (
    activity_timeline,
    language_breakdown,
    profile_summary,
    top_repos,
)
from ghstat.api import fetch_repos, fetch_user
from ghstat.display import show_activity, show_languages, show_profile, show_repos

app = typer.Typer(
    name="ghstat",
    help="Analyze any GitHub profile from the terminal.",
    add_completion=False,
)
console = Console()


@app.command()
def profile(
    username: str = typer.Argument(..., help="GitHub username to analyze"),
):
    """Show a comprehensive profile overview."""
    with console.status(f"Fetching data for @{username}..."):
        user = fetch_user(username)
        repos = fetch_repos(username)

    summary = profile_summary(user, repos)
    show_profile(summary)

    top = top_repos(repos, limit=5)
    if top:
        console.print()
        show_repos(top)

    timeline = activity_timeline(repos)
    if timeline:
        show_activity(timeline)


@app.command()
def repos(
    username: str = typer.Argument(..., help="GitHub username"),
    limit: int = typer.Option(10, "--limit", "-n", help="Number of repos to show"),
):
    """List and rank repositories by stars, forks, and activity."""
    with console.status(f"Fetching repos for @{username}..."):
        all_repos = fetch_repos(username)

    if not all_repos:
        console.print(f"[dim]No public repos found for @{username}[/dim]")
        raise typer.Exit()

    ranked = top_repos(all_repos, limit=limit)
    show_repos(ranked)
    console.print(f"\n[dim]Showing top {len(ranked)} of {len(all_repos)} repos (forks excluded)[/dim]")


@app.command()
def languages(
    username: str = typer.Argument(..., help="GitHub username"),
):
    """Show language breakdown across all repositories."""
    with console.status(f"Fetching repos for @{username}..."):
        all_repos = fetch_repos(username)

    breakdown = language_breakdown(all_repos)
    if not breakdown:
        console.print(f"[dim]No language data found for @{username}[/dim]")
        raise typer.Exit()

    show_languages(breakdown)


if __name__ == "__main__":
    app()
