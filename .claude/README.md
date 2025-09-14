# .claude Directory Structure

This directory contains Claude Code agents, commands, and analysis tools for the Autonomous Agents research repository.

## Directory Structure

### `/agents/`
Custom agent configurations for specialized tasks:
- `analyst-agent.md` - Meta-agent for coordinating research analysis
- `developer-agent.md` - Analyzes GitHub repositories for code quality
- `parallel-orchestrator.md` - Manages parallel execution of multiple agents
- `research-paper-agent.md` - Extracts information from research papers

### `/analysis/`
Research analysis outputs and datasets:
- `criteria.json` - Evaluation criteria for research papers
- `fabric-criteria.json` - Enhanced criteria for fabric dataset
- `CHOSEN_PAPERS_REPORT.md` - Report on selected papers
- `DATASET_REPORT.md` - Final dataset report
- `/papers/` - Individual paper analysis results (JSON files)
- `/results/` - Batch processing results

### `/commands/`
Custom Claude Code commands:
- `build-dataset.md` - Command for building research datasets

### `/scripts/`
Utility scripts for processing:
- `/batch-processing/` - Batch processing scripts for parallel analysis
  - `batch-coordinator.py` - Main coordinator for batch processing
  - `batch_processor.py` - Parallel batch processor
  - `dataset-builder.py` - Dataset construction script
  - `enhanced_analyzer.py` - Enhanced analysis for high-value systems
  - `final_aggregator.py` - Aggregates batch results
  - `run-parallel-batch.sh` - Shell script for running parallel batches

### `settings.local.json`
Local settings configuration file

## Usage

The agents and commands in this directory are designed to work with Claude Code for analyzing autonomous agent research papers and building datasets for multi-agent systems research.

## Workflow

1. Research papers are analyzed using the research-paper-agent
2. Developer-agent evaluates associated code repositories
3. Analyst-agent coordinates and assesses relevance
4. Results are aggregated into comprehensive reports
5. Batch processing scripts handle large-scale analysis

## Note

This structure has been cleaned and organized for clarity. Temporary test files have been removed and batch processing scripts have been consolidated into a dedicated subdirectory.