import os
import rich_click as click
from rich.console import Console
from rich.table import Table
from . import scanner
from . import matcher
from . import manager
from . import cleaner
from . import syncer
import yaml
@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def cli():
    """
    envpilot: A unified Python environment manager and synchronizer.
    
    This tool helps you discover, create, manage, and synchronize Python virtual environments
    to promote reuse and save disk space.
    """
    pass

@cli.command("list")
def list_envs():
    """Scans the system for Python environments and displays them in a table."""
    console = Console()
    
    # In the future, this could be configurable. For now, scan home directory.
    search_path = os.path.expanduser("~")
    
    with console.status(f"[bold green]Scanning for environments in {search_path}...") as status:
        environments = scanner.discover_environments(search_path)

    if not environments:
        console.print("No Python environments found.", style="bold yellow")
        return

    table = Table(
        title="Discovered Python Environments",
        caption=f"Found {len(environments)} environments",
        show_header=True,
        header_style="bold magenta"
    )
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Python Version", style="green")
    table.add_column("Packages", justify="right", style="yellow")
    table.add_column("Size (MB)", justify="right", style="red")
    table.add_column("Path", style="blue", overflow="fold")
    
    # Sort environments by path for consistent ordering
    environments.sort(key=lambda x: x['path'])

    for env in environments:
        table.add_row(
            env["name"],
            env["python_version"],
            str(env["package_count"]),
            f"{env['size_mb']:.2f}",
            env["path"]
        )
    
    console.print(table)

@cli.command("match")
@click.argument("requirements_file", type=click.Path(exists=True, dir_okay=False))
@click.option("--env", "env_name", help="Name of a specific environment to match against.")
def match_reqs(requirements_file, env_name):
    """
    Finds the best-matching virtual environment for a given requirements file.
    
    Ranks all discovered environments by how well they match the packages
    listed in the REQUIREMENTS_FILE.
    """
    console = Console()

    with console.status(f"[bold green]Scanning and matching for {os.path.basename(requirements_file)}...") as status:
        matches, error = matcher.find_best_matches(requirements_file, env_name)

    if error:
        console.print(f"Error: {error}", style="bold red")
        return

    if not matches:
        console.print("No suitable Python environments found to match against.", style="bold yellow")
        return

    table = Table(
        title=f"Environment match results for {os.path.basename(requirements_file)}",
        show_header=True,
        header_style="bold magenta"
    )
    table.add_column("Rank", style="bold white", justify="center")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Match %", justify="right", style="green")
    table.add_column("Extra Pkgs", justify="right", style="yellow")
    table.add_column("Missing", justify="left", style="red")
    table.add_column("Path", style="blue", overflow="fold")

    for i, match in enumerate(matches):
        env = match["env"]
        missing_str = ", ".join(match['missing_packages'])
        if not missing_str:
            missing_str = "None"
        
        table.add_row(
            f"#{i+1}",
            env["name"],
            f"{match['match_percentage']:.2f}%",
            str(match['extra_packages_count']),
            missing_str,
            env["path"]
        )
    
    console.print(table)
    console.print("\n💡 Tip: Reuse a high-ranking environment to save time and disk space.", style="italic dim")

@cli.command("create")
@click.argument("name", default="venv", required=False)
@click.option("--requirements", "-r", "requirements_file", type=click.Path(exists=True, dir_okay=False), help="Path to a requirements.txt file to install packages from.")
@click.option("--path", "-p", "creation_path", type=click.Path(file_okay=False, writable=True), help="The directory where the environment will be created. Defaults to the current directory.")
@click.option("--template", "-t", "template_name", help="Name of the environment template (YAML) to use.")
def create_env(name, requirements_file, creation_path, template_name):
    """
    Creates a new Python virtual environment.
    """
    console = Console()

    dependencies = None
    if template_name:
        template_path = os.path.join("templates", f"{template_name}.yml")
        if not os.path.exists(template_path):
            console.print(f"[bold red]Template '{template_name}' not found in templates/ directory.[/bold red]")
            return
        with open(template_path, "r") as f:
            try:
                config = yaml.safe_load(f)
                dependencies = config.get("dependencies", [])
            except Exception as e:
                console.print(f"[bold red]Failed to load template: {e}[/bold red]")
                return

    with console.status(f"[bold green]Creating environment '{name}'...") as status:
        env_path, error = manager.create_environment(
        name,
        requirements_path=requirements_file,  # <-- FIXED!
        base_path=creation_path,
        dependencies=dependencies  # Pass dependencies to manager
        )
        if error:
            if env_path:
                console.print(f"⚠️  Environment '{name}' created at {env_path} but with an error:", style="bold yellow")
                console.print(error, style="yellow")
            else:
                console.print(f"Error: {error}", style="bold red")
            return

    console.print(f"✅ Environment '{name}' created successfully at {env_path}", style="bold green")
    if dependencies:
        console.print(f"📦 Installed template dependencies: [cyan]{', '.join(dependencies)}[/cyan]")


