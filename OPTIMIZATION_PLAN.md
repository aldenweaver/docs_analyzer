# Performance Optimization Plan

## Current Performance Bottlenecks

### Analysis of Current Implementation

**Timing Breakdown (100 file documentation set):**
```
Without AI:
- File I/O and parsing: ~5-10 seconds
- Quality checks (sequential): ~20-30 seconds
- Report generation: ~5 seconds
Total: ~30-45 seconds

With AI:
- File I/O and parsing: ~5-10 seconds
- Quality checks (sequential): ~20-30 seconds
- AI API calls (sequential): ~25-45 minutes (!) ← BOTTLENECK
- Report generation: ~5 seconds
Total: ~30-60 minutes
```

**Identified Bottlenecks:**
1. **AI API Calls (95% of time with AI enabled)**
   - Sequential execution (one file at a time)
   - 2-5 second latency per API call
   - 100 files = 200-500 seconds minimum
   - Rate limiting adds delays between calls

2. **Sequential File Processing**
   - Files processed one at a time
   - No parallelization of I/O or analysis
   - CPU cores underutilized

3. **No Incremental Analysis**
   - Full re-analysis every run
   - No caching of previous results
   - No "only changed files" mode

4. **Memory Inefficient**
   - All results held in memory
   - Large documentation sets can cause memory pressure

---

## Optimization Strategy

### Phase 1: Quick Wins (Low Effort, High Impact)

#### 1.1 Parallel File Processing
**Impact:** 3-5x faster for non-AI checks
**Effort:** Medium
**Implementation:**

```python
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import multiprocessing

def process_file_parallel(file_path, analyzers):
    """Process a single file with all analyzers"""
    issues = []
    for analyzer in analyzers:
        issues.extend(analyzer.analyze(file_path))
    return file_path, issues

def analyze_directory_parallel(files, analyzers, max_workers=None):
    """Analyze files in parallel using process pool"""
    if max_workers is None:
        max_workers = min(multiprocessing.cpu_count(), len(files))

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(
            lambda f: process_file_parallel(f, analyzers),
            files
        ))

    return dict(results)
```

**Benefits:**
- 4-8 CPU cores utilized simultaneously
- File I/O and parsing parallelized
- Non-AI checks run in parallel
- Near-linear scaling up to CPU core count

**Limitations:**
- AI API calls still sequential (API rate limits)
- Requires careful state management

---

#### 1.2 Batch API Requests
**Impact:** 2-3x faster for AI analysis
**Effort:** Medium
**Implementation:**

```python
def analyze_clarity_batch(self, file_contents: dict[str, str], issues: dict[str, list]):
    """Analyze multiple files in a single API call"""

    # Combine multiple files into one prompt
    batch_prompt = "Analyze these documentation files for clarity issues:\n\n"

    for file_path, content in file_contents.items():
        batch_prompt += f"\n--- File: {file_path} ---\n{content[:1000]}\n"

    batch_prompt += "\nReturn JSON array with file_path field for each issue."

    # Single API call for multiple files
    response = self.claude_client.messages.create(
        model=self.model,
        max_tokens=self.max_tokens * len(file_contents),  # Scale tokens
        messages=[{"role": "user", "content": batch_prompt}]
    )

    # Parse and distribute issues to correct files
    ai_issues = json.loads(response.content[0].text)
    for issue in ai_issues:
        file_path = issue['file_path']
        issues[file_path].append(Issue(...))
```

**Benefits:**
- Fewer API calls (10-20 files per call)
- Reduced network overhead
- Better token utilization
- Amortized rate limiting delays

**Considerations:**
- Max token limits per request
- More complex error handling
- Need to track which file each issue belongs to

---

#### 1.3 Incremental Analysis (Git-Aware)
**Impact:** 10-100x faster for incremental changes
**Effort:** Medium
**Implementation:**

