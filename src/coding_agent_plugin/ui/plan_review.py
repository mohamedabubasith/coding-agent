"""Interactive plan review UI using Rich."""

from rich.table import Table
from rich.panel import Panel
from rich.prompt import Confirm
from typing import Dict, Any


def review_plan(workflow: Dict[str, Any], console) -> bool:
    """
    Display the plan and ask user for approval.
    
    Args:
        workflow: The generated plan with architecture and tasks
        console: Rich console instance
        
    Returns:
        bool: True if user approves, False otherwise
    """
    console.print("\n")
    console.print(Panel.fit(
        "[bold cyan]Generated Plan[/bold cyan]",
        border_style="cyan"
    ))
    
    # Display Architecture
    console.print("\n[bold]📁 Architecture:[/bold]\n")
    architecture = workflow.get("architecture", {})
    
    for component, files in architecture.items():
        console.print(f"  [cyan]{component}/[/cyan]")
        for file in files:
            console.print(f"    ├── {file}")
    
    # Display Tasks
    console.print("\n[bold]📋 Tasks:[/bold]\n")
    tasks = workflow.get("tasks", [])
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=3)
    table.add_column("Phase", style="cyan")
    table.add_column("Description")
    table.add_column("Agent", style="green")
    
    for task in tasks:
        table.add_row(
            str(task.get("id", "")),
            task.get("phase", ""),
            task.get("description", ""),
            task.get("agent", "")
        )
    
    console.print(table)
    
    # Estimate stats
    num_tasks = len(tasks)
    console.print(f"\n[dim]Total tasks: {num_tasks}[/dim]")
    console.print(f"[dim]Estimated time: ~{num_tasks * 10}s[/dim]\n")
    
    # Ask for approval
    return Confirm.ask("\n[bold]Do you want to proceed with this plan?[/bold]", default=True)
