# Documentation Quality Automation - Implementation Guide
## Step-by-Step Deployment Instructions

This guide walks you through deploying the Documentation Quality Automation System to analyze and improve your documentation.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [First Scan](#first-scan)
5. [Interpreting Results](#interpreting-results)
6. [Applying Fixes](#applying-fixes)
7. [Setting Up Monitoring](#setting-up-monitoring)
8. [CI/CD Integration](#cicd-integration)
9. [Ongoing Maintenance](#ongoing-maintenance)
10. [Advanced Features](#advanced-features)

---

## Prerequisites

### System Requirements

- **Python 3.9+**
- **Git** (for version control)
- **10MB disk space** (for database and reports)
- **Internet access** (optional, for AI analysis)

### Optional Requirements

- **ANTHROPIC_API_KEY** - For AI-powered semantic analysis
- **SMTP credentials** - For email alerts
- **Slack webhook** - For Slack notifications

### Knowledge Requirements

- Basic command line usage
- Understanding of your documentation structure
- Familiarity with markdown/MDX files

---

## Installation

### Step 1: Download the System

```bash
# If you have the files locally
cd /path/to/doc-quality-system

# Or clone from repository
git clone https://github.com/your-repo/doc-quality-automation.git
cd doc-quality-automation
```

### Step 2: Install Python Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Verify installation
python -c "import anthropic, yaml; print('✅ Dependencies installed')"
```

### Step 3: (Optional) Set Up API Keys

```bash
# For AI analysis (optional but recommended)
export ANTHROPIC_API_KEY='sk-ant-...'

# For email alerts (optional)
export SMTP_SERVER='smtp.gmail.com'
export SMTP_PORT='587'
export ALERT_EMAIL_SENDER='your-email@example.com'
export ALERT_EMAIL_PASSWORD='your-password'

# For Slack alerts (optional)
export SLACK_WEBHOOK_URL='https://hooks.slack.com/services/...'
```

**Pro Tip**: Add these to your `~/.bashrc` or `~/.zshrc` to make them permanent.

---

## Configuration

### Step 1: Create Configuration File

Start with the template:

```bash
cp quality_config.yaml my_config.yaml
```

### Step 2: Configure Repository Path

Edit `my_config.yaml`:

```yaml
repository:
  path: "./docs"  # Change to your documentation directory
  
  file_patterns:
    - "**/*.md"
    - "**/*.mdx"
  
  exclude_patterns:
    - "**/node_modules/**"
    - "**/.git/**"
    - "**/dist/**"
```

### Step 3: Configure Terminology Rules

Add your specific terminology:

```yaml
terminology:
  deprecated_terms:
    - "old_product_name"
    - "deprecated_api"
  
  preferred_terms:
    old_product_name: "new_product_name"
    deprecated_api: "modern_api"
  
  proper_nouns:
    - "YourProduct"
    - "YourCompany"
```

### Step 4: Configure Frontmatter Requirements

For MDX files:

```yaml
frontmatter:
  required:
    - title
    - description
  
  optional:
    - sidebarTitle
    - author
  
  max_description_length: 160
  min_description_length: 50
```

### Step 5: Test Configuration

```bash
# Validate configuration
python -c "
import yaml
with open('my_config.yaml') as f:
    config = yaml.safe_load(f)
    print('✅ Configuration valid')
    print(f'Repository: {config[\"repository\"][\"path\"]}')
"
```

---

## First Scan

### Step 1: Run Initial Scan

```bash
python doc_quality_automation.py scan --config my_config.yaml
```

**Expected output:**
```
🔍 Starting repository scan...
Found 47 files to analyze
Analyzing: docs/overview.md
Analyzing: docs/api/quickstart.md
...
Running cross-file analysis...

✅ Scan complete. Found 127 issues.

Summary:
  🔴 CRITICAL: 5
  🟠 HIGH: 23
  🟡 MEDIUM: 54
  🟢 LOW: 45
```

### Step 2: Generate Initial Report

```bash
python doc_quality_automation.py report --config my_config.yaml --output initial_report.md
```

### Step 3: Review the Report

```bash
# View in terminal
cat initial_report.md

# Or open in your editor
code initial_report.md
```

---

## Interpreting Results

### Understanding Severity Levels

**🔴 CRITICAL** - Fix immediately
- Broken links
- Missing required frontmatter
- Major structural issues
- **Action**: Fix within 24 hours

**🟠 HIGH** - Fix this sprint
- Deprecated terminology
- Missing error handling in examples
- Significant inconsistencies
- **Action**: Plan fixes in next sprint

**🟡 MEDIUM** - Next iteration
- Style inconsistencies
- Minor formatting issues
- Optimization opportunities
- **Action**: Address in next major update

**🟢 LOW** - Nice to have
- Preference violations
- Minor optimizations
- **Action**: Fix when convenient

### Reading Issue Descriptions

Each issue includes:

```
**HIGH:** Deprecated term 'Claude Code SDK' found
- File: `docs/api/quickstart.md`
- Line: 15
- Fix: Replace 'Claude Code SDK' with 'Claude Agent SDK'
- Context: "Use the Claude Code SDK to access..."
```

**Components:**
- **Severity**: How urgent the fix is
- **Description**: What the problem is
- **File & Line**: Where to find it
- **Fix**: How to resolve it
- **Context**: Surrounding text

### Understanding Metrics

```
Primary KPIs:
  • Total Issues: 127
  • Critical Issues: 5
  • Documentation Debt: 28
  • Auto-fixable Rate: 42%
```

**What these mean:**
- **Total Issues**: All problems found
- **Critical Issues**: Urgent fixes needed (target: 0)
- **Documentation Debt**: Critical + High issues (target: <2)
- **Auto-fixable Rate**: Percentage that can be fixed automatically

---

## Applying Fixes

### Step 1: Preview Auto-fixes

**Always run dry-run first:**

```bash
python doc_quality_automation.py fix --config my_config.yaml --dry-run
```

**Output:**
```
🔧 Running auto-fix (DRY RUN)...

Would fix 53 issues across 18 files:

Terminology fixes (38 issues):
  ✓ docs/overview.md: "Claude Code SDK" → "Claude Agent SDK"
  ✓ docs/api/guide.md: "simply" → [removed]
  ...

Frontmatter fixes (15 issues):
  ✓ docs/advanced.mdx: Add missing frontmatter block
  ✓ docs/reference.mdx: Add 'description' field
  ...

No files would be modified in dry-run mode.
```

### Step 2: Create Backup

```bash
# Manual backup (recommended for first time)
cp -r docs docs_backup_$(date +%Y%m%d)

# Or rely on automatic backups
# (configured in quality_config.yaml)
```

### Step 3: Apply Auto-fixes

```bash
python doc_quality_automation.py fix --config my_config.yaml
```

**Output:**
```
✅ Fixed 53 issues

All changes backed up to: .doc_quality_backups/
All actions logged to: doc_quality.log

Remaining issues: 74 (require manual review)
```

### Step 4: Review Changes

```bash
# View what changed
git diff docs/

# Or use your preferred diff tool
code --diff docs/ docs_backup_*/
```

### Step 5: Commit Fixes

```bash
git add docs/
git commit -m "docs: automated quality improvements

- Fixed deprecated terminology
- Added missing frontmatter
- Standardized formatting

Auto-fixed 53 issues. See doc_quality.log for details."
```

### Step 6: Manual Fixes

For remaining issues:

1. **Filter by severity**: Start with critical, then high
2. **Group by type**: Fix similar issues together
3. **Use IDE features**: Find/replace for patterns
4. **Commit frequently**: One issue type per commit

Example workflow:

```bash
# Fix all broken links
# (manually, using report as reference)
git commit -m "docs: fix broken internal links"

# Fix missing sections
git commit -m "docs: add missing Prerequisites sections"

# Improve code examples
git commit -m "docs: add error handling to API examples"
```

---

## Setting Up Monitoring

### Step 1: Configure Alerts

Edit `my_config.yaml`:

```yaml
alerts:
  enabled: true
  
  channels:
    - type: file
      enabled: true
      path: alerts.log
    
    - type: email
      enabled: true
      recipients:
        - docs-team@example.com
    
    - type: slack
      enabled: true
      webhook_url: "${SLACK_WEBHOOK_URL}"
  
  rules:
    - name: "Critical Issues Detected"
      condition: "critical_issues > 0"
      severity: "critical"
      message: "Documentation has critical issues"
    
    - name: "Quality Degradation"
      condition: "total_issues > 100"
      severity: "high"
      message: "Documentation quality degrading"
```

### Step 2: Set Up Scheduled Monitoring

**Using cron (Linux/Mac):**

```bash
# Edit crontab
crontab -e

# Add daily scan at 2 AM
0 2 * * * cd /path/to/doc-quality-system && python doc_quality_monitoring.py my_config.yaml
```

**Using Task Scheduler (Windows):**

1. Open Task Scheduler
2. Create Basic Task
3. Trigger: Daily at 2 AM
4. Action: Start a program
5. Program: `python`
6. Arguments: `doc_quality_monitoring.py my_config.yaml`
7. Start in: `C:\path\to\doc-quality-system`

### Step 3: Set Up Dashboard

```bash
# Generate initial dashboard
python doc_quality_monitoring.py my_config.yaml

# Serve dashboard (optional)
python -m http.server 8080 &
# Open http://localhost:8080/dashboard.html
```

### Step 4: Test Alerts

```bash
# Trigger a test alert (if configured)
python -c "
from doc_quality_monitoring import MonitoringSystem
system = MonitoringSystem('my_config.yaml')
system.alert_manager.send_alerts([
    Alert('Test Alert', 'low', 'Testing alert system', {})
])
"
```

---

## CI/CD Integration

### GitHub Actions Setup

**Step 1: Add Workflow File**

Create `.github/workflows/doc-quality.yml`:

```yaml
name: Documentation Quality

on:
  pull_request:
    paths: ['docs/**']
  push:
    branches: [main]

jobs:
  quality-check:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run quality scan
        run: python doc_quality_automation.py scan --config quality_config.yaml
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      
      - name: Generate report
        run: python doc_quality_automation.py report --output quality_report.md
      
      - name: Check quality gates
        run: |
          CRITICAL=$(python doc_quality_automation.py metrics | grep critical_issues | awk '{print $2}')
          if [ "$CRITICAL" -gt "0" ]; then
            echo "❌ Quality gate failed: $CRITICAL critical issues"
            exit 1
          fi
          echo "✅ Quality gates passed"
      
      - name: Upload report
        uses: actions/upload-artifact@v4
        with:
          name: quality-report
          path: quality_report.md
```

**Step 2: Add Secrets**

1. Go to repository Settings → Secrets and variables → Actions
2. Add `ANTHROPIC_API_KEY` (if using AI analysis)
3. Add email/Slack credentials if using alerts

**Step 3: Test Workflow**

```bash
# Create test PR
git checkout -b test-quality-check
echo "# Test" >> docs/test.md
git add docs/test.md
git commit -m "test: quality check workflow"
git push origin test-quality-check

# Create PR and check Actions tab
```

### GitLab CI Setup

Create `.gitlab-ci.yml`:

```yaml
stages:
  - quality

documentation-quality:
  stage: quality
  image: python:3.11
  
  before_script:
    - pip install -r requirements.txt
  
  script:
    - python doc_quality_automation.py scan --config quality_config.yaml
    - python doc_quality_automation.py report --output quality_report.md
    - python doc_quality_automation.py metrics > metrics.txt
  
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
      changes:
        - docs/**/*
  
  artifacts:
    reports:
      metrics: metrics.txt
    paths:
      - quality_report.md
    expire_in: 30 days
```

### Pre-commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash

echo "🔍 Running documentation quality check..."

python doc_quality_automation.py scan --config quality_config.yaml > /dev/null

CRITICAL=$(python doc_quality_automation.py metrics | grep critical_issues | awk '{print $2}')

if [ "$CRITICAL" -gt "0" ]; then
  echo "❌ Commit blocked: $CRITICAL critical documentation issues"
  echo "Run: python doc_quality_automation.py report"
  exit 1
fi

echo "✅ Documentation quality check passed"
exit 0
```

Make it executable:

```bash
chmod +x .git/hooks/pre-commit
```

---

## Ongoing Maintenance

### Weekly Tasks

**Monday: Review Metrics**

```bash
python doc_quality_automation.py metrics

# Check trends
python -c "
from doc_quality_automation import DocumentationQualityEngine
engine = DocumentationQualityEngine('my_config.yaml')
for metric in ['total_issues', 'critical_issues', 'documentation_debt']:
    trend = engine.metrics_collector.calculate_trends(metric, days=7)
    print(f'{metric}: {trend[\"trend\"]} ({trend[\"percent_change\"]:.1f}%)')
engine.close()
"
```

**Wednesday: Scan for New Issues**

```bash
python doc_quality_automation.py scan --config my_config.yaml
python doc_quality_automation.py report --output weekly_report.md
```

**Friday: Apply Auto-fixes**

```bash
python doc_quality_automation.py fix --config my_config.yaml
git add docs/
git commit -m "docs: weekly quality improvements"
```

### Monthly Tasks

**Review Configuration**

- Update deprecated terms list
- Adjust quality gates based on progress
- Review alert rules effectiveness

**Deep Analysis**

```bash
# Generate comprehensive report
python doc_quality_automation.py scan --config my_config.yaml
python doc_quality_automation.py report --output monthly_analysis.md

# Generate dashboard
python doc_quality_monitoring.py my_config.yaml
```

**Trend Analysis**

```bash
# 30-day trends
python -c "
from doc_quality_automation import DocumentationQualityEngine
engine = DocumentationQualityEngine('my_config.yaml')

print('📊 30-Day Trends:')
for metric in ['total_issues', 'critical_issues', 'documentation_debt', 'content_consistency_score']:
    trend = engine.metrics_collector.calculate_trends(metric, days=30)
    if trend['trend'] != 'insufficient_data':
        print(f'{metric}: {trend[\"trend\"]} ({trend[\"percent_change\"]:+.1f}%)')

engine.close()
"
```

### Quarterly Tasks

**Update Goals**

Review and update targets in `my_config.yaml`:

```yaml
metrics:
  kpis:
    - name: "critical_issues"
      target: 0
      current: 0  # Update quarterly
    
    - name: "documentation_debt"
      target: 2
      current: 1  # Update quarterly
```

**System Updates**

```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Run full test suite
pytest test_doc_quality_automation.py -v

# Re-validate configuration
python -c "import yaml; yaml.safe_load(open('my_config.yaml'))"
```

---

## Advanced Features

### AI-Powered Semantic Analysis

Enable in `my_config.yaml`:

```yaml
ai_analysis:
  enabled: true
  model: "claude-sonnet-4-5-20250929"
  
  analyze:
    - clarity
    - completeness
    - semantic_gaps
  
  max_requests_per_hour: 50
```

Then run:

```bash
export ANTHROPIC_API_KEY='your-key'
python doc_quality_automation.py scan --config my_config.yaml
```

### Custom Checkers

Create `custom_checkers.py`:

```python
from doc_quality_automation import Issue
from datetime import datetime

class MyCompanyStyleChecker:
    def __init__(self, config):
        self.config = config
    
    def check_file(self, file_path, content):
        issues = []
        
        # Your custom logic
        if 'forbidden_phrase' in content.lower():
            issues.append(Issue(
                id=f"custom_{file_path}",
                category="consistency",
                severity="medium",
                type="style_violation",
                file_path=file_path,
                line_number=None,
                description="Contains forbidden phrase",
                auto_fixable=False,
                suggested_fix="Remove or rephrase",
                detected_at=datetime.now().isoformat()
            ))
        
        return issues
```

Integrate in `doc_quality_automation.py`:

```python
from custom_checkers import MyCompanyStyleChecker

# In DocumentationQualityEngine.__init__:
self.custom_checker = MyCompanyStyleChecker(self.config)

# In scan_repository method:
all_issues.extend(self.custom_checker.check_file(file_path, content))
```

### Integration with Documentation Platforms

**Mintlify:**

```yaml
platform:
  type: mintlify
  config_file: mint.json
  
  validation:
    - frontmatter_required
    - relative_links_only
    - component_usage
```

**Docusaurus:**

```yaml
platform:
  type: docusaurus
  config_file: docusaurus.config.js
  
  validation:
    - sidebar_structure
    - mdx_components
    - versioning
```

---

## Success Criteria

### Week 1
- ✅ System installed and configured
- ✅ Initial scan complete
- ✅ Critical issues fixed
- ✅ Team trained on basic usage

### Month 1
- ✅ Critical issues: 0
- ✅ Documentation debt: <10
- ✅ Auto-fix running weekly
- ✅ CI/CD integrated

### Quarter 1
- ✅ Critical issues: 0 (sustained)
- ✅ Documentation debt: <2
- ✅ Consistency score: >90%
- ✅ Monitoring automated

---

## Need Help?

### Common Issues

**"Database is locked"**
- Solution: Close other instances, or delete and recreate DB

**"Module not found"**
- Solution: `pip install -r requirements.txt`

**"Config file not found"**
- Solution: Specify full path: `--config /full/path/to/config.yaml`

### Getting Support

1. **Check logs**: `tail -f doc_quality.log`
2. **Run tests**: `pytest test_doc_quality_automation.py -v`
3. **Validate config**: `python -c "import yaml; yaml.safe_load(open('config.yaml'))"`

---

## Next Steps

1. ✅ Complete installation
2. ✅ Configure for your repository
3. ✅ Run first scan
4. ✅ Apply auto-fixes
5. ✅ Set up monitoring
6. ✅ Integrate with CI/CD
7. ✅ Train your team
8. ✅ Establish ongoing processes

**🎉 Congratulations! You're now running automated documentation quality improvement!**
