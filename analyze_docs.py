#!/usr/bin/env python3
"""
Unified CLI entry point for documentation analysis and fixing.
Runs both doc_analyzer.py and doc_fixer.py sequentially with a single command.

Usage:
    python analyze_docs.py /path/to/docs [options]

This will:
1. Run doc_analyzer.py to analyze the documentation
2. Run doc_fixer.py to generate fix suggestions
3. Generate all 6 reports (analysis + fixes in .html, .md, .json formats)
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

def run_command(command: list, description: str, timeout: int = 1800) -> tuple[bool, str]:
    """
    Run a command with real-time output streaming and timeout.

    Args:
        command: Command and arguments as list
        description: Description of what's being run
        timeout: Maximum seconds to wait (default: 1800 = 30 minutes)

    Returns:
        Tuple of (success: bool, output: str)
    """
    print(f"\n{'='*70}")
    print(f"📊 {description}")
    print(f"{'='*70}")

    output_lines = []

    try:
        # Use Popen for real-time output streaming
        # Add PYTHONUNBUFFERED to ensure Python scripts output in real-time
        env = os.environ.copy()
        env['PYTHONUNBUFFERED'] = '1'

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Combine stderr with stdout
            text=True,
            bufsize=1,  # Line buffered
            env=env
        )

        # Read output in real-time
        start_time = datetime.now()
        while True:
            # Check timeout
            if (datetime.now() - start_time).total_seconds() > timeout:
                process.kill()
                error_msg = f"Command timed out after {timeout} seconds"
                print(f"\n❌ {error_msg}", file=sys.stderr)
                return False, error_msg

            # Read a line
            line = process.stdout.readline()
            if not line:
                # Check if process has finished
                if process.poll() is not None:
                    break
                continue

            # Print the line in real-time and save it
            print(line.rstrip())
            output_lines.append(line)

        # Get final return code
        returncode = process.poll()

        # Join all output lines
        full_output = ''.join(output_lines)

        return returncode == 0, full_output

    except Exception as e:
        error_msg = f"Failed to run {command[0]}: {str(e)}"
        print(f"❌ {error_msg}", file=sys.stderr)
        return False, error_msg

def main():
    parser = argparse.ArgumentParser(
        description='Unified documentation analyzer and fixer - analyzes .mdx files and generates comprehensive reports',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze docs and generate all report formats
  python analyze_docs.py /path/to/docs --format all

  # Analyze with specific configuration
  python analyze_docs.py /path/to/docs --config custom_config.yaml

  # Analyze without AI features
  python analyze_docs.py /path/to/docs --no-ai

  # Analyze and apply fixes (not just preview)
  python analyze_docs.py /path/to/docs --apply-fixes

  # Analyze remote repository
  python analyze_docs.py --repo-url https://github.com/user/docs --repo-type mintlify
        """
    )

    # Path arguments
    parser.add_argument('docs_path', nargs='?', type=str,
                       help='Path to the documentation directory (analyzes .mdx files)')

    # Repository arguments
    parser.add_argument('--repo-url', type=str,
                       help='URL of the git repository to analyze')
    parser.add_argument('--repo-type', type=str,
                       choices=['mintlify', 'docusaurus', 'mkdocs', 'generic', 'auto'],
                       default='auto',
                       help='Type of documentation repository (default: auto-detect)')
    parser.add_argument('--repo-root', type=str,
                       help='Repository root for platform detection (auto-detected if not specified)')

    # Output arguments
    parser.add_argument('--format', type=str,
                       choices=['json', 'html', 'markdown', 'all'],
                       default='all',
                       help='Output format for reports (default: all)')
    parser.add_argument('--output', type=str,
                       help='Custom output path for reports (default: timestamped directory)')

    # Configuration arguments
    parser.add_argument('--config', type=str,
                       help='Path to configuration file')
    parser.add_argument('--no-ai', action='store_true',
                       help='Disable AI-powered analysis features')

    # Fix-specific arguments
    parser.add_argument('--apply-fixes', action='store_true',
                       help='Apply fixes to files instead of dry-run preview')
    parser.add_argument('--auto-approve', action='store_true',
                       help='Skip confirmation prompts when applying fixes')

    # Analysis control arguments
    parser.add_argument('--skip-analysis', action='store_true',
                       help='Skip analysis phase, only run fixer')
    parser.add_argument('--skip-fixes', action='store_true',
                       help='Skip fix generation phase, only run analysis')

    args = parser.parse_args()

    # Validate arguments
    if not args.docs_path and not args.repo_url:
        parser.error("Either docs_path or --repo-url must be provided")

    if args.skip_analysis and args.skip_fixes:
        parser.error("Cannot skip both analysis and fixes")

    # Track overall success
    overall_success = True

    # Create shared timestamped directory for all reports if no custom output specified
    if not args.output:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        shared_output_dir = Path('reports') / timestamp
        shared_output_dir.mkdir(parents=True, exist_ok=True)
        print(f"📁 Created shared report directory: {shared_output_dir}")
    else:
        shared_output_dir = Path(args.output)
        shared_output_dir.mkdir(parents=True, exist_ok=True)

    # Build base command arguments that both scripts share
    base_args = []

    if args.docs_path:
        base_args.append(args.docs_path)
    if args.repo_url:
        base_args.extend(['--repo-url', args.repo_url])
    if args.repo_type and args.repo_type != 'auto':
        base_args.extend(['--repo-type', args.repo_type])
    if args.repo_root:
        base_args.extend(['--repo-root', args.repo_root])
    if args.config:
        base_args.extend(['--config', args.config])
    if args.format:
        base_args.extend(['--format', args.format])
    # Always pass the shared output directory to both scripts
    base_args.extend(['--output', str(shared_output_dir)])
    if args.no_ai:
        base_args.append('--no-ai')

    print(f"\n{'='*70}")
    print(f"🚀 UNIFIED DOCUMENTATION ANALYZER & FIXER")
    print(f"{'='*70}")
    print(f"📁 Target: {args.docs_path or args.repo_url}")
    print(f"📝 Format: {args.format}")
    print(f"🤖 AI Analysis: {'Disabled' if args.no_ai else 'Enabled'}")
    print(f"🔧 Fix Mode: {'Apply' if args.apply_fixes else 'Preview (dry-run)'}")
    print(f"{'='*70}")

    # Run analysis phase
    if not args.skip_analysis:
        analyzer_cmd = [sys.executable, 'doc_analyzer.py'] + base_args
        success, output = run_command(analyzer_cmd, "Running Documentation Analysis")

        if not success:
            print("\n❌ Analysis phase failed!", file=sys.stderr)
            overall_success = False
            if not args.skip_fixes:
                print("⚠️  Continuing with fix generation despite analysis errors...", file=sys.stderr)
    else:
        print("\n⏭️  Skipping analysis phase (--skip-analysis flag)")

    # Run fixer phase
    if not args.skip_fixes:
        # Build fixer-specific arguments (doc_fixer.py has different args)
        fixer_cmd = [sys.executable, 'doc_fixer.py']

        # Add path argument (required positional for fixer)
        if args.docs_path:
            fixer_cmd.append(args.docs_path)
        elif args.repo_url:
            # For remote repos, we need to use the local clone path
            # The analyzer would have cloned it, so we can just use the repo name
            import re
            repo_name = re.sub(r'\.git$', '', args.repo_url.split('/')[-1])
            fixer_cmd.append(f'./temp/{repo_name}')

        # Add configuration file if specified
        if args.config:
            fixer_cmd.extend(['--config', args.config])

        # Add format and output arguments (IMPORTANT: fixer needs same output dir)
        if args.format:
            fixer_cmd.extend(['--format', args.format])
        fixer_cmd.extend(['--output', str(shared_output_dir)])

        # Add fix-specific arguments
        if not args.apply_fixes:
            fixer_cmd.append('--dry-run')  # Default is dry-run

        # Pass --no-ai flag to fixer if set (disables slow StyleGuideValidator)
        if args.no_ai:
            fixer_cmd.append('--no-ai')

        success, output = run_command(fixer_cmd, "Running Documentation Fixer")

        if not success:
            print("\n❌ Fixer phase failed!", file=sys.stderr)
            overall_success = False
    else:
        print("\n⏭️  Skipping fix generation phase (--skip-fixes flag)")

    # Summary
    print(f"\n{'='*70}")
    if overall_success:
        print("✅ DOCUMENTATION ANALYSIS & FIX GENERATION COMPLETE!")
        print("\n📊 Reports Generated:")
        if not args.skip_analysis:
            print("  • Analysis Reports: .html, .md, .json")
        if not args.skip_fixes:
            print("  • Fix Suggestion Reports: .html, .md, .json")
        print(f"\n📁 Check the reports/ directory for timestamped results")
    else:
        print("⚠️  COMPLETED WITH ERRORS")
        print("\nSome phases encountered errors. Check the output above for details.")
    print(f"{'='*70}\n")

    # Exit with appropriate code
    sys.exit(0 if overall_success else 1)

if __name__ == "__main__":
    main()