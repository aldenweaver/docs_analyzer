#!/usr/bin/env python3
"""
Cost estimator for AI-powered documentation analysis
Helps avoid budget surprises by estimating API costs before running
"""
import os
import sys
from pathlib import Path
from typing import List, Tuple

# Claude API Pricing (as of Jan 2025)
# https://www.anthropic.com/pricing
PRICING = {
    'claude-3-5-haiku-20241022': {
        'input': 0.80 / 1_000_000,   # $0.80 per million input tokens
        'output': 4.00 / 1_000_000,  # $4 per million output tokens
    },
    'claude-sonnet-4-5-20250929': {
        'input': 3.00 / 1_000_000,   # $3 per million input tokens
        'output': 15.00 / 1_000_000,  # $15 per million output tokens
    },
    'claude-3-5-sonnet-20241022': {
        'input': 3.00 / 1_000_000,
        'output': 15.00 / 1_000_000,
    },
    'claude-opus-4-20250514': {
        'input': 15.00 / 1_000_000,
        'output': 75.00 / 1_000_000,
    }
}

def count_tokens_estimate(text: str) -> int:
    """Rough token estimation: ~4 chars per token for English"""
    return len(text) // 4

def find_doc_files(path: str, patterns: List[str] = None) -> List[Path]:
    """Find all documentation files"""
    if patterns is None:
        patterns = ['**/*.md', '**/*.mdx']

    doc_path = Path(path)
    files = []
    for pattern in patterns:
        files.extend(doc_path.glob(pattern))

    return sorted(files)

def analyze_file_sizes(files: List[Path]) -> dict:
    """Analyze file sizes and estimate tokens"""
    total_chars = 0
    file_data = []

    for file_path in files:
        try:
            content = file_path.read_text(encoding='utf-8')
            chars = len(content)
            tokens = count_tokens_estimate(content)
            total_chars += chars
            file_data.append({
                'path': str(file_path),
                'chars': chars,
                'tokens': tokens
            })
        except Exception as e:
            print(f"Warning: Could not read {file_path}: {e}")

    return {
        'files': file_data,
        'total_chars': total_chars,
        'total_tokens': count_tokens_estimate(str(total_chars))
    }