@cli.command("list-templates")
def list_templates():
    """
    Lists available environment templates.
    """
    console = Console()
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    templates_dir = os.path.join(BASE_DIR, "templates")

    if not os.path.isdir(templates_dir):
        console.print("[bold red]No templates directory found.[/bold red]")
        return

    files = [f for f in os.listdir(templates_dir) if f.endswith(".yml")]
    if not files:
        console.print("[bold yellow]No templates found in the templates/ directory.[/bold yellow]")
        return

    table = Table(title="Available Environment Templates", show_header=True, header_style="bold magenta")
    table.add_column("Template Name", style="cyan")
    table.add_column("Description", style="green")

    for filename in files:
        path = os.path.join(templates_dir, filename)
        try:
            with open(path, "r") as f:
                config = yaml.safe_load(f)
                name = config.get("name", filename.replace(".yml", ""))
                desc = config.get("description", "-")
                table.add_row(name, desc)
        except Exception:
            table.add_row(filename.replace(".yml", ""), "[error reading file]")

    console.print(table)



@cli.command("activate")
@click.argument("name")
def activate_env(name):
    """
    Launches a new, activated sub-shell for the specified environment.
    
    Type 'exit' to leave the shell and return to your original session.
    """
    console = Console()
    error = manager.launch_shell(name)
    if error:
        console.print(f"Error: {error}", style="bold red")

@cli.command("clean")
@click.option("--yes", is_flag=True, help="Skip the confirmation prompt and remove environments directly.")
@click.option("--dry-run", is_flag=True, help="List environments that would be removed without actually deleting them.")
def clean_envs(dry_run, yes):
    """
    Scans for and removes orphaned environments to save disk space.
    
    An environment is considered 'orphaned' if it does not have a .project file
    linking it to a known project directory. This is a placeholder for a more
    robust check in the future.
    """
    console = Console()
    
    with console.status("[bold green]Scanning for all environments...") as status:
        all_environments = scanner.discover_environments(os.path.expanduser("~"))

    orphaned = cleaner.find_orphaned_environments(all_environments)

    if not orphaned:
        console.print("✨ No orphaned environments found. Your setup is clean!", style="bold green")
        return

    console.print("Found the following orphaned environments (no .project link):", style="bold yellow")
    
    table = Table(title="Orphaned Environments", show_header=True, header_style="bold magenta")
    table.add_column("Name", style="cyan")
    table.add_column("Size (MB)", justify="right", style="red")
    table.add_column("Path", style="blue")

    for env in orphaned:
        table.add_row(env["name"], f"{env['size_mb']:.2f}", env["path"])
    
    console.print(table)

    if dry_run:
        console.print("\nThis was a dry run. No environments were removed.", style="italic dim")
        return
    
    if yes or click.confirm("\nDo you want to remove these environments?"):
        removed, errors = cleaner.remove_environments(orphaned)
        if removed:
            console.print("\n✅ Successfully removed:", style="bold green")
            for path in removed:
                console.print(f"- {path}")
        if errors:
            console.print("\n❌ Errors occurred:", style="bold red")
            for error in errors:
                console.print(f"- {error}")

@click.group()
def sync():
    """Manages environment state through portable lock files."""
    pass

@sync.command("export")
@click.argument("env_name")
@click.option("--file", "-f", "output_file", default="envpilot-lock.json", help="The name for the output lock file.")
def sync_export(env_name, output_file):
    """Exports an environment's state to a lock file."""
    console = Console()
    
    with console.status(f"[bold green]Exporting environment '{env_name}'...") as status:
        path, error = syncer.export_environment(env_name, output_file)
    
    if error:
        console.print(f"Error: {error}", style="bold red")
        return
        
    console.print(f"✅ Environment '{env_name}' exported successfully to {path}", style="bold green")

@sync.command("import")
@click.argument("lock_file", type=click.Path(exists=True, dir_okay=False))
@click.argument("new_env_name")
def sync_import(lock_file, new_env_name):
    """Creates a new environment from a lock file."""
    console = Console()
    
    with console.status(f"[bold green]Importing environment from '{lock_file}'...") as status:
        path, error = syncer.import_environment(lock_file, new_env_name)
        
    if error:
        if path:
            console.print(f"⚠️  Environment '{new_env_name}' may be partially created at {path} but an error occurred:", style="bold yellow")
            console.print(error, style="yellow")
        else:
            console.print(f"Error: {error}", style="bold red")
        return
        
    console.print(f"✅ Environment '{new_env_name}' imported and created successfully at {path}", style="bold green")

cli.add_command(sync)

if __name__ == "__main__":
    cli() 