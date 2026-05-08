from rich.table import Table
from rich.console import Console
from datetime import datetime
from pathlib import Path

console = Console()


def format_size(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    else:
        return f"{size / (1024 * 1024):.1f} MB"


def format_time(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")


def shorten_path(path: str) -> str:
    """
    Replace home directory with ~ for cleaner display.
    """
    return path.replace(str(Path.home()), "~")


def display_results(results):
    table = Table(title="WLX Results", header_style="bold cyan")

    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Name", style="white")
    table.add_column("Size", justify="right", style="green")
    table.add_column("Modified", style="magenta")
    table.add_column("Path", style="blue", overflow="fold")
    table.add_column("Tags", style="yellow", overflow="fold")

    for row in results:

    # Path formatting
        path_display = shorten_path(row["path"])

    # Tag formatting
        tags = row.get("tags", "")

        if tags:

        # Split tags and clean empty values
            tags_list = [
                tag.strip()
                for tag in tags.split(",")
                if tag.strip()
            ]

        # Limit displayed tags
            max_tags = 5

            tags_display = ", ".join(tags_list[:max_tags])

            if len(tags_list) > max_tags:
                tags_display += ", ..."

        else:
            tags_display = "-"

        #Add row
        table.add_row(
            str(row["id"]),
            row["name"],
            format_size(row["size"]),
            format_time(row["mtime"]),
            path_display,
            tags_display
        )

    console.print(table)
    console.print(
    f"[bold cyan][*] Found {len(results)} Matching Wordlists.[/bold cyan]\n"
)
    