```python
import hashlib
import json
from pathlib import Path

class ResultsCache:
    """Cache analysis results with content hashing"""

    def __init__(self, cache_dir=".docs_analyzer_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def get_file_hash(self, file_path: Path) -> str:
        """Get SHA-256 hash of file content"""
        content = file_path.read_bytes()
        return hashlib.sha256(content).hexdigest()

    def get_cached_result(self, file_path: Path, file_hash: str):
        """Retrieve cached analysis if file unchanged"""
        cache_file = self.cache_dir / f"{file_hash}.json"
        if cache_file.exists():
            return json.loads(cache_file.read_text())
        return None

    def save_result(self, file_path: Path, file_hash: str, issues: list):
        """Cache analysis result"""
        cache_file = self.cache_dir / f"{file_hash}.json"
        cache_file.write_text(json.dumps(issues))

def analyze_with_cache(docs_path: Path, force_refresh=False):
    """Only analyze changed files"""
    cache = ResultsCache()
    all_issues = {}

    for file_path in docs_path.rglob("*.mdx"):
        file_hash = cache.get_file_hash(file_path)

        if not force_refresh:
            cached = cache.get_cached_result(file_path, file_hash)
            if cached:
                print(f"✓ Using cached result for {file_path}")
                all_issues[file_path] = cached
                continue

        # File changed or not cached - analyze it
        print(f"⚙ Analyzing {file_path}")
        issues = analyze_file(file_path)
        cache.save_result(file_path, file_hash, issues)
        all_issues[file_path] = issues

    return all_issues
```

**Benefits:**
- Only analyze changed files (huge speedup for PRs)
- Content-addressable caching (not time-based)
- Works across git branches
- Immediate results for unchanged files

**Use Cases:**
- CI/CD: Only check changed files in PR
- Development: Quick iterations
- Large doc sets: Initial run slow, subsequent runs fast

---

### Phase 2: Advanced Optimizations (Higher Effort)

#### 2.1 Async I/O and API Calls
**Impact:** 2-3x faster overall
**Effort:** High
**Implementation:**

```python
import asyncio
import aiofiles
from anthropic import AsyncAnthropic

async def analyze_file_async(file_path: Path, analyzers: list):
    """Async file analysis"""
    async with aiofiles.open(file_path, 'r') as f:
        content = await f.read()

    issues = []
    # Run non-blocking analysis
    for analyzer in analyzers:
        if analyzer.is_async:
            issues.extend(await analyzer.analyze_async(content))
        else:
            issues.extend(analyzer.analyze(content))

    return file_path, issues

async def analyze_directory_async(files: list, analyzers: list):
    """Analyze all files concurrently"""
    tasks = [analyze_file_async(f, analyzers) for f in files]
    results = await asyncio.gather(*tasks)
    return dict(results)
```

**Benefits:**
- True concurrent I/O
- Multiple API calls in flight
- Better resource utilization
- Scales well with I/O-bound operations

---

#### 2.2 Smart Sampling for Large Doc Sets
**Impact:** 5-10x faster for huge repositories
**Effort:** Medium
**Implementation:**

```python
def sample_documentation(files: list, sample_rate=0.2, always_include=None):
    """Intelligently sample files for large doc sets"""

    always_include = always_include or [
        '**/index.mdx',
        '**/getting-started.mdx',
        '**/README.mdx'
    ]

    # Always analyze critical files
    critical = [f for f in files if any(f.match(pattern) for pattern in always_include)]

    # Sample remaining files
    remaining = [f for f in files if f not in critical]
    sample_size = int(len(remaining) * sample_rate)
    sampled = random.sample(remaining, sample_size)

    return critical + sampled

def analyze_with_sampling(docs_path: Path, sample_rate=0.2):
    """Quick quality check via sampling"""
    all_files = list(docs_path.rglob("*.mdx"))
    files_to_analyze = sample_documentation(all_files, sample_rate)

    print(f"Analyzing {len(files_to_analyze)}/{len(all_files)} files ({sample_rate*100}% sample)")

    # Analyze sample and extrapolate
    issues = analyze_files(files_to_analyze)
    projected_total = len(issues) / sample_rate

    return issues, projected_total
```

