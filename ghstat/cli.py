import typer
from rich.console import Console

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
    console.print(f"[bold]Analyzing:[/bold] {username}")


@app.command()
def repos(
    username: str = typer.Argument(..., help="GitHub username"),
):
    """List and rank repositories by stars, forks, and activity."""
    console.print(f"[bold]Repos for:[/bold] {username}")


@app.command()
def languages(
    username: str = typer.Argument(..., help="GitHub username"),
):
    """Show language breakdown across all repositories."""
    console.print(f"[bold]Languages for:[/bold] {username}")


if __name__ == "__main__":
    app()
