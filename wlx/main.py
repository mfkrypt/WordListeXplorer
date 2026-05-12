#!/usr/bin/env python3
#Importing all wlx associated libraries
from wlx.core import scanner, search, config, db, variables
from wlx.ui import display

#Importing all packages
from rich.table import Table
from rich.console import Console
from pathlib import Path
import subprocess
import urllib.request
import typer
import os

VERSION = "1.0.1"
VERSION_URL = "https://raw.githubusercontent.com/ZeroPrime9/WordListeXplorer/main/VERSION"


app = typer.Typer(
    help="""
WLX — WordList eXplorer by Farzan Nobi (ZeroPrime9)

A Local Wordlist Intelligence CLI For Offensive Security Workflows.

Examples:
  wlx search admin
  wlx search login --filter api,auth
  wlx use 12 WORDLIST
""",
    no_args_is_help=True,
    add_completion=False
)

#Handling WLX Config Command
config_app = typer.Typer(help="Manage WLX Directories & Configuration.")
app.add_typer(config_app, name="config")

#Initialising Rich Console
console = Console()


@config_app.command("addir")
def config_add(path: str):
    """
    Add Directories into WLX Configuration for Scanning
    """
    added = config.add_directory(path)

    if added:
        typer.secho(f"[+] Added: {path}", fg=typer.colors.GREEN)
    else:
        typer.secho("[!] Directory already exists in config.", fg=typer.colors.YELLOW)



@config_app.command("rmdir")
def config_remove(index: int):
    """
    Remove directories from WLX Configuration by ID
    """
    dirs = config.get_directories()

    #Checking for Invalid ID Numbers
    if index < 1 or index > len(dirs):
        console.print("[red][!] Invalid ID[/red]")
        raise typer.Exit(code=1)

    target = dirs[index - 1]

    #Removing Directory
    console.print(f"[yellow][!] Remove directory:[/yellow] [blue]{target}[/blue]? (y/n): ", end="")
    choice = input().strip().lower()

    if choice != "y":
        console.print("[yellow][!] Operation cancelled[/yellow]")
        raise typer.Exit()

    removed = config.remove_directory_by_index(index)

    if removed:
        console.print(f"[red][*] Removed:[/red] [blue]{removed}[/blue]")



@config_app.command("list")
def config_list():
    """
    List all configured directories from WLX Configuration.
    """
    dirs = config.get_directories()

    if not dirs:
        console.print("[red][!] No directories configured[/red]")
        return

    table = Table(title="Configured Directories", header_style="bold cyan")

    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Path", style="blue", overflow="fold")

    for idx, d in enumerate(dirs, start=1):
        # Shortening the Home Path
        d_display = d.replace(str(Path.home()), "~")
        table.add_row(str(idx), d_display)

    console.print(table)
    
@config_app.command("index")
def scan(directory: str = None):
    """
    Scan & Index Wordlists From Configured Directories.
    """

    db.init_db()

    paths = []

    if directory:
        paths.append(directory)

    else:
        paths = config.get_directories()

        if not paths:
            typer.secho(
                "[!] No directories configured. Use 'wlx config addir <path>'",
                fg=typer.colors.RED
            )
            raise typer.Exit(code=1)

    total_files = 0
    scanned_directories = 0

    console.print(
        "[bold cyan][*] Starting WLX Indexer...[/bold cyan]"
    )

    console.print(
        "[dim]This may take a moment depending on wordlist size and directory count.[/dim]"
    )

    with console.status(
        "[bold cyan]Scanning Directories & Indexing Wordlists...[/bold cyan]",
        spinner="dots"
    ):

        for dir_path in paths:

            path = Path(dir_path)

            if not path.exists() or not path.is_dir():
                console.print(
                    f"[bold red][!] Skipping invalid path:[/bold red] {dir_path}"
                )
                continue

            scanned_directories += 1

            files = scanner.scan_directory(path)

            total_files += len(files)

            for file in files:
                db.upsert_wordlist(file)

    console.print()

    console.print(
        f"[bold green][+] Scan completed successfully.[/bold green]"
    )

    console.print(
        f"[bold cyan][*] Indexed Wordlists: {total_files} [/bold cyan]"
    )

    console.print(
        f"[bold cyan][*] Directories scanned:[/bold cyan] {scanned_directories}\n"
    )


