"""
Agentic Coder Benchmark Suite
=============================

This script runs a series of standardized coding challenges against the Agentic Coder
to evaluate its performance, stability, and capability.

Usage:
    export OPENAI_API_KEY=sk-...
    python benchmarks/run_benchmark.py

Scenarios:
1. Basic: Simple Python Script
2. Web: FastAPI CRUD Application
3. Frontend: React Component
4. Data: CSV Processing Script
"""

import asyncio
import time
import os
import shutil
import json
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn

# Adjust path to include src
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from coding_agent_plugin.agents.orchestrator import OrchestratorAgent
from coding_agent_plugin.managers import ProjectManager

console = Console()

BENCHMARK_CASES = [
    {
        "name": "Basic Python Script",
        "category": "Scripting",
        "difficulty": "Easy",
        "prompt": "Create a python script that calculates the Fibonacci sequence up to the 100th number and saves it to 'fib.txt'.",
        "expected_files": ["fib.py"]
    },
    {
        "name": "FastAPI CRUD",
        "category": "Backend",
        "difficulty": "Medium",
        "prompt": "Create a FastAPI application with a 'Book' model (title, author, year). Implement Create, Read, Update, Delete endpoints. Use SQLite.",
        "expected_files": ["main.py", "models.py", "requirements.txt"]
    },
    {
        "name": "React Counter",
        "category": "Frontend",
        "difficulty": "Medium",
        "prompt": "Create a React component 'Counter.js' that has increment/decrement buttons and displays the count. Add a 'Reset' button too.",
        "expected_files": ["Counter.js"]
    },
    {
        "name": "Data Processing",
        "category": "Data Engineering",
        "difficulty": "Hard",
        "prompt": "Create a script that generates a dummy CSV file with 1000 rows of sales data (date, product, amount), then reads it using pandas to calculate total sales per product.",
        "expected_files": ["generate_data.py", "analyze_data.py"]
    }
]

class BenchmarkRunner:
    def __init__(self):
        self.results = []
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = Path(f"benchmarks/results/{self.timestamp}")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def run_case(self, case: Dict[str, Any]) -> Dict[str, Any]:
        project_id = f"bench_{case['name'].lower().replace(' ', '_')}_{self.timestamp}"
        start_time = time.time()
        
        console.print(f"\n[bold blue]Running Case: {case['name']}[/bold blue]")
        console.print(f"Prompt: {case['prompt']}")
        
        status = "FAILED"
        error = None
        tasks_completed = 0
        files_created = []
        
        try:
            # Initialize Orchestrator
            orchestrator = OrchestratorAgent()
            
            # Create Project first
            pm = ProjectManager()
            # Note: create_project returns a dict, not an object, based on the code I saw
            # But wait, the docstring says "Returns Created Project object" but the code says "return project_dict"
            # Let's assume it returns a dict based on line 116: return project_dict
            
            # Also need to handle if project already exists (cleanup from previous run)
            existing = pm.get_project(case['name'])
            if existing:
                pm.delete_project(existing.id)
                
            project_data = pm.create_project(name=case['name'], description=f"Benchmark: {case['name']}")
            project_id = project_data['id']
            
            # Run Project
            result = await orchestrator.run_project(case['prompt'], project_id)
            
            # Verify
            project = pm.get_project(project_id)
            if project:
                files = pm.list_files(project_id)
                files_created = files
                
                # Check expected files
                missing = [f for f in case['expected_files'] if not any(f in created for created in files)]
                
                if not missing:
                    status = "PASSED"
                else:
                    status = "PARTIAL"
                    error = f"Missing files: {missing}"
            else:
                status = "FAILED"
                error = "Project not created"
                
        except Exception as e:
            status = "ERROR"
            error = str(e)
            console.print(f"[red]Error: {e}[/red]")
            
        duration = time.time() - start_time
        
        return {
            "name": case['name'],
            "category": case['category'],
            "difficulty": case['difficulty'],
            "status": status,
            "duration": round(duration, 2),
            "files_created": len(files_created),
            "error": error
        }

    async def run_all(self):
        console.print("[bold green]🚀 Starting Agentic Coder Benchmark Suite[/bold green]")
        console.print(f"Output Directory: {self.output_dir}\n")
        
        for case in BENCHMARK_CASES:
            result = await self.run_case(case)
            self.results.append(result)
            
            color = "green" if result["status"] == "PASSED" else "yellow" if result["status"] == "PARTIAL" else "red"
            console.print(f"Result: [{color}]{result['status']}[/{color}] in {result['duration']}s")
            if result["error"]:
                console.print(f"Details: {result['error']}")
                
        self.generate_report()

    def generate_report(self):
        report_path = self.output_dir / "BENCHMARK_REPORT.md"
        
        passed = len([r for r in self.results if r['status'] == 'PASSED'])
        total = len(self.results)
        score = (passed / total) * 100 if total > 0 else 0
        
        with open(report_path, "w") as f:
            f.write(f"# Agentic Coder Benchmark Report\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Overall Score:** {score:.1f}%\n\n")
            
            f.write("## Summary\n\n")
            f.write("| Case | Category | Difficulty | Status | Time (s) | Files |\n")
            f.write("|------|----------|------------|--------|----------|-------|\n")
            for r in self.results:
                status_icon = "✅" if r['status'] == 'PASSED' else "⚠️" if r['status'] == 'PARTIAL' else "❌"
                f.write(f"| {r['name']} | {r['category']} | {r['difficulty']} | {status_icon} {r['status']} | {r['duration']} | {r['files_created']} |\n")
            
            f.write("\n## Detailed Results\n\n")
            for r in self.results:
                f.write(f"### {r['name']}\n")
                f.write(f"- **Status:** {r['status']}\n")
                f.write(f"- **Time:** {r['duration']}s\n")
                if r['error']:
                    f.write(f"- **Issues:** {r['error']}\n")
                f.write("\n")
                
        console.print(f"\n[bold]Benchmark Complete![/bold]")
        console.print(f"Report saved to: {report_path}")
        
        # Also print table to console
        table = Table(title="Benchmark Results")
        table.add_column("Case", style="cyan")
        table.add_column("Status", style="magenta")
        table.add_column("Time", justify="right")
        
        for r in self.results:
            color = "green" if r['status'] == 'PASSED' else "red"
            table.add_row(r['name'], f"[{color}]{r['status']}[/{color}]", f"{r['duration']}s")
            
        console.print(table)

if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        console.print("[bold red]WARNING: OPENAI_API_KEY not set. Benchmarks will likely fail or use mocks if configured.[/bold red]")
        
    runner = BenchmarkRunner()
    asyncio.run(runner.run_all())
