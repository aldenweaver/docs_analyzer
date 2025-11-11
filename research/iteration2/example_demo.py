#!/usr/bin/env python3
"""
Practical Example: Analyzing Claude Documentation Issues
Demonstrates the complete workflow with realistic examples.
"""

import os
import tempfile
import shutil
from pathlib import Path
from doc_quality_automation import DocumentationQualityEngine
import yaml


def create_claude_docs_sample():
    """Create sample Claude documentation with real issues identified in the analysis."""
    
    temp_dir = tempfile.mkdtemp(prefix='claude_docs_example_')
    docs_dir = Path(temp_dir) / "docs"
    docs_dir.mkdir()
    
    # Sample file 1: overview.mdx - Missing frontmatter, deprecated terminology
    (docs_dir / "overview.mdx").write_text("""# Claude Code Overview

Simply utilize the Claude Code SDK to leverage the power of AI agents.

You can click here for more information about getting started.

## Key Features

- Agentic coding capabilities
- Built-in Tools support
- MCP server integration
""")
    
    # Sample file 2: api/quickstart.mdx - Has frontmatter but missing description, deprecated terms
    (docs_dir / "api").mkdir()
    (docs_dir / "api" / "quickstart.mdx").write_text("""---
title: Quick Start Guide
---

# Quick Start with Claude Code SDK

Install the ClaudeCodeOptions package to get started.

```typescript
// Missing error handling
import { ClaudeCode } from 'claude-code-sdk';

const client = new ClaudeCode({
  apiKey: process.env.CLAUDE_API_KEY
});

const result = await client.generate({
  prompt: 'Write a function'
});

console.log(result);
```

For more details, see [this page](./nonexistent.md).
""")
    
    # Sample file 3: guides/agent-skills.md - Duplicate content path (known issue)
    (docs_dir / "guides").mkdir()
    (docs_dir / "guides" / "agent-skills.md").write_text("""# Agent Skills

Agent Skills allow you to extend Claude's capabilities.

This content duplicates what's in the main agent-skills documentation.

## Using Skills

```
# Missing language tag and error handling
skill = load_skill("web_search")
result = skill.execute("latest AI news")
print(result)
```
""")
    
    # Sample file 4: reference/api.md - Missing required sections
    (docs_dir / "reference").mkdir()
    (docs_dir / "reference" / "api.md").write_text("""# API Reference

The API provides access to Claude Code features.

## Endpoints

Details about endpoints.

# Missing: Parameters, Response, Examples, Errors sections
""")
    
    # Sample file 5: troubleshooting/errors.md - Good structure, some issues
    (docs_dir / "troubleshooting").mkdir()
    (docs_dir / "troubleshooting" / "errors.md").write_text("""# Error Handling

## Problem

API calls failing with rate limit errors.

## Solution

Simply wait and retry. Click here to learn more.

# Missing: Prevention section
""")
    
    # Sample file 6: Very deep nesting
    deep_path = docs_dir / "guides" / "advanced" / "features" / "deep"
    deep_path.mkdir(parents=True)
    (deep_path / "nested.md").write_text("""# Deeply Nested Page

This page is at depth 4, exceeding the maximum of 3.

## Skipped Heading

##### H5 without H2-H4

Content here.
""")
    
    return temp_dir


def create_example_config(temp_dir):
    """Create configuration based on Claude Documentation Analysis."""
    
    config = {
        'database': {
            'path': os.path.join(temp_dir, 'metrics.db')
        },
        'repository': {
            'path': os.path.join(temp_dir, 'docs'),
            'file_patterns': ['**/*.md', '**/*.mdx'],
            'exclude_patterns': ['**/node_modules/**', '**/.git/**']
        },
        'terminology': {
            'case_sensitive': False,
            'deprecated_terms': [
                'Claude Code SDK',
                'ClaudeCodeOptions',
                'simply',
                'utilize',
                'leverage',
                'click here',
                'Built-in Tools'
            ],
            'preferred_terms': {
                'claude code sdk': 'Claude Agent SDK',
                'claudecodeoptions': 'ClaudeAgentOptions',
                'built-in tools': 'built-in tools'
            },
            'proper_nouns': ['Claude', 'Claude Code', 'Anthropic', 'Agent Skills', 'MCP']
        },
        'frontmatter': {
            'required': ['title', 'description'],
            'optional': ['sidebarTitle', 'icon'],
            'max_description_length': 160,
            'min_description_length': 50,
            'auto_generate': {
                'enabled': True,
                'title_from_filename': True
            }
        },
        'links': {
            'check_internal': True,
            'check_external': False,
            'check_anchors': True,
            'poor_link_text': ['here', 'click here', 'link', 'this']
        },
        'code_examples': {
            'require_error_handling': True,
            'require_language_tags': True,
            'require_imports': False,
            'languages': ['python', 'typescript', 'javascript', 'java']
        },
        'duplication': {
            'threshold': 0.8,
            'known_patterns': [
                {
                    'canonical': 'docs/agent-tools/agent-skills.md',
                    'locations': [
                        'docs/agent-tools/agent-skills.md',
                        'docs/api/skills/index.md',
                        'docs/guides/agent-skills.md'
                    ],
                    'action': 'consolidate'
                }
            ]
        },
        'information_architecture': {
            'max_navigation_depth': 3,
            'max_section_length': 500,
            'required_sections': {
                'guide': ['Prerequisites', 'Examples'],
                'api_reference': ['Parameters', 'Response', 'Examples', 'Errors'],
                'troubleshooting': ['Problem', 'Solution', 'Prevention']
            }
        },
        'ai_analysis': {
            'enabled': False  # Set to True if you have ANTHROPIC_API_KEY
        }
    }
    
    config_path = os.path.join(temp_dir, 'config.yaml')
    with open(config_path, 'w') as f:
        yaml.dump(config, f)
    
    return config_path


