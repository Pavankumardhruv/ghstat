from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from ghstat.api import Repo

console = Console()


def show_profile(summary: dict) -> None:
    grid = Table.grid(padding=(0, 2))
    grid.add_column(style="bold cyan", justify="right")
    grid.add_column()

    grid.add_row("Name", summary["name"])
    grid.add_row("Bio", summary["bio"])
    grid.add_row("Location", summary["location"])
    grid.add_row("Company", summary["company"])
    grid.add_row("Account Age", summary["account_age"])
    grid.add_row("", "")
    grid.add_row("Public Repos", str(summary["public_repos"]))
    grid.add_row("Total Stars", f"⭐ {summary['total_stars']}")
    grid.add_row("Total Forks", f"🍴 {summary['total_forks']}")
    grid.add_row("Followers", str(summary["followers"]))
    grid.add_row("Following", str(summary["following"]))
    grid.add_row("", "")
    grid.add_row("Top Language", summary["top_language"])
    grid.add_row("Languages Used", str(summary["languages_used"]))

    panel = Panel(
        grid,
        title=f"[bold]@{summary['username']}[/bold]",
        border_style="bright_blue",
        padding=(1, 2),
    )
    console.print(panel)


def show_repos(repos: list[Repo]) -> None:
    table = Table(title="Top Repositories", border_style="dim")
    table.add_column("Repository", style="cyan bold")
    table.add_column("Language", style="yellow")
    table.add_column("Stars", justify="right")
    table.add_column("Forks", justify="right")
    table.add_column("Last Push", style="dim")
    table.add_column("Description", max_width=40)

    for r in repos:
        pushed = r.pushed_at[:10] if r.pushed_at else "-"
        desc = (r.description or "-")[:40]
        table.add_row(
            r.name,
            r.language or "-",
            str(r.stars),
            str(r.forks),
            pushed,
            desc,
        )

    console.print(table)


def show_languages(breakdown: list[tuple[str, int, float]]) -> None:
    table = Table(title="Language Breakdown", border_style="dim")
    table.add_column("Language", style="bold")
    table.add_column("Repos", justify="right")
    table.add_column("%", justify="right")
    table.add_column("", min_width=30)

    for lang, count, pct in breakdown:
        bar_width = int(pct / 100 * 30)
        bar = Text("█" * bar_width, style="cyan") + Text("░" * (30 - bar_width), style="dim")
        table.add_row(lang, str(count), f"{pct}%", bar)

    console.print(table)


def show_activity(timeline: list[tuple[str, int]]) -> None:
    if not timeline:
        console.print("[dim]No recent activity.[/dim]")
        return

    max_count = max(c for _, c in timeline)
    console.print("\n[bold]Activity (last 12 months)[/bold]\n")

    for month, count in timeline:
        bar_width = int(count / max_count * 30) if max_count else 0
        bar = "▓" * bar_width
        console.print(f"  {month}  [cyan]{bar}[/cyan] {count}")

    console.print()
