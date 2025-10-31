#!/usr/bin/env python3
"""
Automated GitHub Issues Research Script

Fetches and analyzes documentation-related issues from the Claude Code GitHub repository
to identify patterns and implementable fixes for the docs_analyzer tool.
"""

import os
import json
import requests
from datetime import datetime, timezone
from collections import Counter, defaultdict
from typing import List, Dict, Any
import re


class GitHubIssuesResearcher:
    """Automates research of GitHub issues for documentation patterns."""

    def __init__(self, repo: str = "anthropics/claude-code", label: str = "documentation"):
        self.repo = repo
        self.label = label
        self.api_base = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
        }

        # Add token if available (for higher rate limits)
        github_token = os.environ.get("GITHUB_TOKEN")
        if github_token:
            self.headers["Authorization"] = f"token {github_token}"

    def fetch_issues(self, state: str = "open", max_issues: int = None) -> List[Dict[str, Any]]:
        """
        Fetch issues from GitHub API with pagination.

        Args:
            state: Issue state (open/closed/all)
            max_issues: Maximum issues to fetch. If None, fetches ALL issues.

        Returns:
            List of issues
        """
        all_issues = []
        page = 1
        per_page = 100  # GitHub max per page

        print(f"Fetching issues from {self.repo} with label '{self.label}'...")

        while True:
            url = f"{self.api_base}/repos/{self.repo}/issues"
            params = {
                "state": state,
                "labels": self.label,
                "per_page": per_page,
                "page": page,
                "sort": "created",
                "direction": "desc"
            }

            response = requests.get(url, headers=self.headers, params=params)

            if response.status_code != 200:
                raise Exception(f"GitHub API error: {response.status_code} - {response.text}")

            issues = response.json()

            if not issues:
                break

            all_issues.extend(issues)
            print(f"Fetched page {page}: {len(issues)} issues (total: {len(all_issues)})")

            # Stop if we've reached max_issues
            if max_issues and len(all_issues) >= max_issues:
                all_issues = all_issues[:max_issues]
                break

            # Stop if we got less than per_page (last page)
            if len(issues) < per_page:
                break

            page += 1

        print(f"Total issues fetched: {len(all_issues)}")
        return all_issues

    def categorize_issue(self, issue: Dict[str, Any]) -> str:
        """Categorize issue based on title and body content."""
        title = issue.get("title", "").lower()
        body = issue.get("body", "").lower() if issue.get("body") else ""
        text = f"{title} {body}"

        # Pattern matching for categories
        if any(keyword in text for keyword in ["missing", "no documentation", "undocumented", "not documented", "need docs"]):
            return "Missing"
        elif any(keyword in text for keyword in ["outdated", "old", "deprecated", "stale", "update"]):
            return "Outdated"
        elif any(keyword in text for keyword in ["unclear", "confusing", "hard to understand", "difficult", "explain", "clarify"]):
            return "Unclear"
        elif any(keyword in text for keyword in ["can't find", "cannot find", "where is", "how to find", "search"]):
            return "Findability"
        elif any(keyword in text for keyword in ["context", "prerequisite", "assumes", "background", "explain why"]):
            return "Context"
        else:
            # Default to Unclear if we can't determine
            return "Unclear"

    def calculate_age_days(self, created_at: str) -> int:
        """Calculate issue age in days."""
        created = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        return (now - created).days

    def get_upvotes(self, issue: Dict[str, Any]) -> int:
        """Get number of 👍 reactions."""
        reactions = issue.get("reactions", {})
        return reactions.get("+1", 0)

    def calculate_impact_score(self, upvotes: int, comments: int, age_days: int) -> float:
        """Calculate impact score: (upvotes × comments) / age."""
        if age_days == 0:
            age_days = 1  # Avoid division by zero
        return (upvotes * max(comments, 1)) / age_days

    def extract_patterns(self, issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract patterns from issues."""
        categorized = defaultdict(list)

        for issue in issues:
            category = self.categorize_issue(issue)
            age_days = self.calculate_age_days(issue["created_at"])
            upvotes = self.get_upvotes(issue)
            comments = issue.get("comments", 0)
            impact = self.calculate_impact_score(upvotes, comments, age_days)

            categorized[category].append({
                "number": issue["number"],
                "title": issue["title"],
                "upvotes": upvotes,
                "comments": comments,
                "age_days": age_days,
                "impact_score": impact,
                "url": issue["html_url"],
                "body": issue.get("body", "")[:200]  # First 200 chars
            })

        return categorized

    def extract_requested_topics(self, issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Extract specific topics/features users are requesting documentation for.

        This addresses the TRUE gap detection: what topics are users asking for
        that might not exist in the docs?
        """
        requested_topics = []

        for issue in issues:
            title = issue.get("title", "")
            body = issue.get("body", "") or ""
            number = issue["number"]

            # Extract topic from common patterns
            topic = None

            # Pattern 1: "[DOCS] Missing Documentation for X"
            match = re.search(r'\[DOCS\].*(?:missing|add).*(?:documentation|docs).*for\s+(.+)', title, re.IGNORECASE)
            if match:
                topic = match.group(1).strip()

            # Pattern 2: "[DOCS] Document X"
            if not topic:
                match = re.search(r'\[DOCS\].*document\s+(.+)', title, re.IGNORECASE)
                if match:
                    topic = match.group(1).strip()

            # Pattern 3: "Missing Documentation for X" (without [DOCS] tag)
            if not topic:
                match = re.search(r'missing.*documentation.*for\s+(.+)', title, re.IGNORECASE)
                if match:
                    topic = match.group(1).strip()

            # Pattern 4: Look for specific features mentioned
            if not topic:
                # Common Claude Code features mentioned in issues
                features = [
                    "AskUserQuestion", "ultrathink", "thinking mode", "subagent",
                    "MCP", "Bedrock", "AWS", "slash command", "skill", "YAML frontmatter",
                    "tool", "agent", "Explore", "Plan", "Task"
                ]
                for feature in features:
                    if feature.lower() in title.lower() or feature.lower() in body.lower():
                        topic = feature
                        break

            if topic:
                # Clean up the topic
                topic = topic.rstrip('.!?')
                topic = re.sub(r'\s*\(.*?\)', '', topic)  # Remove parentheticals

                requested_topics.append({
                    "topic": topic,
                    "issue_number": number,
                    "issue_title": title,
                    "issue_url": issue["html_url"]
                })

        return requested_topics

    def identify_common_themes(self, issues_by_category: Dict[str, List[Dict]]) -> Dict[str, List[str]]:
        """Identify common themes within each category."""
        themes = {}

        for category, issues in issues_by_category.items():
            # Extract keywords from titles
            all_titles = " ".join([issue["title"].lower() for issue in issues])

            # Common documentation-related keywords
            keywords = [
                "example", "guide", "tutorial", "setup", "configuration",
                "api", "error", "troubleshooting", "installation", "usage",
                "cli", "command", "option", "feature", "integration"
            ]

            found_themes = []
            for keyword in keywords:
                if keyword in all_titles:
                    count = all_titles.count(keyword)
                    if count >= 2:  # At least 2 mentions
                        found_themes.append(f"{keyword} ({count} mentions)")

            themes[category] = found_themes[:5]  # Top 5 themes

        return themes

    def generate_findings_report(self, issues: List[Dict[str, Any]]) -> str:
        """Generate comprehensive findings report."""
        categorized = self.extract_patterns(issues)
        themes = self.identify_common_themes(categorized)
        requested_topics = self.extract_requested_topics(issues)

        # Calculate stats
        total_issues = len(issues)
        category_counts = {cat: len(iss) for cat, iss in categorized.items()}

        # Top 5 by impact
        all_with_impact = []
        for category, issues_list in categorized.items():
            for issue in issues_list:
                issue["category"] = category
                all_with_impact.append(issue)

        top_issues = sorted(all_with_impact, key=lambda x: x["impact_score"], reverse=True)[:5]

        # Generate report
        report = f"""# GitHub Issues Research - Automated Analysis

**Research Date:** {datetime.now().strftime('%Y-%m-%d')}
**Repository:** https://github.com/{self.repo}
**Filter:** `state:open label:{self.label}`
**Issues Analyzed:** {total_issues}
**Analysis Method:** Automated via GitHub API

---

## Executive Summary

Analyzed {total_issues} open documentation issues from the Claude Code repository.

**Category Breakdown:**
"""

        for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_issues) * 100
            report += f"- **{category}:** {count} issues ({percentage:.1f}%)\n"

        report += "\n---\n\n## Issues Data Collection\n\n"
        report += "| Issue # | Title | Category | Upvotes (👍) | Comments | Age (days) | Impact Score |\n"
        report += "|---------|-------|----------|--------------|----------|------------|-------------|\n"

        # Show top 20 by impact
        for issue in top_issues[:20]:
            title_short = issue["title"][:50] + "..." if len(issue["title"]) > 50 else issue["title"]
            report += f"| #{issue['number']} | {title_short} | {issue['category']} | {issue['upvotes']} | {issue['comments']} | {issue['age_days']} | {issue['impact_score']:.2f} |\n"

        report += "\n---\n\n## Pattern Analysis by Category\n\n"

        for category in ["Missing", "Outdated", "Unclear", "Findability", "Context"]:
            count = category_counts.get(category, 0)
            percentage = (count / total_issues * 100) if total_issues > 0 else 0

            report += f"### {category} Documentation\n\n"
            report += f"**Count:** {count} issues ({percentage:.1f}%)\n\n"

            if category in themes and themes[category]:
                report += "**Common themes:**\n"
                for theme in themes[category]:
                    report += f"- {theme}\n"

            if category in categorized:
                report += f"\n**Example issues:**\n"
                for issue in categorized[category][:3]:
                    report += f"- [#{issue['number']}]({issue['url']}): {issue['title']}\n"

            report += "\n"

        report += "---\n\n## Top 5 Most-Impactful Issues\n\n"
        report += "*Ranked by: (Upvotes × Comments) ÷ Age*\n\n"

        for i, issue in enumerate(top_issues, 1):
            impact = "HIGH" if issue["impact_score"] > 5 else "MEDIUM" if issue["impact_score"] > 1 else "LOW"

            report += f"{i}. **Issue #{issue['number']}:** [{issue['title']}]({issue['url']})\n"
            report += f"   - Category: {issue['category']}\n"
            report += f"   - Impact: {impact} (score: {issue['impact_score']:.2f})\n"
            report += f"   - Engagement: {issue['upvotes']} upvotes, {issue['comments']} comments\n"
            report += f"   - Age: {issue['age_days']} days\n\n"

        report += "---\n\n## Implementable Fixes Analysis\n\n"
        report += self._generate_fix_candidates(categorized, themes)

        report += "\n---\n\n## Requested Topics (TRUE Gap Detection)\n\n"
        report += f"**Extracted {len(requested_topics)} specific topic requests from issues:**\n\n"

        if requested_topics:
            # Group by topic
            topic_counts = {}
            topic_issues = {}
            for item in requested_topics:
                topic = item["topic"]
                if topic not in topic_counts:
                    topic_counts[topic] = 0
                    topic_issues[topic] = []
                topic_counts[topic] += 1
                topic_issues[topic].append(f"[#{item['issue_number']}]({item['issue_url']})")

            # Sort by frequency
            sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)

            report += "| Topic | Mentions | Related Issues |\n"
            report += "|-------|----------|----------------|\n"

            for topic, count in sorted_topics[:20]:  # Top 20
                issues_list = ", ".join(topic_issues[topic][:3])  # Show first 3
                if len(topic_issues[topic]) > 3:
                    issues_list += f" (+{len(topic_issues[topic]) - 3} more)"
                report += f"| {topic} | {count} | {issues_list} |\n"

            report += "\n**These are the specific features/topics users are requesting documentation for.**\n"
            report += "To truly address these gaps, check if these topics exist in the actual Claude docs.\n\n"

        report += "\n---\n\n## Key Insights\n\n"
        report += "**1. Root Causes:**\n"
        report += f"- Documentation completeness: {category_counts.get('Missing', 0)} issues about missing docs\n"
        report += f"- Content clarity: {category_counts.get('Unclear', 0)} issues about comprehension\n"
        report += f"- Information architecture: {category_counts.get('Findability', 0)} issues about finding content\n\n"

        report += "**2. Systematic Patterns:**\n"
        top_category = max(category_counts.items(), key=lambda x: x[1])
        report += f"- Most common issue type: {top_category[0]} ({top_category[1]} issues)\n"
        report += f"- Average issue age: {sum(i['age_days'] for i in all_with_impact) / len(all_with_impact):.1f} days\n"
        report += f"- Average engagement: {sum(i['comments'] for i in all_with_impact) / len(all_with_impact):.1f} comments per issue\n\n"

        report += "**3. Quick Wins:**\n"
        report += "- Issues will be identified after manual review of top-impact items\n\n"

        report += "---\n\n## Next Steps\n\n"
        report += "- [ ] Review top 5 high-impact issues manually\n"
        report += "- [ ] Validate these patterns exist in docs/about-claude/\n"
        report += "- [ ] Design GitHubInformedFixer class structure\n"
        report += "- [ ] Implement detection and fixing logic\n"
        report += "- [ ] Run comparative analysis\n\n"

        report += "---\n\n"
        report += f"**Analysis completed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"**Tool:** Automated GitHub Issues Researcher\n"

        return report

    def _generate_fix_candidates(self, categorized: Dict[str, List[Dict]], themes: Dict[str, List[str]]) -> str:
        """Generate fix candidate suggestions."""
        fixes = ""

        # Analyze patterns for each category
        if "Missing" in categorized and categorized["Missing"]:
            fixes += "### Fix Candidate #1: Missing Documentation Detection\n"
            fixes += "**Pattern:** Users reporting features/concepts that lack documentation\n"
            fixes += f"**Example Issues:** " + ", ".join([f"#{i['number']}" for i in categorized["Missing"][:3]]) + "\n"
            fixes += "**How to detect:** Flag pages with:\n"
            fixes += "- Very short content (< 100 words)\n"
            fixes += "- Missing code examples when discussing code features\n"
            fixes += "- No 'Prerequisites' section for procedural content\n\n"
            fixes += "**How to fix:** Flag for manual review with suggested templates\n"
            fixes += "**Effort:** MEDIUM\n"
            fixes += "**Impact:** HIGH\n"
            fixes += "**Implement?** YES\n\n"

        if "Unclear" in categorized and categorized["Unclear"]:
            fixes += "### Fix Candidate #2: Clarity Improvements\n"
            fixes += "**Pattern:** Users finding existing documentation confusing\n"
            fixes += f"**Example Issues:** " + ", ".join([f"#{i['number']}" for i in categorized["Unclear"][:3]]) + "\n"
            fixes += "**How to detect:** Look for:\n"
            fixes += "- Jargon without definitions\n"
            fixes += "- Missing examples\n"
            fixes += "- Long paragraphs without structure\n\n"
            fixes += "**How to fix:** Add warnings/suggestions for:\n"
            fixes += "- Technical terms that need glossary entries\n"
            fixes += "- Code mentions without examples\n"
            fixes += "**Effort:** SMALL\n"
            fixes += "**Impact:** MEDIUM\n"
            fixes += "**Implement?** YES\n\n"

        if "Findability" in categorized and categorized["Findability"]:
            fixes += "### Fix Candidate #3: Findability/Navigation\n"
            fixes += "**Pattern:** Users can't locate existing information\n"
            fixes += f"**Example Issues:** " + ", ".join([f"#{i['number']}" for i in categorized["Findability"][:3]]) + "\n"
            fixes += "**How to detect:** Check for:\n"
            fixes += "- Missing cross-references\n"
            fixes += "- Inconsistent terminology across pages\n\n"
            fixes += "**How to fix:** Suggest adding cross-links for related concepts\n"
            fixes += "**Effort:** MEDIUM\n"
            fixes += "**Impact:** MEDIUM\n"
            fixes += "**Implement?** MAYBE\n\n"

        return fixes


def main():
    """Main execution function."""
    researcher = GitHubIssuesResearcher()

    try:
        # Fetch ALL issues (no limit)
        print("Fetching ALL documentation issues from GitHub...")
        issues = researcher.fetch_issues(max_issues=None)

        # Generate report
        report = researcher.generate_findings_report(issues)

        # Write to file
        output_path = "GITHUB_ISSUES_FINDINGS.md"
        with open(output_path, "w") as f:
            f.write(report)

        print(f"\n✅ Research complete! Findings written to {output_path}")
        print(f"📊 Analyzed {len(issues)} issues")

        # Also save raw data as JSON for further analysis
        json_path = "github_issues_raw.json"
        with open(json_path, "w") as f:
            json.dump(issues, f, indent=2)

        print(f"📁 Raw data saved to {json_path}")

    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