@config_app.command("diag")
def diagnostics():
    """
    Display WLX environment diagnostics and health information.
    """

    console.print("\n[bold cyan]WLX Diagnostics[/bold cyan]\n")

    wlx_dir = Path.home() / ".wlx"
    db_file = wlx_dir / "wlx.db"
    config_file = wlx_dir / "config.json"
    session_file = wlx_dir / "session.env"

    # Checking WLX Directory

    if wlx_dir.exists():
        console.print("[bold green][+] WLX directory exists[/bold green]")
    else:
        console.print("[bold red][!] WLX directory missing[/bold red]")


    #Checking  Database

    if db_file.exists():
        console.print("[bold green][+] Database accessible[/bold green]")
    else:
        console.print("[bold red][!] Database not found[/bold red]")


    # Checking Config File


    if config_file.exists():
        console.print("[bold green][+] Configuration file detected[/bold green]")
    else:
        console.print("[bold yellow][!] No configuration file found[/bold yellow]")


    # Checking Configured Directories

    try:
        directories = config.get_directories()

        if directories:
            console.print(
                f"[bold green][+] {len(directories)} configured directories[/bold green]"
            )

            for directory in directories:

                path = Path(directory)

                if path.exists():
                    console.print(
                        f"    [green]•[/green] {directory}"
                    )
                else:
                    console.print(
                        f"    [red]• Missing:[/red] {directory}"
                    )

        else:
            console.print(
                "[bold yellow][!] No configured directories[/bold yellow]"
            )

    except Exception:
        console.print(
            "[bold red][!] Failed to load configured directories[/bold red]"
        )


    # Checking Indexed Wordlists

    try:
        count = db.get_wordlist_count()

        console.print(
            f"[bold green][+] {count} indexed wordlists[/bold green]"
        )

    except Exception:
        console.print(
            "[bold red][!] Failed to read database entries[/bold red]"
        )


    # PATH Check

    local_bin = str(Path.home() / ".local" / "bin")

    if local_bin in os.environ.get("PATH", ""):
        console.print(
            "[bold green][+] PATH configured correctly[/bold green]"
        )
    else:
        console.print(
            "[bold yellow][!] ~/.local/bin not found in PATH[/bold yellow]"
        )


    # Checking Shell Integration

    shell = os.environ.get("SHELL", "")

    shell_rc = None

    if "bash" in shell:
        shell_rc = Path.home() / ".bashrc"

    elif "zsh" in shell:
        shell_rc = Path.home() / ".zshrc"

    if shell_rc and shell_rc.exists():

        content = shell_rc.read_text()

        if "wlxuse()" in content:
            console.print(
                "[bold green][+] WLX shell integration enabled[/bold green]"
            )
        else:
            console.print(
                "[bold yellow][!] WLX shell integration not detected[/bold yellow]"
            )

  
    # Active WLX Variables


    if session_file.exists():

        with open(session_file, "r") as f:
            variables = [
                line.strip()
                for line in f.readlines()
                if line.strip()
            ]

        console.print(
            f"[bold green][+] {len(variables)} active WLX variables[/bold green]"
        )

    else:
        console.print(
            "[bold yellow][!] No active WLX variables[/bold yellow]"
        )

    console.print()



@app.command("search")
def search_cmd(
    query: str = typer.Argument("", help="Search keyword"),
    filters: str = typer.Option(None, "--filter", "-f", help="Filter results by tags (comma-separated)"),
):
    
    """
    Search Indexed Wordlists By Keyword Or Filter.
    """
    
    db.init_db()

    # Prevent Empty Searches
    if not query.strip() and not filters:
        typer.secho("[!] Please provide a search query or a filter", fg=typer.colors.YELLOW)
        raise typer.Exit()

    tags = None

    if filters:
        tags = [
            t.strip().lower()
            for t in filters.split(",")
            if t.strip()
        ]

    results = search.search_wordlists(query, tags)

    if not results:

        if query.strip():
            typer.secho(
                f"[!] No results found for '{query}'",
                fg=typer.colors.RED
            )

        else:
            typer.secho(
                "[!] No results found for provided filters.",
                fg=typer.colors.RED
            )

        raise typer.Exit(code=1)

    typer.secho(
        f"[*] Found {len(results)} matching wordlists.",
        fg=typer.colors.CYAN
    )

    display.display_results(results)
    
   
    
