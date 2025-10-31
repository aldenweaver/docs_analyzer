#!/usr/bin/env python3
"""
Run GitHub-Informed quality checker on docs and report findings
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from fixers.github_informed_fixer import GitHubInformedFixer
from core.config import Config
from collections import Counter

def main():
    docs_path = Path("/Users/alden/dev/claude_docs_clone_mintlify/docs")

    if not docs_path.exists():
        print(f"Error: {docs_path} not found")
        return 1

    # Initialize fixer
    config = Config()
    fixer = GitHubInformedFixer(config)

    print("Running GitHub-informed quality checker...")
    print(f"Analyzing docs in: {docs_path}\n")

    # Find all MDX files
    doc_files = list(docs_path.rglob("*.md")) + list(docs_path.rglob("*.mdx"))

    all_issues = []
    files_with_issues = 0

    for file_path in doc_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            issues = fixer.check_file(str(file_path), content)

            if issues:
                files_with_issues += 1
                all_issues.extend(issues)
                print(f"📄 {file_path.relative_to(docs_path)}: {len(issues)} issue(s)")
                for issue in issues:
                    print(f"   - {issue.issue_type}: {issue.description[:80]}...")

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    # Summary
    print("\n" + "="*70)
    print("GITHUB-INFORMED QUALITY CHECK SUMMARY")
    print("="*70)
    print(f"Files analyzed: {len(doc_files)}")
    print(f"Files with issues: {files_with_issues}")
    print(f"Total issues found: {len(all_issues)}\n")

    # Count by type
    issue_types = Counter(issue.issue_type for issue in all_issues)
    print("Issues by type:")
    for issue_type, count in issue_types.most_common():
        print(f"  - {issue_type}: {count}")

    # Count by severity
    severities = Counter(issue.severity for issue in all_issues)
    print("\nIssues by severity:")
    for severity, count in severities.most_common():
        print(f"  - {severity}: {count}")

    print("="*70)

    return 0

if __name__ == "__main__":
    exit(main())
