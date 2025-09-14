# How to Start the Multi-Agent Analysis System

## Quick Start

To analyze research papers using the multi-agent system, you can use Claude Code with the analyst-agent to coordinate the workflow.

## Step 1: Single Paper Analysis

To analyze a single paper:

```bash
# Use the analyst-agent to analyze a specific paper
claude-code "Please use the analyst-agent to analyze the LightAgent paper from the README.md file"
```

## Step 2: Batch Analysis

To analyze multiple papers from a file:

```bash
# Analyze all papers in README.md
claude-code "Use the analyst-agent to analyze all papers in README.md that mention 'agent' and have potential GitHub repositories. Generate a batch report."
```

## Step 3: Generate Report

After analysis, request a formatted report:

```bash
# Generate the markdown report
claude-code "Generate a batch analysis report for all papers analyzed today, using the format specified in report-template.md"
```

## Example Commands

### Find Papers with GitHub URLs
```bash
claude-code "Search README.md for papers that mention GitHub repositories or claim to be open-source. List them in a table."
```

### Analyze Top 10 Papers
```bash
claude-code "Analyze the 10 most recent papers from README.md using the multi-agent system. Focus on sandbox compatibility."
```

### Review Excluded Papers
```bash
claude-code "Review all papers that were excluded due to hardware requirements. Can any run in simulation mode?"
```

## Workflow Overview

1. **Discovery Phase**
   - Analyst-agent searches for papers with implementation claims
   - Filters for multi-agent related papers
   - Identifies GitHub/GitLab URLs

2. **Analysis Phase**
   - Research-paper-agent extracts paper details
   - Developer-agent analyzes GitHub repositories
   - Scores calculated based on criteria.json

3. **Reporting Phase**
   - Results compiled into markdown tables
   - Decision telemetry calculated
   - Recommendations generated

## Output Files

Analysis results are saved to:
- `.claude/analysis/papers/[paper-id].json` - Individual analyses
- `.claude/analysis/reports/[date]-batch.md` - Batch reports
- `.claude/analysis/dataset/included.json` - Final dataset

## Monitoring Progress

Check analysis status:
```bash
# Count analyzed papers
ls -1 .claude/analysis/papers/*.json 2>/dev/null | wc -l

# View latest report
cat .claude/analysis/reports/latest.md
```

## Customization

### Adjust Criteria
Edit `.claude/analysis/criteria.json` to modify:
- Scoring weights
- Inclusion thresholds
- Exclusion criteria

### Focus Areas
Specify focus when starting analysis:
```bash
claude-code "Analyze papers focusing on security features and sandbox compatibility"
```

## Tips

1. **Start Small**: Test with 3-5 papers first
2. **Review Borderline**: Papers scoring 5.0-6.0 may need manual review
3. **Check Logs**: Review excluded papers for patterns
4. **Iterate**: Adjust criteria based on initial results

## Troubleshooting

### No GitHub URL Found
- Check if paper mentions "code available upon request"
- Search author names for personal GitHub
- Check paper website for repository links

### Repository Private/Deleted
- Mark for manual follow-up
- Check if archived versions exist
- Contact authors if critical paper

### Hardware Dependencies
- Check for simulation/mock modes
- Look for Docker alternatives
- Consider cloud-based testing options

## Ready to Start?

Run your first analysis:
```bash
claude-code "Let's analyze the first 5 papers from September 2025 in README.md using the multi-agent system and generate a report"
```