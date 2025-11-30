"""
CLI entry point for coding-agent-plugin.
Provides a user-friendly command-line interface for project generation.
"""

import asyncio
import sys
import os
from pathlib import Path
from typing import Optional
import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint
from coding_agent_plugin.context.project_context import ProjectContext

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def app():
    """
    🚀 Coding Agent Plugin - Autonomous Project Generator
    
    An AI-powered tool that creates complete projects from natural language descriptions.
    """
    pass


@app.command()
@click.argument("prompt", required=False)
@click.option("--mode", "-m", 
              type=click.Choice(['direct', 'autonomous'], case_sensitive=False),
              default='autonomous',
              help="Creation mode: 'direct' for quick coding, 'autonomous' for full planning")
@click.option("--project", "-p", help="Target project name")
@click.option("--model", help="LLM model to use (overrides .env)")
@click.option("--provider", help="LLM provider (openai, nvidia, etc.)")
@click.option("--interactive", "-i", is_flag=True, help="Review plan before generation")
@click.option("--git", is_flag=True, default=True, help="Initialize git repository")
@click.option("--no-git", is_flag=True, help="Skip git initialization")
@click.option("--verbose", "-v", is_flag=True, help="Show detailed logs")
def create(prompt, mode, project, model, provider, interactive, git, no_git, verbose):
    """
    Create a new project from a natural language prompt.
    
    Modes:
        direct: Quick code generation without planning (for small tasks)
        autonomous: Full planning + generation (for complete projects)
    
    Examples:
        agentic-coder create "add login endpoint" --mode direct
        agentic-coder create "FastAPI backend" --mode autonomous
        agentic-coder create "React dashboard" --project my-app
    """
    # Handle no-git flag
    if no_git:
        git = False
    
    # If no prompt, enter interactive mode
    if not prompt:
        console.print("\n[bold cyan]🤖 Agentic Coder - Interactive Mode[/bold cyan]\n")
        prompt = click.prompt("What do you want to build?", type=str)
        
        if not interactive and mode == 'autonomous':
            interactive = click.confirm("Do you want to review the plan before generation?", default=True)
    
    # Display header
    mode_emoji = "🚀" if mode == 'direct' else "🤖"
    mode_name = "Direct Mode" if mode == 'direct' else "Autonomous Mode"
    
    console.print(Panel.fit(
        f"[bold green]{mode_emoji} {mode_name}[/bold green]\n\n"
        f"[cyan]Prompt:[/cyan] {prompt}\n"
        f"[cyan]Project:[/cyan] {project or 'current/default'}\n"
        f"[cyan]Model:[/cyan] {model or 'default (from .env)'}",
        title="[bold]Agentic Coder[/bold]",
        border_style="green"
    ))
    
    # Run async creation based on mode
    if mode == 'direct':
        asyncio.run(_direct_mode(
            prompt=prompt,
            project_name=project,
            model=model,
            verbose=verbose
        ))
    else:  # autonomous mode
        asyncio.run(_autonomous_mode(
            prompt=prompt,
            project_name=project,
            model=model,
            provider=provider,
            interactive=interactive,
            git=git,
            verbose=verbose
        ))



def _infer_filename(prompt: str) -> str:
    """
    Infer filename from prompt using simple heuristics.
    
    Examples:
        "add login endpoint" -> "auth.py"
        "create user model" -> "user.py"
        "fix database query" -> "database.py"
    """
    import re
    
    prompt_lower = prompt.lower()
    
    # Common patterns
    if "login" in prompt_lower or "auth" in prompt_lower:
        return "auth.py"
    elif "user" in prompt_lower:
        return "user.py"
    elif "model" in prompt_lower:
        return "models.py"
    elif "endpoint" in prompt_lower or "route" in prompt_lower or "api" in prompt_lower:
        return "routes.py"
    elif "database" in prompt_lower or "db" in prompt_lower:
        return "database.py"
    elif "config" in prompt_lower or "setting" in prompt_lower:
        return "config.py"
    elif "test" in prompt_lower:
        return "test.py"
    elif "util" in prompt_lower or "helper" in prompt_lower:
        return "utils.py"
    
    # Extract first meaningful word
    words = re.findall(r'\b[a-z]{3,}\b', prompt_lower)
    if words:
        # Skip common words
        skip_words = {'add', 'create', 'fix', 'update', 'delete', 'make', 'build', 'write'}
        for word in words:
            if word not in skip_words:
                return f"{word}.py"
    
    # Default
    return "main.py"


