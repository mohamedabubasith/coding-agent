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
        "validation": {
            "extensions": [".py"],
            "min_files": 1
        }
    },
    {
        "name": "FastAPI CRUD",
        "category": "Backend",
        "difficulty": "Medium",
        "prompt": "Create a FastAPI application with a 'Book' model (title, author, year). Implement Create, Read, Update, Delete endpoints. Use SQLite.",
        "validation": {
            "extensions": [".py", ".txt"],
            "min_files": 3
        }
    },
    {
        "name": "React Counter",
        "category": "Frontend",
        "difficulty": "Medium",
        "prompt": "Create a React component 'Counter.js' that has increment/decrement buttons and displays the count. Add a 'Reset' button too.",
        "validation": {
            "extensions": [".js", ".jsx", ".tsx"],
            "min_files": 1
        }
    },
    {
        "name": "Data Processing",
        "category": "Data Engineering",
        "difficulty": "Hard",
        "prompt": "Create a script that generates a dummy CSV file with 1000 rows of sales data (date, product, amount), then reads it using pandas to calculate total sales per product.",
        "validation": {
            "extensions": [".py"],
            "min_files": 2
        }
    },
    {
        "name": "Node Express Server",
        "category": "Backend",
        "difficulty": "Medium",
        "prompt": "Create a simple Node.js Express server with a single GET /health endpoint that returns {'status': 'ok'}.",
        "validation": {
            "extensions": [".js", ".json"],
            "min_files": 2
        }
    },
    {
        "name": "C Hello World",
        "category": "Systems",
        "difficulty": "Easy",
        "prompt": "Create a C program 'hello.c' that prints 'Hello from C' to stdout.",
        "validation": {
            "extensions": [".c"],
            "min_files": 1
        }
    },
    {
        "name": "C++ Class",
        "category": "Systems",
        "difficulty": "Medium",
        "prompt": "Create a C++ program 'person.cpp' with a Person class. It should have a method to print the person's name. Instantiate it and print 'Hello User'.",
        "validation": {
            "extensions": [".cpp"],
            "min_files": 1
        }
    },
    {
        "name": "Go Server",
        "category": "Backend",
        "difficulty": "Medium",
        "prompt": "Create a simple Go web server 'main.go' that listens on port 8080 and returns 'Hello from Go' on the root path.",
        "validation": {
            "extensions": [".go"],
            "min_files": 1
        }
    },
    {
        "name": "Rust Script",
        "category": "Systems",
        "difficulty": "Easy",
        "prompt": "Create a Rust program 'main.rs' that prints 'Hello from Rust' to stdout.",
        "validation": {
            "extensions": [".rs"],
            "min_files": 1
        }
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
            
            # Also need to handle if project already exists (cleanup from previous run)
            existing = pm.get_project(case['name'])
            if existing:
                pm.delete_project(existing['id'])
                
            project_data = pm.create_project(name=case['name'], description=f"Benchmark: {case['name']}")
            project_id = project_data['id']
            
            # Run Project
            result = await orchestrator.run_project(case['prompt'], project_id)
            
            # Verify
            project = pm.get_project(project_id)
            if project:
                files = pm.list_files(project_id)
                files_created = files
                
                # Validation Logic
                validation = case.get("validation", {})
                required_extensions = validation.get("extensions", [])
                min_files = validation.get("min_files", 0)
                
                # Check 1: Min files
                if len(files) < min_files:
                    status = "PARTIAL"
                    error = f"Expected at least {min_files} files, got {len(files)}"
                else:
                    # Check 2: Extensions
                    found_extensions = {os.path.splitext(f)[1] for f in files}
                    missing_extensions = [ext for ext in required_extensions if ext not in found_extensions]
                    
                    if missing_extensions:
                        status = "PARTIAL"
                        error = f"Missing file types: {missing_extensions}"
                    else:
                        status = "PASSED"

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
