#!/usr/bin/env python3
"""
Documentation Fixer - Automated fixing tool for documentation quality issues

Automatically fixes common documentation issues found by doc_analyzer:
- Missing or incomplete frontmatter
- Deprecated terminology
- Improper capitalization
- Absolute URLs that should be relative

Usage:
    python doc_fixer.py <docs_directory> [--dry-run] [--backup]
"""

import argparse
import sys
from pathlib import Path
from typing import List
import shutil
from datetime import datetime

from core.config import Config
from core.models import FixResult, FixerStats
from fixers import (
    FrontmatterFixer,
    TerminologyFixer,
    URLFixer,
    CodeBlockFixer,
    GitHubInformedFixer,
    StyleGuideValidationFixer,
    # High-impact fixers
    CodeLanguageTagFixer,
    HeadingHierarchyFixer,
    LinkTextImprover,
    LongSentenceSplitter,
    PassiveVoiceConverter,
    MissingPrerequisitesDetector,
    # Style consistency fixers
    CapitalizationFixer,
    TerminologyConsistencyFixer,
    CalloutStandardizationFixer,
    BrokenLinkDetector,
    ProductionCodeValidator,
)
import os


class DocFixer:
    """Main documentation fixer orchestrator"""

    def __init__(self, config_path: Path = None, enable_style_guide: bool = True):
        """
        Initialize the fixer with configuration

        Args:
            config_path: Optional path to config file
            enable_style_guide: Enable style guide validation (default: True for testing)
                               Can be disabled via ENABLE_STYLE_GUIDE_VALIDATOR=false env var
        """
        self.config = Config(config_path) if config_path else Config()

        # Check environment variable for style guide validator toggle
        env_enable = os.getenv('ENABLE_STYLE_GUIDE_VALIDATOR', 'true').lower()
        if env_enable in ['false', '0', 'no']:
            enable_style_guide = False

        # Initialize core fixers (always enabled)
        self.fixers = [
            FrontmatterFixer(self.config),
            TerminologyFixer(self.config),
            URLFixer(self.config),
            CodeBlockFixer(self.config),
            GitHubInformedFixer(self.config)  # GitHub user-informed quality checks
        ]

        # Add style guide validator if enabled (uses Claude AI API)
        if enable_style_guide:
            try:
                self.fixers.append(StyleGuideValidationFixer(self.config))
                print("✓ Style Guide Validator enabled (with Claude AI analysis)")
            except Exception as e:
                print(f"⚠ Warning: Could not enable Style Guide Validator: {e}")

        # High-impact fixers (toggleable via environment variables)
        if os.getenv('ENABLE_CODE_LANGUAGE_FIXER', 'true').lower() not in ['false', '0', 'no']:
            self.fixers.append(CodeLanguageTagFixer(self.config))
            print("✓ Code Language Tag Fixer enabled")

        if os.getenv('ENABLE_HEADING_HIERARCHY_FIXER', 'true').lower() not in ['false', '0', 'no']:
            self.fixers.append(HeadingHierarchyFixer(self.config))
            print("✓ Heading Hierarchy Fixer enabled")

        if os.getenv('ENABLE_LINK_TEXT_IMPROVER', 'false').lower() not in ['false', '0', 'no']:
            self.fixers.append(LinkTextImprover(self.config))
            print("✓ Link Text Improver enabled (manual fix required)")

        if os.getenv('ENABLE_LONG_SENTENCE_SPLITTER', 'false').lower() not in ['false', '0', 'no']:
            self.fixers.append(LongSentenceSplitter(self.config))
            print("✓ Long Sentence Splitter enabled")

        if os.getenv('ENABLE_PASSIVE_VOICE_CONVERTER', 'false').lower() not in ['false', '0', 'no']:
            self.fixers.append(PassiveVoiceConverter(self.config))
            print("✓ Passive Voice Converter enabled (manual fix required)")

        if os.getenv('ENABLE_MISSING_PREREQUISITES_DETECTOR', 'false').lower() not in ['false', '0', 'no']:
            self.fixers.append(MissingPrerequisitesDetector(self.config))
            print("✓ Missing Prerequisites Detector enabled (manual fix required)")

        # Style consistency fixers (toggleable via environment variables)
        if os.getenv('ENABLE_CAPITALIZATION_FIXER', 'true').lower() not in ['false', '0', 'no']:
            self.fixers.append(CapitalizationFixer(self.config))
            print("✓ Capitalization Fixer enabled")

        if os.getenv('ENABLE_TERMINOLOGY_CONSISTENCY_FIXER', 'false').lower() not in ['false', '0', 'no']:
            self.fixers.append(TerminologyConsistencyFixer(self.config))
            print("✓ Terminology Consistency Fixer enabled")

        if os.getenv('ENABLE_CALLOUT_STANDARDIZATION_FIXER', 'false').lower() not in ['false', '0', 'no']:
            self.fixers.append(CalloutStandardizationFixer(self.config))
            print("✓ Callout Standardization Fixer enabled")

        if os.getenv('ENABLE_BROKEN_LINK_DETECTOR', 'false').lower() not in ['false', '0', 'no']:
            self.fixers.append(BrokenLinkDetector(self.config))
            print("✓ Broken Link Detector enabled (manual fix required)")

        if os.getenv('ENABLE_PRODUCTION_CODE_VALIDATOR', 'false').lower() not in ['false', '0', 'no']:
            self.fixers.append(ProductionCodeValidator(self.config))
            print("✓ Production Code Validator enabled (manual fix required)")

        self.stats = FixerStats()

    def process_directory(self, docs_path: Path, dry_run: bool = False, backup: bool = True) -> FixerStats:
        """
        Process all markdown/mdx files in directory

        Args:
            docs_path: Path to documentation directory
            dry_run: If True, don't write changes to disk
            backup: If True, create backups before modifying

        Returns:
            FixerStats with summary of changes
        """
        # Find all MDX and MD files
        md_files = list(docs_path.rglob("*.md")) + list(docs_path.rglob("*.mdx"))

        print(f"\n{'='*70}")
        print(f"Documentation Fixer")
        print(f"{'='*70}")
        print(f"Target directory: {docs_path}")
        print(f"Files found: {len(md_files)}")
        print(f"Mode: {'DRY RUN' if dry_run else 'LIVE'}")
        print(f"Backup: {'Enabled' if backup else 'Disabled'}")
        print(f"{'='*70}\n")

        for file_path in md_files:
            # Make file path relative to docs_path for display
            relative_path = file_path.relative_to(docs_path)

            print(f"Processing: {relative_path}")

            # Apply all fixers to this file
            combined_result = self._process_file(file_path)

            # Record stats
            self.stats.add_result(combined_result)

            # Write changes if not dry run
            if not dry_run and combined_result.content_changed:
                if backup:
                    self._create_backup(file_path)

                # Write fixed content
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(combined_result.fixed_content)

            # Print summary for this file
            if combined_result.content_changed:
                for fix in combined_result.fixes_applied:
                    print(f"  ✓ {fix}")
            else:
                print(f"  ✓ No changes needed")

            print()

        return self.stats

    def _process_file(self, file_path: Path) -> FixResult:
        """
        Apply all fixers to a single file

        Args:
            file_path: Path to file to process

        Returns:
            Combined FixResult
        """
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()

            current_content = original_content
            all_fixes = []
            all_issues_fixed = []

            # Apply each fixer in sequence
            for fixer in self.fixers:
                # Check for issues
                issues = fixer.check_file(str(file_path), current_content)

                # Filter to auto-fixable issues only
                auto_fixable = [i for i in issues if i.auto_fixable]

                if auto_fixable:
                    # Apply fixes
                    result = fixer.fix(str(file_path), current_content, auto_fixable)

                    if result.content_changed:
                        current_content = result.fixed_content
                        all_fixes.extend(result.fixes_applied)
                        all_issues_fixed.extend(result.issues_fixed)

            return FixResult(
                file_path=str(file_path),
                original_content=original_content,
                fixed_content=current_content,
                fixes_applied=all_fixes,
                issues_fixed=all_issues_fixed
            )

        except Exception as e:
            return FixResult(
                file_path=str(file_path),
                original_content="",
                fixed_content="",
                error=str(e)
            )

    def _create_backup(self, file_path: Path):
        """Create a backup of the file"""
        backup_dir = file_path.parent / ".doc_fixer_backups"
        backup_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"{file_path.name}.{timestamp}.bak"

        shutil.copy2(file_path, backup_path)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Automatically fix documentation quality issues",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run (preview changes without applying)
  python doc_fixer.py ./docs --dry-run

  # Apply fixes with backups (default)
  python doc_fixer.py ./docs

  # Apply fixes without backups
  python doc_fixer.py ./docs --no-backup

  # Use custom config file
  python doc_fixer.py ./docs --config custom_config.yaml
        """
    )

    parser.add_argument(
        'docs_directory',
        type=Path,
        help='Path to documentation directory'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without applying them'
    )

    parser.add_argument(
        '--no-backup',
        action='store_true',
        help='Do not create backup files'
    )

    parser.add_argument(
        '--config',
        type=Path,
        help='Path to custom config.yaml file'
    )

    args = parser.parse_args()

    # Validate docs directory
    if not args.docs_directory.exists():
        print(f"Error: Directory not found: {args.docs_directory}", file=sys.stderr)
        sys.exit(1)

    if not args.docs_directory.is_dir():
        print(f"Error: Not a directory: {args.docs_directory}", file=sys.stderr)
        sys.exit(1)

    # Initialize fixer
    try:
        fixer = DocFixer(config_path=args.config)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Process directory
    stats = fixer.process_directory(
        docs_path=args.docs_directory,
        dry_run=args.dry_run,
        backup=not args.no_backup
    )

    # Print final summary
    print(stats.summary())

    # Exit with appropriate code
    if stats.errors:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