@app.command()
def use(
    wordlist_id: int,
    variable: str
):
    """
    Assign a wordlist path to an environment variable.
    """

    result = db.get_wordlist_by_id(wordlist_id)

    if not result:
        typer.secho("[!] Invalid wordlist ID.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    # Normalize variable name
    variable = variable.upper()

    path = result["path"]

    print(f'export {variable}="{path}"')
  
    
@app.command()
def tag(wordlist_ids: str, tags: str):
    """
    Add Custom Tags To One or More Wordlists.
    """

    db.init_db()

    ids = [
        int(i.strip())
        for i in wordlist_ids.split(",")
        if i.strip().isdigit()
    ]

    tag_list = [
        t.strip().lower()
        for t in tags.split(",")
        if t.strip()
    ]

    if not ids:
        typer.secho(
            "[!] No valid wordlist IDs provided.",
            fg=typer.colors.RED
        )
        raise typer.Exit(code=1)

    if not tag_list:
        typer.secho(
            "[!] No valid tags provided.",
            fg=typer.colors.RED
        )
        raise typer.Exit(code=1)

    tagged_count = 0

    for wordlist_id in ids:

        result = db.get_wordlist_by_id(wordlist_id)

        if not result:
            typer.secho(
                f"[!] Invalid wordlist ID: {wordlist_id}",
                fg=typer.colors.RED
            )
            continue

        for single_tag in tag_list:
            db.add_tag(wordlist_id, single_tag)

        tagged_count += 1

    typer.secho(
        f"[+] Applied tags [{', '.join(tag_list)}] to {tagged_count} wordlists.",
        fg=typer.colors.GREEN
    )



@app.command()
def untag(wordlist_ids: str, tags: str):
    """
    Remove custom tags from one or more wordlists.
    """

    db.init_db()

    ids = [
        int(i.strip())
        for i in wordlist_ids.split(",")
        if i.strip().isdigit()
    ]

    tag_list = [
        t.strip().lower()
        for t in tags.split(",")
        if t.strip()
    ]

    if not ids:
        typer.secho(
            "[!] No valid wordlist IDs provided.",
            fg=typer.colors.RED
        )
        raise typer.Exit(code=1)

    if not tag_list:
        typer.secho(
            "[!] No valid tags provided.",
            fg=typer.colors.RED
        )
        raise typer.Exit(code=1)

    untagged_count = 0

    for wordlist_id in ids:

        result = db.get_wordlist_by_id(wordlist_id)

        if not result:
            typer.secho(
                f"[!] Invalid wordlist ID: {wordlist_id}",
                fg=typer.colors.RED
            )
            continue

        for single_tag in tag_list:
            db.remove_tag(wordlist_id, single_tag)

        untagged_count += 1

    typer.secho(
        f"[+] Removed tags [{', '.join(tag_list)}] from {untagged_count} wordlists.",
        fg=typer.colors.GREEN
    )


@app.command()
def stats():
    """
    Display WLX Statistics & Indexing Information.
    """
    db.init_db()

    total_wordlists = db.get_wordlist_count()
    directories = config.get_directories()
    
    #Displaying Main Stats Table
    table = Table()

    table.add_column("Status", style="white")
    table.add_column("Value", style="green")

    table.add_row("Indexed Wordlists", str(total_wordlists))
    table.add_row("Configured Directories", str(len(directories)))
    table.add_row("Database Path", str(db.DB_PATH))
    

    console.print(table)  
    
       # Print Directory Listing
    if directories:
        dir_table = Table()

        dir_table.add_column("ID", style="cyan", justify="right")
        dir_table.add_column("Configured Path", style="blue")

        for idx, d in enumerate(directories, start=1):
        # Optional: shorten home path
            d_display = d.replace(str(Path.home()), "~")

            dir_table.add_row(str(idx), d_display)

        console.print(dir_table)
    
    else:
        console.print("[red]No directories configured[/red]")  
        

@app.command("vars")
def list_variables():
    """
    Display active WLX environment variables.
    """

    from rich.table import Table
    from rich.console import Console

    vars_data = variables.load_variables()

    if not vars_data:
        typer.secho("[!] No WLX variables found.", fg=typer.colors.YELLOW)
        raise typer.Exit()

    table = Table(title="WLX Variables")

    table.add_column("Variable", style="cyan")
    table.add_column("Path", style="green")

    for var, path in vars_data.items():
        table.add_row(var, path)

    console = Console()
    console.print(table) 

    
@app.command()
def version():
    """
    Display WLX version information.
    """

    console.print(
        f"[bold cyan]WordListeXplorer (WLX):[/bold cyan] [bold red]v{VERSION}[/bold red]"
    )
    
    
@app.command()
def update():
    """
    Check for WLX updates and install the latest version.
    """

    console.print("\n[bold cyan][*] Checking for updates...[/bold cyan]\n")

    #Fetching Latest Version
    try:

        response = urllib.request.urlopen(VERSION_URL)

        latest_version = response.read().decode().strip()

    except Exception as e:

        console.print(
            f"[bold red][!] Failed to check updates:[/bold red] {e}"
        )

        raise typer.Exit(code=1)


    #Check if version matches
    if latest_version == VERSION:

        console.print(
            "[bold green][+] WLX is already up to date.[/bold green]"
        )

        raise typer.Exit()


    console.print(
        f"[bold green][+] Update available:[/bold green] {latest_version}"
    )

    console.print(
        f"[bold yellow][*] Current version:[/bold yellow] {VERSION}\n"
    )

    confirm = typer.prompt(
        "Do you want to update? [y/n]"
    ).strip().lower()

    if confirm != "y":

        console.print(
            "\n[bold yellow][*] Update cancelled.[/bold yellow]"
        )

        raise typer.Exit()

    
    # Read Installation Path
    install_path_file = Path.home() / ".wlx" / "install_path"

    if not install_path_file.exists():

        console.print(
            "[bold red][!] Installation path not found.[/bold red]"
        )

        raise typer.Exit(code=1)

    install_path = install_path_file.read_text().strip()

    repo_path = Path(install_path)

    if not repo_path.exists():

        console.print(
            "[bold red][!] WLX installation directory missing.[/bold red]"
        )

        raise typer.Exit(code=1)

    #Git Pull Update
    console.print(
        "\n[bold cyan][*] Pulling latest changes...[/bold cyan]"
    )

    try:

        subprocess.run(
            ["git", "pull"],
            cwd=repo_path,
            check=True
        )

    except subprocess.CalledProcessError:

        console.print(
            "[bold red][!] Failed to pull latest updates.[/bold red]"
        )

        raise typer.Exit(code=1)


    #Reinstall WLX
    console.print(
        "[bold cyan][*] Installing latest WLX version...[/bold cyan]"
    )

    venv_pip = Path.home() / ".wlx" / "venv" / "bin" / "pip"

    try:

        subprocess.run(
            [str(venv_pip), "install", "."],
            cwd=repo_path,
            check=True
        )

    except subprocess.CalledProcessError:

        console.print(
            "[bold red][!] Failed to install latest version.[/bold red]"
        )

        raise typer.Exit(code=1)

    #Display Ouput
    console.print(
        f"\n[bold green][+] WLX updated successfully to v{latest_version}[/bold green]"
    )

    console.print(
        "\n[bold cyan][*] Restart your shell [/bold cyan]"
    )

    console.print(
        "    exec $SHELL\n"
    )



@config_app.command("reset")
def reset():
    """
    Reset WLX configuration, database, and session variables.
    """

    typer.secho(
        "\n[!] WARNING: This will permanently delete:",
        fg=typer.colors.YELLOW
    )

    typer.echo("    • Configured directories")
    typer.echo("    • Indexed database")
    typer.echo("    • WLX session variables\n")

    confirm = typer.prompt(
        "Are you sure? [y/n]"
    ).strip().lower()

    if confirm != "y":
        typer.secho(
            "[*] Reset cancelled.",
            fg=typer.colors.YELLOW
        )
        raise typer.Exit()

    files_to_remove = [
        Path.home() / ".wlx" / "config.json",
        Path.home() / ".wlx" / "wlx.db",
        Path.home() / ".wlx" / "session.env"
    ]

    removed = 0

    for file in files_to_remove:

        if file.exists():
            file.unlink()
            removed += 1

    typer.secho(
        f"[+] WLX reset completed successfully. Removed {removed} files.",
        fg=typer.colors.GREEN
    )


def main():
    try:
        app()

    except KeyboardInterrupt:
        console.print(
            "\n[bold yellow][!] Operation interrupted by user.[/bold yellow]"
        )

    except Exception as e:
        console.print(
            f"\n[bold red][!] Unexpected error:[/bold red] {e}"
        )

if __name__ == "__main__":
    main()