async def _direct_mode(
    prompt: str,
    project_name: str,
    model: str = None,
    verbose: bool = False
):
    """
    Direct mode: Quick code generation without planning.
    
    Args:
        prompt: User's coding request
        project_name: Target project
        model: Optional LLM model override
        verbose: Show detailed logs
    """
    from coding_agent_plugin.agents.coding import CodingAgent
    from coding_agent_plugin.managers import StorageManager, ProjectManager
    from coding_agent_plugin.utils.logger import logger
    
    console.print("[bold cyan]🚀 Direct Mode: Quick Coding[/bold cyan]\n")
    
    # Infer filename
    filename = _infer_filename(prompt)
    console.print(f"[cyan]Target file:[/cyan] {filename}\n")
    
    # Get or create project
    pm = ProjectManager()
    project = pm.get_project(project_name)
    if not project:
        raise ValueError(f"Project '{project_name}' not found. Create it first with 'agentic-coder project create {project_name}'")
    
    # Normalize to dict
    if hasattr(project, "to_dict"):
        project = project.to_dict()
    
    # Check existing content
    sm = StorageManager()
    existing_content = sm.get_file(project_name, filename)
    
    if existing_content:
        console.print(f"[yellow]ℹ️  File exists, will update it[/yellow]\n")
    
    # Generate code
    coding_agent = CodingAgent("coding")
    
    try:
        with console.status("[bold green]Generating code...", spinner="dots"):
            if model:
                import os
                os.environ["LLM_MODEL"] = model
            
            result = await coding_agent.execute({
                "file_path": filename,
                "user_prompt": prompt,
                "project_id": project_name,
                "existing_content": existing_content
            })
            
            logger.info(f"Code generated for {filename}")
        
        console.print(f"[green]✓[/green] Generated {filename}")
        
        # Success message
        console.print(Panel.fit(
            f"[bold green]✓ Code generated successfully![/bold green]\n\n"
            f"[cyan]File:[/cyan] {filename}\n"
            f"[cyan]Project:[/cyan] {project_name}\n"
            f"[cyan]Location:[/cyan] {project['storage_path']}",
            title="[bold]Direct Mode Complete[/bold]",
            border_style="green"
        ))
        
    except Exception as e:
        console.print(f"[red]❌ Code generation failed: {e}[/red]")
        if verbose:
            logger.exception("Direct mode failed")
        raise


