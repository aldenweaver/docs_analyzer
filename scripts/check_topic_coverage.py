#!/usr/bin/env python3
"""
Documentation Topic Coverage Checker

Checks if GitHub-requested topics are actually covered in the Claude documentation.
This helps identify:
1. Which GitHub issues are invalid (docs already exist)
2. Which are TRUE documentation gaps
3. Which issues could potentially be closed

Uses semantic/keyword search to find topic mentions in docs.
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Set
from collections import defaultdict


class TopicCoverageChecker:
    """Checks if requested topics are covered in documentation"""

    def __init__(self, docs_path: str):
        """
        Initialize checker with docs directory.

        Args:
            docs_path: Path to documentation directory
        """
        self.docs_path = Path(docs_path)
        self.doc_contents = {}
        self._load_docs()

    def _load_docs(self):
        """Load all markdown/mdx files from docs directory"""
        print(f"Loading documentation from {self.docs_path}...")

        if not self.docs_path.exists():
            raise FileNotFoundError(f"Documentation path not found: {self.docs_path}")

        # Find all .md and .mdx files
        doc_files = list(self.docs_path.rglob("*.md")) + list(self.docs_path.rglob("*.mdx"))

        for file_path in doc_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Store relative path as key
                    rel_path = file_path.relative_to(self.docs_path)
                    self.doc_contents[str(rel_path)] = {
                        'path': str(rel_path),
                        'full_path': str(file_path),
                        'content': content,
                        'content_lower': content.lower()
                    }
            except Exception as e:
                print(f"Warning: Could not read {file_path}: {e}")

        print(f"Loaded {len(self.doc_contents)} documentation files")

    def search_topic(self, topic: str) -> Dict[str, Any]:
        """
        Search for a topic in the documentation.

        Uses multiple search strategies:
        1. Exact phrase match
        2. Case-insensitive match
        3. Word-boundary match (avoids partial matches)
        4. Related term matching

        Args:
            topic: Topic to search for (e.g., "Bedrock", "MCP", "AskUserQuestion")

        Returns:
            Dictionary with search results
        """
        results = {
            'topic': topic,
            'found': False,
            'matches': [],
            'confidence': 'none',  # none, low, medium, high
            'match_types': []
        }

        # Normalize topic for searching
        topic_lower = topic.lower()
        topic_words = set(re.findall(r'\w+', topic_lower))

        for doc_path, doc_data in self.doc_contents.items():
            content = doc_data['content']
            content_lower = doc_data['content_lower']

            match_info = {
                'file': doc_path,
                'match_type': None,
                'excerpt': None,
                'line_number': None
            }

            # Strategy 1: Exact case-sensitive match
            if topic in content:
                match_info['match_type'] = 'exact'
                results['found'] = True
                results['confidence'] = 'high'

                # Find context around match
                idx = content.index(topic)
                start = max(0, idx - 50)
                end = min(len(content), idx + len(topic) + 50)
                match_info['excerpt'] = content[start:end]

                # Find line number
                match_info['line_number'] = content[:idx].count('\n') + 1

                results['matches'].append(match_info)
                if 'exact' not in results['match_types']:
                    results['match_types'].append('exact')

            # Strategy 2: Case-insensitive match
            elif topic_lower in content_lower:
                match_info['match_type'] = 'case_insensitive'
                results['found'] = True
                if results['confidence'] == 'none':
                    results['confidence'] = 'high'

                # Find context
                idx = content_lower.index(topic_lower)
                start = max(0, idx - 50)
                end = min(len(content), idx + len(topic) + 50)
                match_info['excerpt'] = content[start:end]
                match_info['line_number'] = content[:idx].count('\n') + 1

                results['matches'].append(match_info)
                if 'case_insensitive' not in results['match_types']:
                    results['match_types'].append('case_insensitive')

            # Strategy 3: Word boundary match (e.g., "bedrock" as a complete word)
            elif re.search(rf'\b{re.escape(topic_lower)}\b', content_lower):
                match_info['match_type'] = 'word_boundary'
                results['found'] = True
                if results['confidence'] == 'none':
                    results['confidence'] = 'medium'

                # Find first occurrence
                match = re.search(rf'\b{re.escape(topic_lower)}\b', content_lower)
                if match:
                    idx = match.start()
                    start = max(0, idx - 50)
                    end = min(len(content), idx + len(topic) + 50)
                    match_info['excerpt'] = content[start:end]
                    match_info['line_number'] = content[:idx].count('\n') + 1

                results['matches'].append(match_info)
                if 'word_boundary' not in results['match_types']:
                    results['match_types'].append('word_boundary')

            # Strategy 4: Related terms (for compound topics)
            # Check if majority of words in topic appear
            elif len(topic_words) > 1:
                words_found = sum(1 for word in topic_words if word in content_lower)
                if words_found >= len(topic_words) * 0.6:  # 60% of words found
                    match_info['match_type'] = 'related_terms'
                    results['found'] = True
                    if results['confidence'] == 'none':
                        results['confidence'] = 'low'

                    # Find a relevant excerpt
                    for word in topic_words:
                        if word in content_lower:
                            idx = content_lower.index(word)
                            start = max(0, idx - 50)
                            end = min(len(content), idx + 100)
                            match_info['excerpt'] = content[start:end]
                            match_info['line_number'] = content[:idx].count('\n') + 1
                            break

                    results['matches'].append(match_info)
                    if 'related_terms' not in results['match_types']:
                        results['match_types'].append('related_terms')

        # Deduplicate matches by file
        if results['matches']:
            seen_files = set()
            unique_matches = []
            for match in results['matches']:
                if match['file'] not in seen_files:
                    seen_files.add(match['file'])
                    unique_matches.append(match)
            results['matches'] = unique_matches

        return results

    def check_all_topics(self, requested_topics: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Check coverage for all requested topics from GitHub issues.

        Args:
            requested_topics: List of topic dictionaries from GitHub issues

        Returns:
            Coverage analysis results
        """
        print(f"\nChecking coverage for {len(requested_topics)} requested topics...")

        coverage_results = {
            'total_topics': len(requested_topics),
            'covered': 0,
            'gaps': 0,
            'high_confidence': 0,
            'medium_confidence': 0,
            'low_confidence': 0,
            'results': []
        }

        # Group topics by name (many issues might request the same topic)
        topics_by_name = defaultdict(list)
        for item in requested_topics:
            topics_by_name[item['topic']].append(item)

        # Check each unique topic
        for topic, issue_items in topics_by_name.items():
            print(f"Searching for: {topic}...")
            search_result = self.search_topic(topic)

            # Add issue information
            search_result['related_issues'] = [
                {
                    'number': item['issue_number'],
                    'title': item['issue_title'],
                    'url': item['issue_url']
                }
                for item in issue_items
            ]

            coverage_results['results'].append(search_result)

            if search_result['found']:
                coverage_results['covered'] += 1

                if search_result['confidence'] == 'high':
                    coverage_results['high_confidence'] += 1
                elif search_result['confidence'] == 'medium':
                    coverage_results['medium_confidence'] += 1
                elif search_result['confidence'] == 'low':
                    coverage_results['low_confidence'] += 1
            else:
                coverage_results['gaps'] += 1

        # Calculate percentages
        total = coverage_results['total_topics']
        coverage_results['coverage_percentage'] = (coverage_results['covered'] / total * 100) if total > 0 else 0
        coverage_results['gap_percentage'] = (coverage_results['gaps'] / total * 100) if total > 0 else 0

        return coverage_results


