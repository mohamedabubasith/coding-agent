"""
CLI entry point for coding-agent-plugin.
Provides a user-friendly command-line interface for project generation.
"""

import click
import asyncio
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich import print as rprint

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
@click.option("--model", "-m", help="LLM model to use (overrides .env)")
@click.option("--provider", "-p", help="LLM provider (openai, nvidia, etc.)")
@click.option("--interactive", "-i", is_flag=True, help="Review plan before generation")
@click.option("--git", is_flag=True, default=True, help="Initialize git repository")
@click.option("--no-git", is_flag=True, help="Skip git initialization")
@click.option("--verbose", "-v", is_flag=True, help="Show detailed logs")
def create(prompt, model, provider, interactive, git, no_git, verbose):
    """
    Create a new project from a natural language prompt.
    
    Examples:
        coding-agent create "FastAPI login backend"
        coding-agent create "React Todo App" --interactive
    """
    # Handle no-git flag
    if no_git:
        git = False
    
    # If no prompt, enter interactive mode
    if not prompt:
        console.print("\n[bold cyan]🤖 Coding Agent - Interactive Mode[/bold cyan]\n")
        prompt = click.prompt("What do you want to build?", type=str)
        
        if not interactive:
            interactive = click.confirm("Do you want to review the plan before generation?", default=True)
    
    # Display header
    console.print(Panel.fit(
        f"[bold green]Creating Project[/bold green]\n\n"
        f"[cyan]Prompt:[/cyan] {prompt}\n"
        f"[cyan]Model:[/cyan] {model or 'default (from .env)'}\n"
        f"[cyan]Interactive:[/cyan] {interactive}",
        title="[bold]Coding Agent[/bold]",
        border_style="green"
    ))
    
    # Run async creation
    asyncio.run(_create_project(
        prompt=prompt,
        model=model,
        provider=provider,
        interactive=interactive,
        git=git,
        verbose=verbose
    ))


async def _create_project(prompt: str, model: str = None, provider: str = None, 
                          interactive: bool = False, git: bool = True, verbose: bool = False):
    """Internal async function to create project."""
    from coding_agent_plugin.agents.orchestrator import OrchestratorAgent
    from coding_agent_plugin.ui.plan_review import review_plan
    from coding_agent_plugin.integrations.git_manager import GitManager
    from coding_agent_plugin.utils.logger import logger, get_project_logger
    from coding_agent_plugin.utils.validation import validate_prompt, sanitize_project_id, ValidationError
    from coding_agent_plugin.core.config import validate_llm_config
    
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
        
        # Generate project ID from prompt
        project_id = sanitize_project_id(prompt)
        logger.info(f"Creating project: {project_id}")
        
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
                git_mgr = GitManager(f"projects/{project_id}")
                if git_mgr.init_repo():
                    git_mgr.commit("Initial commit: project generated by coding-agent")
                    console.print("\n[green]✓[/green] Git repository initialized")
                    logger.info("Git repository initialized")
            except Exception as e:
                console.print(f"\n[yellow]⚠️  Git initialization failed: {e}[/yellow]")
                logger.warning(f"Git initialization failed: {e}")
                # Continue despite git failure
        
        # Success message
        console.print(Panel.fit(
            f"[bold green]✓ Project created successfully![/bold green]\n\n"
            f"[cyan]Location:[/cyan] projects/{project_id}\n"
            f"[cyan]Files:[/cyan] {len(result.get('results', []))} tasks completed",
            title="[bold]Success[/bold]",
            border_style="green"
        ))
        
        logger.info(f"Project {project_id} created successfully")
        
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
    """Initialize a new project interactively with questions."""
    console.print("[cyan]🚀 Initializing new project...[/cyan]")
    
    # Coming soon
    console.print("[yellow]This feature is coming soon![/yellow]")


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
    console.print("\n[dim]Use: coding-agent create --template <name>[/dim]")


if __name__ == "__main__":
    app()