async def _autonomous_mode(
    prompt: str,
    project_name: str,
    model: str = None,
    provider: str = None,
    interactive: bool = False,
    git: bool = True,
    verbose: bool = False
):
    """
    Autonomous mode: Full planning + generation.
    
    This is the original behavior with full orchestration.
    """
    from coding_agent_plugin.agents.orchestrator import OrchestratorAgent
    from coding_agent_plugin.ui.plan_review import review_plan
    from coding_agent_plugin.integrations.git_manager import GitManager
    from coding_agent_plugin.utils.logger import logger, get_project_logger
    from coding_agent_plugin.utils.validation import validate_prompt, sanitize_project_id, ValidationError
    from coding_agent_plugin.core.config import validate_llm_config
    from coding_agent_plugin.managers import ProjectManager
    
    try:
        # Validate LLM configuration
        try:
            validate_llm_config()
        except ValueError as e:
            console.print(f"[red]❌ Configuration Error:[/red]\n{e}")
            return
        
        # Validate inputs
        try:
            prompt = validate_prompt(prompt)
        except ValidationError as e:
            console.print(f"[red]❌ Invalid prompt: {e}[/red]")
            return
        
        # Get or create project
        pm = ProjectManager()
        
        if not project_name:
            # 1. Try to get current project
            current_project = pm.get_current_project()
            if current_project:
                project_name = current_project
                console.print(f"[cyan]Using active project: {project_name}[/cyan]")
            else:
                # 2. Generate project name from prompt
                import re
                safe_name = re.sub(r'[^a-zA-Z0-9]', '_', prompt[:40]).lower().strip('_')
                project_name = f"project_{safe_name}"
                console.print(f"[yellow]No active project. Generated new: {project_name}[/yellow]")
        
        # Check if project exists, otherwise create it
        project = pm.get_project(project_name)
        if not project:
            console.print(f"[green]Creating new project '{project_name}'...[/green]")
            try:
                project = pm.create_project(project_name, prompt)
            except Exception as e:
                console.print(f"[red]❌ Failed to create project: {e}[/red]")
                return
        
        # Normalize to dict
        if hasattr(project, "to_dict"):
            project = project.to_dict()
            
        project_id = project['id']
        logger.info(f"Using project: {project_id}")
        
        # Set model and provider if provided
        if model:
            os.environ["LLM_MODEL"] = model
            logger.info(f"Using model: {model}")
        if provider:
            os.environ["LLM_BASE_URL"] = provider
            logger.info(f"Using provider: {provider}")
        
        try:
            orchestrator = OrchestratorAgent()
        except Exception as e:
            console.print(f"[red]❌ Failed to initialize orchestrator: {e}[/red]")
            if verbose:
                logger.exception("Orchestrator initialization failed")
            return
        
        # Phase 1: Planning
        try:
            with console.status("[bold green]Planning project...", spinner="dots"):
                planning_agent = orchestrator.agents["planning"]
                plan_result = await planning_agent.execute({
                    "user_prompt": prompt,
                    "project_id": project_id
                })
                workflow = plan_result["workflow"]
                logger.info(f"Planning completed: {len(workflow.get('tasks', []))} tasks")
        except Exception as e:
            console.print(f"[red]❌ Planning failed: {e}[/red]")
            if verbose:
                logger.exception("Planning phase failed")
            return
        
        # Interactive plan review
        if interactive:
            try:
                approved = review_plan(workflow, console)
                if not approved:
                    console.print("[yellow]❌ Project creation cancelled.[/yellow]")
                    logger.info("Project creation cancelled by user")
                    return
            except Exception as e:
                console.print(f"[yellow]⚠️  Plan review failed: {e}. Continuing anyway...[/yellow]")
                logger.warning(f"Plan review failed: {e}")
        
        # Phase 2: Execution with error handling
        console.print("\n[bold green]🚀 Generating project...[/bold green]\n")
        
        try:
            result = await orchestrator.run_project(prompt, project_id)
            logger.info(f"Project execution completed: {result.get('status')}")
        except Exception as e:
            console.print(f"[red]❌ Project execution failed: {e}[/red]")
            if verbose:
                logger.exception("Project execution failed")
            return
        
        # Phase 3: Git initialization (optional)
        if git:
            try:
                # Use dictionary access for project dict
                git_mgr = GitManager(project['storage_path'])
                if git_mgr.init_repo():
                    git_mgr.commit("Initial commit: project generated by agentic-coder")
                    console.print("\n[green]✓[/green] Git repository initialized")
                    logger.info("Git repository initialized")
            except Exception as e:
                console.print(f"\n[yellow]⚠️  Git initialization failed: {e}[/yellow]")
                logger.warning(f"Git initialization failed: {e}")
                # Continue despite git failure
        
        # Success message
        console.print(Panel.fit(
            f"[bold green]✓ Project created successfully![/bold green]\n\n"
            f"[cyan]Project:[/cyan] {project_name}\n"
            f"[cyan]Location:[/cyan] {project['storage_path']}\n"
            f"[cyan]Files:[/cyan] {len(result.get('results', []))} tasks completed",
            title="[bold]Success[/bold]",
            border_style="green"
        ))
        
        logger.info(f"Project {project_id} completed successfully")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]❌ Operation cancelled by user[/yellow]")
        logger.info("Operation cancelled by user")
    except Exception as e:
        console.print(f"\n[bold red]❌ Unexpected error:[/bold red] {e}")
        logger.exception("Unexpected error in project creation")
        if verbose:
            import traceback
            console.print(traceback.format_exc())