**Benefits:**
- Quick quality estimates for large repos
- Representative sampling algorithm
- Always check critical files
- Good for initial assessment

---

#### 2.3 Profile-Guided Optimization
**Implementation:**

```python
import cProfile
import pstats

def profile_analysis():
    """Profile the analyzer to find bottlenecks"""
    profiler = cProfile.Profile()
    profiler.enable()

    # Run analysis
    analyze_documentation('/path/to/docs')

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)  # Top 20 slowest functions
```

**Focus Areas:**
- Identify slow regex patterns
- Find redundant file reads
- Optimize hot loops
- Reduce memory allocations

---

## Implementation Roadmap

### Immediate (Week 1)
- [ ] Add `--parallel` flag for parallel file processing
- [ ] Implement basic results caching
- [ ] Add `--changed-only` flag for git-aware analysis

### Short-term (Month 1)
- [ ] Batch API requests (5-10 files per call)
- [ ] Add `--sample` flag with intelligent sampling
- [ ] Profile and optimize hot paths

### Long-term (Quarter 1)
- [ ] Full async/await implementation
- [ ] Distributed analysis for massive doc sets
- [ ] ML-based issue prediction (skip clean files)

---

## Performance Targets

**Current State:**
- 100 files without AI: ~45 seconds
- 100 files with AI: ~30 minutes

**After Phase 1 Optimizations:**
- 100 files without AI: ~10 seconds (4.5x faster)
- 100 files with AI: ~8 minutes (3.75x faster)

**After Phase 2 Optimizations:**
- 100 files without AI: ~5 seconds (9x faster)
- 100 files with AI: ~3 minutes (10x faster)

**With Incremental Analysis:**
- Changed files only: ~2-5 seconds (100x faster)

---

## Command-Line Interface Additions

```bash
# Parallel processing (use all CPU cores)
python analyze_docs.py /path/to/docs --parallel --workers 8

# Incremental analysis (only changed files)
python analyze_docs.py /path/to/docs --changed-only

# Force refresh cache
python analyze_docs.py /path/to/docs --no-cache

# Quick sampling for large repos
python analyze_docs.py /path/to/docs --sample 0.2  # Analyze 20%

# Batch API requests (group files)
python analyze_docs.py /path/to/docs --batch-size 10

# Combined optimization
python analyze_docs.py /path/to/docs --parallel --changed-only --no-ai
```

---

## Technical Considerations

### Parallelization Challenges
- **API Rate Limits**: Claude API has per-minute limits
- **Memory Usage**: Multiple processes increase memory
- **State Management**: Shared state requires locks
- **Error Handling**: More complex with parallel execution

### Solutions
- Implement backoff/retry with jitter
- Use memory-mapped files for large docs
- Process pools for CPU-bound, thread pools for I/O
- Comprehensive error aggregation

### Testing Strategy
- Unit tests for cache logic
- Integration tests for parallel processing
- Performance benchmarks (before/after)
- Stress tests with 1000+ file repositories

---

## Monitoring & Metrics

```python
class PerformanceMetrics:
    """Track analyzer performance"""

    def __init__(self):
        self.start_time = time.time()
        self.files_processed = 0
        self.cache_hits = 0
        self.cache_misses = 0
        self.api_calls = 0
        self.errors = 0

    def report(self):
        duration = time.time() - self.start_time
        return {
            'duration_seconds': duration,
            'files_per_second': self.files_processed / duration,
            'cache_hit_rate': self.cache_hits / (self.cache_hits + self.cache_misses),
            'api_calls': self.api_calls,
            'errors': self.errors
        }
```

---

## Conclusion

The biggest performance gains come from:
1. **Parallelization** (4-8x speedup for non-AI)
2. **Incremental analysis** (10-100x for changed files only)
3. **Batch API requests** (2-3x for AI analysis)

Implementing Phase 1 optimizations would provide the best ROI and should be prioritized.