def estimate_ai_cost(num_files: int, avg_file_tokens: int, model: str, max_tokens: int = 2000) -> dict:
    """
    Estimate API cost for analysis

    The analyzer does two types of AI analysis:
    1. Per-file clarity analysis (first 200 lines of each file)
    2. One semantic gap analysis across all files (summary of all files)
    """
    if model not in PRICING:
        print(f"Warning: Unknown model {model}, using Sonnet pricing")
        model = 'claude-sonnet-4-5-20250929'

    pricing = PRICING[model]

    # Per-file clarity analysis (samples first 200 lines ≈ 40% of avg file)
    sample_ratio = 0.4  # Conservative estimate
    input_per_file = int(avg_file_tokens * sample_ratio) + 150  # +150 for prompt
    output_per_file = 500  # Typical output for clarity issues

    clarity_input_tokens = num_files * input_per_file
    clarity_output_tokens = num_files * output_per_file

    # Semantic gap analysis (one request with summary of all files)
    gap_input_tokens = 1000 + (num_files * 100)  # Prompt + file summaries
    gap_output_tokens = max_tokens  # Full output

    # Total tokens
    total_input = clarity_input_tokens + gap_input_tokens
    total_output = clarity_output_tokens + gap_output_tokens

    # Calculate costs
    input_cost = total_input * pricing['input']
    output_cost = total_output * pricing['output']
    total_cost = input_cost + output_cost

    return {
        'model': model,
        'num_files': num_files,
        'total_input_tokens': total_input,
        'total_output_tokens': total_output,
        'input_cost': input_cost,
        'output_cost': output_cost,
        'total_cost': total_cost,
        'cost_per_file': total_cost / num_files if num_files > 0 else 0
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python estimate_cost.py <docs_path> [--model MODEL]")
        print("\nExample:")
        print("  python estimate_cost.py /path/to/docs")
        print("  python estimate_cost.py /path/to/docs --model claude-opus-4-20250514")
        sys.exit(1)

    docs_path = sys.argv[1]
    model = 'claude-sonnet-4-5-20250929'

    # Parse model argument
    if '--model' in sys.argv:
        model_idx = sys.argv.index('--model')
        if model_idx + 1 < len(sys.argv):
            model = sys.argv[model_idx + 1]

    print("=" * 70)
    print("📊 AI Analysis Cost Estimator")
    print("=" * 70)

    # Find files
    print(f"\n🔍 Scanning: {docs_path}")
    files = find_doc_files(docs_path)

    if not files:
        print("❌ No documentation files found!")
        sys.exit(1)

    print(f"✅ Found {len(files)} documentation files")

    # Analyze file sizes
    print("\n📏 Analyzing file sizes...")
    file_stats = analyze_file_sizes(files)
    avg_tokens = file_stats['total_tokens'] // len(files) if files else 0

    print(f"   Total characters: {file_stats['total_chars']:,}")
    print(f"   Estimated total tokens: {file_stats['total_tokens']:,}")
    print(f"   Average tokens per file: {avg_tokens:,}")

    # Show largest files
    sorted_files = sorted(file_stats['files'], key=lambda x: x['tokens'], reverse=True)
    print(f"\n📄 Largest files (top 5):")
    for i, f in enumerate(sorted_files[:5], 1):
        print(f"   {i}. {Path(f['path']).name}: ~{f['tokens']:,} tokens")

    # Cost estimates for different scenarios
    print("\n" + "=" * 70)
    print("💰 Cost Estimates by Model")
    print("=" * 70)

    for model_name, pricing in PRICING.items():
        estimate = estimate_ai_cost(len(files), avg_tokens, model_name)
        print(f"\n{model_name}:")
        print(f"   Input:  {estimate['total_input_tokens']:,} tokens × ${pricing['input']*1_000_000:.2f}/M = ${estimate['input_cost']:.4f}")
        print(f"   Output: {estimate['total_output_tokens']:,} tokens × ${pricing['output']*1_000_000:.2f}/M = ${estimate['output_cost']:.4f}")
        print(f"   Total:  ${estimate['total_cost']:.4f}")
        print(f"   Per file: ${estimate['cost_per_file']:.4f}")

    # Testing recommendations
    print("\n" + "=" * 70)
    print("💡 Smart Testing Recommendations")
    print("=" * 70)

    default_estimate = estimate_ai_cost(len(files), avg_tokens, 'claude-sonnet-4-5-20250929')

    print(f"\n📊 Your Budget: $5.00")
    print(f"📊 Full Analysis Cost: ${default_estimate['total_cost']:.2f}")

    if default_estimate['total_cost'] > 5.00:
        print("\n⚠️  WARNING: Full analysis exceeds your $5 budget!")

        # Calculate how many files fit in budget
        files_in_budget = int(5.00 / default_estimate['cost_per_file'])
        print(f"\n🎯 Recommended Testing Strategy:")
        print(f"   1. Start with {min(5, len(files))} files (cost: ~${min(5, len(files)) * default_estimate['cost_per_file']:.2f})")
        print(f"   2. Review results and adjust")
        print(f"   3. You can analyze up to ~{files_in_budget} files within budget")
        print(f"\n💡 To limit files, use a subfolder or create a test subset")

    else:
        print(f"\n✅ Full analysis fits within budget!")
        print(f"   Estimated cost: ${default_estimate['total_cost']:.2f}")
        print(f"   Remaining budget: ${5.00 - default_estimate['total_cost']:.2f}")

    print("\n Cost-Saving Tips:")
    print("   • Analyze subfolders first (e.g., just /pages)")
    print("   • Use --no-ai flag for free structural analysis")
    print("   • Run AI analysis only on final review")
    print("   • Test with 5-10 files first to validate setup")

    print("\n🧪 Testing Commands:")
    print(f"   # Free structural analysis (no AI)")
    print(f"   python doc_analyzer.py {docs_path} --no-ai --format html")
    print(f"\n   # Test AI with small subset (est: ${min(5, len(files)) * default_estimate['cost_per_file']:.2f})")
    if len(files) > 5:
        sample_dir = Path(sorted_files[0]['path']).parent
        print(f"   python doc_analyzer.py {sample_dir} --format html")
    else:
        print(f"   python doc_analyzer.py {docs_path} --format html")

    print("\n" + "=" * 70)

if __name__ == '__main__':
    main()