@app.command()
@click.argument("request", required=False)
@click.option("--file", "-f", help="Target specific file to modify")
@click.option("--interactive", "-i", is_flag=True, help="Start interactive improvement session")
@click.option("--dry-run", is_flag=True, help="Show what will change without applying")
def improve(request, file, interactive, dry_run):
    """
    Improve an existing project with natural language requests.
    
    Examples:
        coding-agent improve "add type hints to all functions"
        coding-agent improve --file auth.py "add docstrings"
        coding-agent improve --interactive
    """
    from coding_agent_plugin.context.project_context import ProjectContext
    from coding_agent_plugin.agents.file_modifier import FileModifierAgent
    import re
    
    # Load project context from current directory
    context = ProjectContext(os.getcwd())
    
    if not context.is_valid_project():
        console.print("[red]❌ Not a coding-agent project![/red]")
        console.print("[yellow]Tip: Navigate to a project created with coding-agent[/yellow]")
        return
    
    # Load project
    with console.status("[bold green]Loading project...", spinner="dots"):
        if not context.load_project():
            console.print("[red]Failed to load project[/red]")
            return
    
    # Show project summary
    console.print(Panel.fit(
        context.get_project_summary(),
        title="[bold cyan]Project Loaded[/bold cyan]",
        border_style="cyan"
    ))
    
    # Get request if not provided
    if not request and not interactive:
        request = click.prompt("\n🤖 What would you like to improve?", type=str)
    
    # Interactive mode
    if interactive:
        console.print("\n[bold cyan]🤖 Interactive Improvement Mode[/bold cyan]")
        console.print("[dim]Type 'exit' or 'quit' to end session[/dim]\n")
        
        while True:
            request = click.prompt("What would you like to improve?", type=str)
            
            if request.lower() in ['exit', 'quit', 'q']:
                console.print("[yellow]Ending session...[/yellow]")
                break
            
            _process_improvement(request, context, file, dry_run)
            console.print()
    else:
        _process_improvement(request, context, file, dry_run)


def _process_improvement(request: str, context: ProjectContext, target_file: str = None, dry_run: bool = False):
    """Process a single improvement request."""
    from coding_agent_plugin.agents.file_modifier import FileModifierAgent
    from coding_agent_plugin.integrations.git_manager import GitManager
    
    console.print(f"\n[bold]Processing:[/bold] {request}\n")
    
    # Determine which files to modify
    if target_file:
        files_to_modify = [target_file] if target_file in context.files else []
        if not files_to_modify:
            console.print(f"[red]File not found: {target_file}[/red]")
            return
    else:
        # Auto-detect files (for now, let's modify main files)
        files_to_modify = context.get_main_files()
        if not files_to_modify:
            # Fallback to Python files
            files_to_modify = context.get_files_by_extension(".py")[:3]  # Limit to 3 files
    
    if not files_to_modify:
        console.print("[yellow]No files found to modify[/yellow]")
        return
    
    console.print(f"[cyan]Will modify:[/cyan] {', '.join(files_to_modify)}\n")
    
    if dry_run:
        console.print("[yellow]Dry run - no changes will be applied[/yellow]")
        return
    
    # Modify each file
    modifier = FileModifierAgent("file_modifier")
    changes = []
    
    for file_path in files_to_modify:
        try:
            with console.status(f"[bold green]Modifying {file_path}...", spinner="dots"):
                result = asyncio.run(modifier.execute({
                    "instruction": request,
                    "file_path": file_path,
                    "project_id": os.path.basename(os.getcwd()),
                    "existing_content": context.get_file_content(file_path)
                }))
            
            console.print(f"[green]✓[/green] Modified {file_path}")
            changes.append({
                "file": file_path,
                "instruction": request
            })
            
        except Exception as e:
            console.print(f"[red]✗[/red] Failed to modify {file_path}: {e}")
    
    if changes:
        # Save to conversation history
        context.save_conversation_history(request, changes)
        
        # Git commit
        git_mgr = GitManager(os.getcwd())
        if git_mgr.repo:
            git_mgr.commit(f"improve: {request}")
            console.print(f"\n[green]✓[/green] Changes committed to git")
        
        console.print(f"\n[bold green]✓ Done![/bold green] Modified {len(changes)} file(s)")


