<p align="center">
  <h1 align="center">ghstat</h1>
</p>

<p align="center">
  <strong>Analyze any GitHub profile from the terminal.</strong><br>
  Repos, languages, activity, and contribution insights — all from the command line.
</p>

<p align="center">
  <a href="https://github.com/Pavankumardhruv/ghstat/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Pavankumardhruv/ghstat?style=flat-square" alt="License"></a>
  <img src="https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/GitHub%20API-v3-black?style=flat-square&logo=github" alt="GitHub API">
</p>

---

ghstat fetches public GitHub data and renders it as rich terminal output — profile cards, repo rankings, language breakdowns with bar charts, and activity timelines.

No API key required for basic usage. Set `GITHUB_TOKEN` for higher rate limits.

## Quick Start

```bash
# Install
git clone https://github.com/Pavankumardhruv/ghstat.git
cd ghstat
pip install -e .

# Analyze a profile
ghstat profile torvalds

# List top repos
ghstat repos torvalds --limit 15

# Language breakdown
ghstat languages torvalds
```

## Commands

### `ghstat profile <username>`

Full profile overview — identity, stats, top repos, and 12-month activity chart.

```
╭──────────── @torvalds ────────────╮
│       Name  Linus Torvalds        │
│        Bio  —                     │
│   Location  Portland, OR          │
│                                   │
│  Public Repos  8                  │
│  Total Stars   ⭐ 221,402        │
│  Total Forks   🍴 52,118         │
│  Followers     223,819            │
│                                   │
│  Top Language  C                  │
│  Languages     4                  │
╰───────────────────────────────────╯
```

### `ghstat repos <username>`

Ranked repo table sorted by a weighted score (stars × 3 + forks × 2).

```
┌─────────────────── Top Repositories ───────────────────┐
│ Repository   │ Language │ Stars   │ Forks  │ Last Push │
├──────────────┼──────────┼─────────┼────────┼───────────┤
│ linux        │ C        │ 185,612 │ 45,201 │ 2026-04-… │
│ subsurface   │ C++      │ 2,891   │ 1,052  │ 2025-11-… │
└──────────────┴──────────┴─────────┴────────┴───────────┘
```

### `ghstat languages <username>`

Bar chart showing language distribution across all non-fork repos.

```
┌──────── Language Breakdown ────────┐
│ Language │ Repos │ %     │         │
├──────────┼───────┼───────┼─────────┤
│ C        │     3 │ 42.9% │ █████░░ │
│ C++      │     2 │ 28.6% │ ████░░░ │
│ Shell    │     1 │ 14.3% │ ██░░░░░ │
└──────────┴───────┴───────┴─────────┘
```

## Architecture

```
ghstat/
├── cli.py         # Typer CLI commands
├── api.py         # GitHub API client with pagination
├── analytics.py   # Scoring, language stats, activity timelines
└── display.py     # Rich terminal rendering (panels, tables, charts)
```

**Design decisions:**

- **No auth required** — Works with public GitHub API. Optional `GITHUB_TOKEN` raises the rate limit from 60 to 5,000 requests/hour.
- **Fork filtering** — Forks are excluded from all stats to show original work only.
- **Weighted ranking** — Repos are scored by `stars × 3 + forks × 2`, surfacing high-impact projects.
- **Pagination** — Handles users with 100+ repos by fetching all pages automatically.

## Optional: Set a GitHub Token

For heavy usage or private repo access:

```bash
export GITHUB_TOKEN=your-token-here
```

Generate one at [github.com/settings/tokens](https://github.com/settings/tokens) (no scopes needed for public data).

## Requirements

- Python 3.10+

## License

MIT License — see [LICENSE](LICENSE) for details.