def generate_coverage_report(coverage_results: Dict[str, Any]) -> str:
    """Generate markdown report from coverage results"""

    report = "# Documentation Topic Coverage Report\n\n"
    report += "**Analysis of GitHub-requested topics against actual Claude documentation**\n\n"

    # Summary stats
    report += "## Executive Summary\n\n"
    report += f"- **Total unique topics requested:** {coverage_results['total_topics']}\n"
    report += f"- **Topics with documentation found:** {coverage_results['covered']} ({coverage_results['coverage_percentage']:.1f}%)\n"
    report += f"- **TRUE documentation gaps:** {coverage_results['gaps']} ({coverage_results['gap_percentage']:.1f}%)\n\n"

    report += "### Confidence Breakdown\n"
    report += f"- **High confidence** (exact/case-insensitive match): {coverage_results['high_confidence']} topics\n"
    report += f"- **Medium confidence** (word boundary match): {coverage_results['medium_confidence']} topics\n"
    report += f"- **Low confidence** (related terms): {coverage_results['low_confidence']} topics\n\n"

    # Covered topics (potentially invalid issues)
    report += "---\n\n## ✅ Topics with Existing Documentation\n\n"
    report += "**These GitHub issues may be INVALID - documentation already exists!**\n\n"

    covered = [r for r in coverage_results['results'] if r['found']]
    if covered:
        for result in sorted(covered, key=lambda x: x['confidence'], reverse=True):
            report += f"### {result['topic']} ({result['confidence'].upper()} confidence)\n\n"
            report += f"**Match types:** {', '.join(result['match_types'])}\n\n"

            report += f"**Related GitHub issues that could potentially be closed:**\n"
            for issue in result['related_issues']:
                report += f"- [#{issue['number']}]({issue['url']}): {issue['title']}\n"

            report += f"\n**Found in {len(result['matches'])} file(s):**\n"
            for match in result['matches'][:3]:  # Show first 3
                report += f"- `{match['file']}` (line {match['line_number']}) - {match['match_type']}\n"
                if match['excerpt']:
                    excerpt = match['excerpt'].replace('\n', ' ')[:100]
                    report += f"  > {excerpt}...\n"

            if len(result['matches']) > 3:
                report += f"  _(and {len(result['matches']) - 3} more files)_\n"

            report += "\n"

    # Gap topics (valid issues)
    report += "---\n\n## ❌ TRUE Documentation Gaps\n\n"
    report += "**These GitHub issues are VALID - no documentation found!**\n\n"

    gaps = [r for r in coverage_results['results'] if not r['found']]
    if gaps:
        for result in gaps:
            report += f"### {result['topic']}\n\n"
            report += f"**Related GitHub issues (valid requests):**\n"
            for issue in result['related_issues']:
                report += f"- [#{issue['number']}]({issue['url']}): {issue['title']}\n"
            report += "\n**Action needed:** Create documentation for this topic\n\n"

    # Recommendations
    report += "---\n\n## Recommendations\n\n"
    report += "### For GitHub Issue Triage\n\n"
    report += f"1. **Review {coverage_results['covered']} 'covered' topics** - documentation exists, consider:\n"
    report += "   - Closing issues as duplicate/invalid\n"
    report += "   - Or improving discoverability if users can't find it\n\n"

    report += f"2. **Address {coverage_results['gaps']} TRUE gaps** - create missing documentation\n\n"

    report += "### For Documentation Team\n\n"
    report += "Focus on the TRUE gaps, especially topics with multiple issue requests:\n\n"

    # Find topics with most requests
    gap_topics_by_issues = [(r, len(r['related_issues'])) for r in gaps]
    gap_topics_by_issues.sort(key=lambda x: x[1], reverse=True)

    for result, issue_count in gap_topics_by_issues[:5]:
        report += f"- **{result['topic']}** ({issue_count} issue requests)\n"

    return report