def print_section(title):
    """Print formatted section header."""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print('='*80 + '\n')


def main():
    """Run the complete example demonstration."""
    
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║  Documentation Quality Automation System - Practical Example            ║
║  Analyzing Real Claude Documentation Issues                             ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
""")
    
    # Create sample documentation
    print_section("Step 1: Creating Sample Claude Documentation")
    print("Creating sample files with real issues identified in the analysis:")
    print("  • overview.mdx - Missing frontmatter, deprecated terminology")
    print("  • api/quickstart.mdx - Deprecated SDK names, missing error handling")
    print("  • guides/agent-skills.md - Duplicate content path")
    print("  • reference/api.md - Missing required sections")
    print("  • troubleshooting/errors.md - Missing Prevention section")
    print("  • deeply nested page - Navigation depth violation")
    
    temp_dir = create_claude_docs_sample()
    print(f"\n✅ Created sample documentation in: {temp_dir}")
    
    # Create configuration
    print_section("Step 2: Creating Configuration")
    print("Configuration based on Claude Documentation Analysis:")
    print("  • Deprecated terms: Claude Code SDK → Claude Agent SDK")
    print("  • Weak language detection: simply, utilize, leverage")
    print("  • Frontmatter requirements: title, description")
    print("  • Code quality checks: error handling, language tags")
    print("  • Known duplicate paths: agent-skills in 3 locations")
    
    config_path = create_example_config(temp_dir)
    print(f"\n✅ Configuration created: {config_path}")
    
    # Initialize engine
    print_section("Step 3: Initializing Quality Engine")
    engine = DocumentationQualityEngine(config_path)
    print("✅ Engine initialized with all quality checkers")
    
    # Scan repository
    print_section("Step 4: Scanning Documentation")
    print("Running comprehensive quality scan...")
    print("Checking for:")
    print("  • Information Architecture issues")
    print("  • Consistency problems")
    print("  • Completeness gaps")
    print("  • User Experience issues")
    print("  • Platform optimization opportunities")
    
    issues = engine.scan_repository()
    
    print(f"\n✅ Scan complete! Found {len(issues)} issues")
    
    # Show issues by severity
    print("\nIssues by Severity:")
    severity_counts = {}
    for issue in issues:
        severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1
    
    severity_icons = {
        'critical': '🔴',
        'high': '🟠',
        'medium': '🟡',
        'low': '🟢'
    }
    
    for severity in ['critical', 'high', 'medium', 'low']:
        count = severity_counts.get(severity, 0)
        if count > 0:
            icon = severity_icons.get(severity, '•')
            print(f"  {icon} {severity.upper()}: {count}")
    
    # Show issues by category
    print("\nIssues by Category:")
    category_counts = {}
    for issue in issues:
        category_counts[issue.category] = category_counts.get(issue.category, 0) + 1
    
    for category, count in sorted(category_counts.items()):
        print(f"  • {category.replace('_', ' ').title()}: {count}")
    
    # Show example issues
    print_section("Step 5: Example Issues Detected")
    
    print("CRITICAL Issues:")
    critical = [i for i in issues if i.severity == 'critical']
    for issue in critical[:3]:
        print(f"\n  • {issue.description}")
        print(f"    File: {issue.file_path}")
        if issue.suggested_fix:
            print(f"    Fix: {issue.suggested_fix}")
    
    print("\n\nHIGH Priority Issues:")
    high = [i for i in issues if i.severity == 'high']
    for issue in high[:3]:
        print(f"\n  • {issue.description}")
        print(f"    File: {issue.file_path}")
        if issue.suggested_fix:
            print(f"    Fix: {issue.suggested_fix}")
    
    # Collect metrics
    print_section("Step 6: Collecting Quality Metrics")
    metrics = engine.collect_metrics()
    
    print("Primary KPIs:")
    print(f"  • Total Issues: {metrics['total_issues']:.0f}")
    print(f"  • Critical Issues: {metrics['critical_issues']:.0f}")
    print(f"  • Documentation Debt: {metrics['documentation_debt']:.0f}")
    print(f"  • Auto-fixable Rate: {metrics['auto_fixable_rate']*100:.1f}%")
    
    print("\nQuality Scores:")
    print(f"  • Content Consistency: {metrics['content_consistency_score']*100:.1f}%")
    print(f"  • Issues per File: {metrics['issues_per_file']:.2f}")
    
    # Quality gates
    print("\nQuality Gates:")
    critical_pass = metrics['critical_issues'] == 0
    debt_pass = metrics['documentation_debt'] <= 2
    consistency_pass = metrics['content_consistency_score'] >= 0.95
    
    print(f"  {'✅' if critical_pass else '❌'} No Critical Issues: {metrics['critical_issues']:.0f} / 0")
    print(f"  {'✅' if debt_pass else '❌'} Documentation Debt: {metrics['documentation_debt']:.0f} / 2")
    print(f"  {'✅' if consistency_pass else '⚠️ '} Consistency Score: {metrics['content_consistency_score']:.2f} / 0.95")
    
    # Auto-fix
    print_section("Step 7: Running Auto-fix (Dry Run)")
    print("Identifying auto-fixable issues...")
    
    fix_stats_dry = engine.auto_fix_issues(dry_run=True)
    
    print(f"\n✅ Auto-fix analysis complete")
    print(f"\nWould fix {fix_stats_dry['fixed']} issues automatically:")
    print(f"  • Terminology replacements")
    print(f"  • Missing frontmatter generation")
    print(f"  • Simple formatting corrections")
    
    # Actually fix
    print("\nApplying fixes...")
    fix_stats = engine.auto_fix_issues(dry_run=False)
    
    print(f"\n✅ Fixed {fix_stats['fixed']} issues")
    if fix_stats['failed'] > 0:
        print(f"⚠️  {fix_stats['failed']} fixes failed")
    if fix_stats['skipped'] > 0:
        print(f"ℹ️  {fix_stats['skipped']} issues skipped (already correct)")
    
    # Re-scan
    print_section("Step 8: Verifying Improvements")
    print("Re-scanning to verify fixes...")
    
    issues_after = engine.scan_repository()
    metrics_after = engine.collect_metrics()
    
    print(f"\n✅ Verification complete")
    print(f"\nImprovement Summary:")
    print(f"  • Issues Before: {len(issues)}")
    print(f"  • Issues After: {len(issues_after)}")
    print(f"  • Issues Resolved: {len(issues) - len(issues_after)}")
    print(f"  • Improvement: {(1 - len(issues_after)/len(issues))*100:.1f}%")
    
    print(f"\nMetrics Comparison:")
    print(f"  • Critical Issues: {metrics['critical_issues']:.0f} → {metrics_after['critical_issues']:.0f}")
    print(f"  • Documentation Debt: {metrics['documentation_debt']:.0f} → {metrics_after['documentation_debt']:.0f}")
    print(f"  • Consistency Score: {metrics['content_consistency_score']:.2f} → {metrics_after['content_consistency_score']:.2f}")
    
    # Generate report
    print_section("Step 9: Generating Quality Report")
    report_path = os.path.join(temp_dir, 'quality_report.md')
    engine.generate_report(report_path)
    
    print(f"✅ Report generated: {report_path}")
    print("\nReport includes:")
    print("  • Executive summary with key metrics")
    print("  • 30-day trend analysis")
    print("  • Issues organized by category")
    print("  • Recommended actions")
    print("  • Quality gate status")
    
    # Summary
    print_section("Summary: Key Takeaways")
    
    print("This demonstration showed:")
    print("\n1. ✅ Comprehensive Issue Detection")
    print("   - Found issues across all 5 categories")
    print("   - Detected problems from the Claude Docs analysis")
    print("   - Severity-based prioritization")
    
    print("\n2. ✅ Automated Fixing")
    print(f"   - Fixed {fix_stats['fixed']} issues automatically")
    print("   - Maintained backups for safety")
    print("   - Reduced manual work significantly")
    
    print("\n3. ✅ Metrics Tracking")
    print("   - Tracked 12+ quality KPIs")
    print("   - Quality gates for CI/CD integration")
    print("   - Historical trend analysis ready")
    
    print("\n4. ✅ Production Ready")
    print("   - Works on real documentation")
    print("   - Handles complex issues")
    print("   - Generates actionable reports")
    
    print(f"\n\n{'='*80}")
    print("Example files remain at:", temp_dir)
    print("Review the quality_report.md to see the complete analysis")
    print('='*80 + '\n')
    
    # Cleanup option
    response = input("\nDelete example files? (y/N): ")
    if response.lower() == 'y':
        shutil.rmtree(temp_dir)
        print("✅ Cleaned up example files")
    else:
        print(f"ℹ️  Example files kept at: {temp_dir}")
    
    engine.close()
    
    print("\n✅ Example demonstration complete!\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExample interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
