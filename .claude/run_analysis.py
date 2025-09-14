#!/usr/bin/env python3
"""
Main coordinator that uses Claude Code Task tool to analyze papers in parallel.
This script should be run by Claude Code, which will handle the Task tool calls.
"""

import json
import re
import time
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

class SimplePaperAnalyzer:
    """Coordinates parallel paper analysis using Claude Code tasks"""

    def __init__(self):
        self.output_file = Path(".claude/analysis/dataset.md")
        self.progress_file = Path(".claude/analysis/progress.json")
        self.output_file.parent.mkdir(parents=True, exist_ok=True)

        # Initialize dataset file
        if not self.output_file.exists():
            header = f"""# Multi-Agent Systems Dataset

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}

| Paper Title | ArXiv URL | GitHub URL | Valid | Codebase Summary | Relevance |
|-------------|-----------|------------|-------|------------------|-----------|
"""
            self.output_file.write_text(header)

        # Load progress
        self.progress = self.load_progress()

    def load_progress(self) -> Dict:
        """Load processing progress"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        return {"completed": [], "last_batch": 0}

    def save_progress(self):
        """Save processing progress"""
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)

    def extract_papers_from_file(self, file_path: Path) -> List[Dict]:
        """Extract papers from a markdown file"""
        papers = []
        content = file_path.read_text(encoding='utf-8')

        # Split by horizontal rules
        entries = re.split(r'\n---+\n', content)

        for entry in entries:
            # Find arxiv links
            arxiv_match = re.search(r'\[([^\]]+)\]\((https://arxiv\.org/[^\)]+)\)', entry)
            if arxiv_match:
                title = arxiv_match.group(1)
                arxiv_url = arxiv_match.group(2)

                # Extract paper ID
                paper_id = re.search(r'(\d{4}\.\d{5})', arxiv_url)
                if paper_id:
                    paper_id = paper_id.group(1)
                else:
                    paper_id = arxiv_url.split('/')[-1]

                # Skip if already processed
                if paper_id not in self.progress["completed"]:
                    papers.append({
                        "title": title,
                        "arxiv_url": arxiv_url,
                        "content": entry[:2000],
                        "paper_id": paper_id
                    })

        return papers

    def get_all_papers(self) -> List[Dict]:
        """Get all papers from markdown files"""
        paper_files = [
            Path("README.md"),
            Path("resources/Autonomous_Agents_Research_Papers_2025.md"),
            Path("resources/Autonomous_Agents_Research_Papers_2025_2.md"),
            Path("resources/Autonomous_Agents_Research_Papers_2024.md"),
            Path("resources/Autonomous_Agents_Research_Papers_2023.md")
        ]

        all_papers = []
        for file_path in paper_files:
            if file_path.exists():
                papers = self.extract_papers_from_file(file_path)
                all_papers.extend(papers)
                print(f"Found {len(papers)} unprocessed papers in {file_path}")

        return all_papers

    def append_to_dataset(self, result: Dict):
        """Append result to dataset markdown file"""
        # Format the row
        title = result.get("title", "Unknown")[:50]
        arxiv_id = result.get("arxiv_url", "").split("/")[-1]
        github_url = result.get("github_url", "Not found")
        valid = "✓" if result.get("github_valid", False) else "✗"
        summary = result.get("codebase_summary", "N/A")[:80]
        relevance = result.get("relevance_score", 0)

        row = f"| {title} | [{arxiv_id}]({result.get('arxiv_url', '')}) | {github_url} | {valid} | {summary} | {relevance:.1f} |\n"

        with open(self.output_file, 'a', encoding='utf-8') as f:
            f.write(row)

    def process_batch_with_tasks(self, batch: List[Dict]) -> List[Dict]:
        """
        Process a batch of papers using Claude Code Task tool.
        This function will be called by Claude Code to launch parallel tasks.
        """
        print(f"\n{'='*60}")
        print(f"Processing batch of {len(batch)} papers")
        print(f"{'='*60}")

        results = []

        # IMPORTANT: This is where Claude Code will use the Task tool
        # to launch parallel agents for each paper
        for paper in batch:
            print(f"\n→ Analyzing: {paper['title'][:60]}...")

            # Claude Code will replace this section with actual Task tool calls
            # launching research-paper-agent-simple and developer-agent-simple in parallel

            # For now, create a placeholder that shows what we expect
            result = {
                "title": paper["title"],
                "arxiv_url": paper["arxiv_url"],
                "paper_id": paper["paper_id"],
                "github_url": None,  # Will be filled by research-paper-agent
                "github_valid": False,  # Will be filled by developer-agent
                "codebase_summary": "Pending analysis",  # Will be filled by developer-agent
                "relevance_score": 0.0  # Will be filled by research-paper-agent
            }

            results.append(result)

            # Mark as completed
            self.progress["completed"].append(paper["paper_id"])

        return results

    def run(self, batch_size: int = 10, max_papers: Optional[int] = None):
        """Main processing loop"""
        print("""
╔════════════════════════════════════════════╗
║   Multi-Agent Papers Dataset Builder      ║
║   Parallel Processing with Claude Code    ║
╚════════════════════════════════════════════╝
        """)

        # Get all unprocessed papers
        papers = self.get_all_papers()

        if max_papers:
            papers = papers[:max_papers]

        print(f"\nTotal papers to process: {len(papers)}")
        print(f"Batch size: {batch_size}")
        print(f"Output file: {self.output_file}")

        # Process in batches
        for i in range(0, len(papers), batch_size):
            batch = papers[i:i + batch_size]
            batch_num = i // batch_size + 1

            # Process batch with parallel tasks
            results = self.process_batch_with_tasks(batch)

            # Save results
            for result in results:
                self.append_to_dataset(result)

            # Update progress
            self.progress["last_batch"] = batch_num
            self.save_progress()

            print(f"\n✓ Batch {batch_num} complete")
            print(f"  Processed: {len(self.progress['completed'])} papers total")

            # Rate limiting between batches
            if i + batch_size < len(papers):
                print("\n⏳ Waiting 5 seconds before next batch...")
                time.sleep(5)

        print(f"\n{'='*60}")
        print(f"✅ COMPLETE! Processed {len(self.progress['completed'])} papers")
        print(f"📊 Results saved to: {self.output_file}")
        print(f"{'='*60}")

def main():
    """Entry point for Claude Code to run"""
    analyzer = SimplePaperAnalyzer()

    # Start with a small test batch
    # Claude Code will modify this to process all papers
    analyzer.run(batch_size=10, max_papers=30)  # Test with first 30 papers

if __name__ == "__main__":
    main()