def main():
    """Main execution"""
    import sys

    # Add parent directory to path for imports
    sys.path.insert(0, str(Path(__file__).parent.parent))

    # Load GitHub issues findings
    findings_path = Path("GITHUB_ISSUES_FINDINGS.md")
    raw_data_path = Path("github_issues_raw.json")

    if not raw_data_path.exists():
        print("Error: github_issues_raw.json not found. Run github_issues_research.py first.")
        return 1

    # Load raw issue data
    with open(raw_data_path, 'r') as f:
        issues = json.load(f)

    # Extract requested topics (same logic as in github_issues_research.py)
    print("Extracting requested topics from issues...")
    from scripts.github_issues_research import GitHubIssuesResearcher

    researcher = GitHubIssuesResearcher()
    requested_topics = researcher.extract_requested_topics(issues)

    print(f"Found {len(requested_topics)} topic requests")

    # Check coverage
    docs_path = "/Users/alden/dev/claude_docs_clone_mintlify/docs"
    if not Path(docs_path).exists():
        print(f"Error: Documentation path not found: {docs_path}")
        print("Please update docs_path in the script to point to your Claude docs")
        return 1

    checker = TopicCoverageChecker(docs_path)
    coverage_results = checker.check_all_topics(requested_topics)

    # Generate report
    report = generate_coverage_report(coverage_results)

    # Save report
    output_path = "TOPIC_COVERAGE_REPORT.md"
    with open(output_path, 'w') as f:
        f.write(report)

    print(f"\n✅ Coverage report written to {output_path}")

    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total topics: {coverage_results['total_topics']}")
    print(f"Covered: {coverage_results['covered']} ({coverage_results['coverage_percentage']:.1f}%)")
    print(f"TRUE gaps: {coverage_results['gaps']} ({coverage_results['gap_percentage']:.1f}%)")
    print("="*60)

    return 0


if __name__ == "__main__":
    exit(main())