@app.command()
def init():
    """Initialize agentic-coder environment."""
    from coding_agent_plugin.managers import ProjectManager
    
    try:
        pm = ProjectManager()
        console.print(Panel.fit(
            f"[bold green]✓ Environment initialized![/bold green]\n\n"
            f"[cyan]Database:[/cyan] {pm.db_path}\n"
            f"[cyan]Projects:[/cyan] {pm.projects_dir}",
            title="[bold]Initialization[/bold]",
            border_style="green"
        ))
    except Exception as e:
        console.print(f"[red]❌ Initialization failed: {e}[/red]")


@app.command()
def templates():
    """List available project templates."""
    console.print("[cyan]📋 Available Templates:[/cyan]\n")
    
    templates_list = [
        ("nextjs-auth", "Next.js with authentication"),
        ("fastapi-crud", "FastAPI with CRUD operations"),
        ("react-dashboard", "React admin dashboard"),
        ("django-rest", "Django REST API"),
        ("express-graphql", "Express + GraphQL"),
    ]
    
    from rich.table import Table
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Template", style="green")
    table.add_column("Description")
    
    for name, desc in templates_list:
        table.add_row(name, desc)
    
    console.print(table)
    console.print("\n[dim]Use: agentic-coder create --template <name>[/dim]")


@app.group()
def project():
    """Manage projects (create, list, switch, delete, run)."""
    pass


@project.command("run")
@click.argument("prompt")
@click.option("--mode", type=click.Choice(["autonomous", "direct"]), default="autonomous", help="Execution mode")
@click.option("--interactive", "-i", is_flag=True, help="Interactive plan review")
@click.option("--git/--no-git", default=True, help="Initialize/Commit to git")
@click.option("--verbose", "-v", is_flag=True, help="Verbose logging")
def project_run(prompt, mode, interactive, git, verbose):
    """Run the agent on the current project."""
    import asyncio
    from coding_agent_plugin.managers import ProjectManager
    
    pm = ProjectManager()
    current_project = pm.get_current_project()
    
    if not current_project:
        console.print("[red]❌ No active project selected.[/red]")
        console.print("[yellow]Use 'agentic-coder project switch <name>' or 'agentic-coder project create <name>' first.[/yellow]")
        return
        
    if mode == "autonomous":
        asyncio.run(_autonomous_mode(
            prompt=prompt,
            project_name=current_project,
            interactive=interactive,
            git=git,
            verbose=verbose
        ))
    else:
        asyncio.run(_direct_mode(
            prompt=prompt,
            project_name=current_project,
            verbose=verbose
        ))


@project.command("create")
@click.argument("name")
@click.option("--description", "-d", help="Project description")
def project_create(name, description):
    """Create a new project."""
    from coding_agent_plugin.managers import ProjectManager
    
    try:
        pm = ProjectManager()
        proj = pm.create_project(name, description)
        
        desc_line = f"[cyan]Description:[/cyan] {proj['description']}" if proj.get('description') else ''
        
        console.print(Panel.fit(
            f"[bold green]✓ Project created successfully![/bold green]\n\n"
            f"[cyan]Name:[/cyan] {proj['name']}\n"
            f"[cyan]ID:[/cyan] {proj['id']}\n"
            f"[cyan]Location:[/cyan] {proj['storage_path']}\n"
            f"{desc_line}",
            title="[bold]New Project[/bold]",
            border_style="green"
        ))
        
        # Set as current project
        pm.set_current_project(name)
        console.print(f"\n[dim]✓ Set as current project[/dim]")
        
    except ValueError as e:
        console.print(f"[red]❌ Error: {e}[/red]")
    except Exception as e:
        console.print(f"[red]❌ Failed to create project: {e}[/red]")


@project.command("list")
def project_list():
    """List all projects."""
    from coding_agent_plugin.managers import ProjectManager
    from rich.table import Table
    
    pm = ProjectManager()
    projects = pm.list_projects()
    
    if not projects:
        console.print("[yellow]No projects found. Create one with 'agentic-coder project create <name>'[/yellow]")
        return
    
    current = pm.get_current_project()
    
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("#", style="dim")
    table.add_column("Name", style="green")
    table.add_column("Description")
    table.add_column("Created", style="dim")
    table.add_column("Status")
    
    for idx, proj in enumerate(projects, 1):
        is_current = "⭐ Active" if proj["name"] == current else ""
        created = proj["created_at"][:10] if proj["created_at"] else "N/A"
        desc = proj["description"] or "[dim]No description[/dim]"
        
        table.add_row(
            str(idx),
            proj["name"],
            desc,
            created,
            is_current
        )
    
    console.print(table)
    console.print(f"\n[dim]Total: {len(projects)} project(s)[/dim]")


