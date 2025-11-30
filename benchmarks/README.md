# Agentic Coder Benchmark Suite

This directory contains tools to evaluate the performance and capabilities of the Agentic Coder plugin.

## 🚀 Running the Benchmark

To run the standard benchmark suite, which tests the agents across different categories (Scripting, Backend, Frontend, Data), run:

```bash
# Ensure you have your API key set
export OPENAI_API_KEY=sk-your-key-here

# Run the benchmark script
python benchmarks/run_benchmark.py
```

## 📊 What it Tests

The suite runs 4 standardized scenarios:

1.  **Basic Python Script**: Tests simple logic and file I/O.
2.  **FastAPI CRUD**: Tests backend web development, database models, and API structure.
3.  **React Counter**: Tests frontend component generation and state management.
4.  **Data Processing**: Tests data engineering tasks with pandas.

## 📈 Reports

Results are saved in `benchmarks/results/<timestamp>/BENCHMARK_REPORT.md`.
The report includes:
- Pass/Fail status for each case
- Execution time
- Number of files created
- Error details (if any)

## 🏆 Rating Your Model

You can use this suite to compare different LLMs (e.g., GPT-4 vs GPT-3.5 vs Claude).
1. Set `LLM_MODEL=gpt-4o` in `.env` and run the benchmark.
2. Set `LLM_MODEL=gpt-3.5-turbo` and run again.
3. Compare the "Overall Score" and execution times in the generated reports.