@project.command("switch")
@click.argument("name")
def project_switch(name):
    """Switch to a different project."""
    from coding_agent_plugin.managers import ProjectManager
    
    pm = ProjectManager()
    
    if pm.set_current_project(name):
        console.print(f"[green]✓ Switched to project '[bold]{name}[/bold]'[/green]")
    else:
        console.print(f"[red]❌ Project '{name}' not found[/red]")


@project.command("delete")
@click.argument("name")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation")
def project_delete(name, yes):
    """Delete a project and all its files."""
    from coding_agent_plugin.managers import ProjectManager
    
    if not yes:
        confirm = click.confirm(
            f"Are you sure you want to delete project '{name}' and all its files?",
            default=False
        )
        if not confirm:
            console.print("[yellow]Cancelled[/yellow]")
            return
    
    pm = ProjectManager()
    
    if pm.delete_project(name):
        console.print(f"[green]✓ Project '{name}' deleted successfully[/green]")
    else:
        console.print(f"[red]❌ Project '{name}' not found[/red]")


@project.command("info")
@click.argument("name", required=False)
def project_info(name):
    """Show detailed project information."""
    from coding_agent_plugin.managers import ProjectManager
    
    pm = ProjectManager()
    
    # If no name provided, use current project
    if not name:
        name = pm.get_current_project()
        if not name:
            console.print("[red]❌ No current project set. Specify a project name or switch to one.[/red]")
            return
    
    stats = pm.get_project_stats(name)
    
    if not stats:
        console.print(f"[red]❌ Project '{name}' not found[/red]")
        return
    
    console.print(Panel.fit(
        f"[bold cyan]Project Information[/bold cyan]\n\n"
        f"[cyan]Name:[/cyan] {stats['name']}\n"
        f"[cyan]ID:[/cyan] {stats['id']}\n"
        f"[cyan]Description:[/cyan] {stats['description'] or 'N/A'}\n"
        f"[cyan]Location:[/cyan] {stats['storage_path']}\n"
        f"[cyan]Files:[/cyan] {stats['file_count']}\n"
        f"[cyan]Size:[/cyan] {stats['total_size_mb']} MB\n"
        f"[cyan]Created:[/cyan] {stats['created_at'][:19] if stats['created_at'] else 'N/A'}\n"
        f"[cyan]Updated:[/cyan] {stats['updated_at'][:19] if stats['updated_at'] else 'N/A'}",
        title=f"[bold]{stats['name']}[/bold]",
        border_style="cyan"
    ))


@app.command()
def init():
    """Initialize agentic-coder (first-time setup)."""
    from coding_agent_plugin.models import init_db
    from coding_agent_plugin.models.database import AGENTIC_HOME
    from coding_agent_plugin.core.config import validate_db_config
    
    console.print("\n[bold cyan]🚀 Initializing Agentic Coder...[/bold cyan]\n")
    
    try:
        validate_db_config()
    except ValueError as e:
        console.print(f"[red]❌ Configuration Error:[/red]\n{e}")
        return
    
    # Create home directory
    AGENTIC_HOME.mkdir(parents=True, exist_ok=True)
    console.print(f"[green]✓[/green] Created home directory: {AGENTIC_HOME}")
    
    # Initialize database
    init_db()
    console.print(f"[green]✓[/green] Initialized database")
    
    # Create projects directory
    (AGENTIC_HOME / "projects").mkdir(exist_ok=True)
    console.print(f"[green]✓[/green] Created projects directory")
    
    console.print(Panel.fit(
        "[bold green]✓ Initialization complete![/bold green]\n\n"
        "[cyan]Next steps:[/cyan]\n"
        "1. Create a project: [bold]agentic-coder project create <name>[/bold]\n"
        "2. Generate code: [bold]agentic-coder create \"description\"[/bold]\n"
        "3. List projects: [bold]agentic-coder project list[/bold]",
        title="[bold]Ready to Go![/bold]",
        border_style="green"
    ))


if __name__ == "__main__":
    app()
