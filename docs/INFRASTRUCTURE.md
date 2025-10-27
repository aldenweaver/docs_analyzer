# Infrastructure & Deployment Guide

## Overview

This project is now fully containerized and follows security best practices for easy deployment and development.

## Key Features

### 🐳 Docker Support
- **Dockerfile**: Multi-stage build with non-root user for security
- **docker-compose.yml**: Three service profiles (analyzer, test, shell)
- **Read-only mounts**: Documentation mounted read-only for safety
- **Volume mapping**: Outputs written to local `./reports/` directory

### 🔐 Security Best Practices
- **API keys in .env**: Never committed to git
- **Comprehensive .gitignore**: Excludes secrets, venv, outputs
- **Environment variable precedence**: .env → environment → CLI flags
- **Graceful degradation**: Works without API key

### 📦 Dependency Management
- **Python venv support**: Isolated dependencies
- **Automated setup scripts**: `setup.sh` / `setup.bat`
- **Convenience runner**: `run.sh` auto-activates venv
- **Requirements pinning**: All dependencies in `requirements.txt`

### ⚙️ Flexible Configuration
- **With AI**: Full analysis using Claude API
- **Without AI**: Basic analysis (no API key required)
- **Environment control**: `ENABLE_AI_ANALYSIS` flag
- **Model selection**: Via `CLAUDE_MODEL` env var

## Quick Start Options

### Option 1: Docker (Recommended)

```bash
# Setup
cp .env.example .env
# Edit .env if you want AI analysis

# Run analysis
mkdir -p docs_input reports
cp -r /path/to/docs docs_input/
docker-compose up

# Results in ./reports/
```

### Option 2: Local with Virtual Environment

```bash
# One-command setup
./setup.sh

# Configure (optional)
cp .env.example .env

# Run
source venv/bin/activate
python doc_analyzer.py /path/to/docs
```

### Option 3: Manual Setup

```bash
# Create venv
python3 -m venv venv
source venv/bin/activate

# Install
pip install -r requirements.txt

# Configure
cp .env.example .env

# Run
python doc_analyzer.py /path/to/docs
```

## Environment Variables

### Required for AI Analysis
- `ANTHROPIC_API_KEY`: Your Claude API key

### Optional Configuration
- `ENABLE_AI_ANALYSIS`: true/false (default: true)
- `CLAUDE_MODEL`: Model to use (default: claude-sonnet-4-5-20250929)
- `AI_MAX_TOKENS`: Token limit (default: 2000)
- `DOCS_PATH`: Default docs path
- `REPO_TYPE`: auto/mintlify/docusaurus/mkdocs/generic
- `OUTPUT_DIR`: Report output directory

## Security Features

### What's Protected
1. ✅ API keys never committed (`.env` in `.gitignore`)
2. ✅ Template provided (`.env.example`)
3. ✅ Docker runs as non-root user
4. ✅ Documentation mounted read-only
5. ✅ Virtual environment isolation

### File Structure
```
.
├── .env                    # Your secrets (gitignored)
├── .env.example            # Template (committed)
├── .gitignore              # Excludes secrets, venv, outputs
├── Dockerfile              # Container image
├── docker-compose.yml      # Container orchestration
├── setup.sh / setup.bat    # Automated setup
├── run.sh                  # Convenience runner
└── requirements.txt        # Python dependencies
```

## Modes of Operation

### Full Mode (With API Key)
- ✓ All quality checks
- ✓ AI-powered clarity analysis
- ✓ Semantic gap detection
- ✓ User journey validation
- ✓ Readability metrics
- ✓ Style guide compliance
- ✓ IA validation
- ✓ Consistency checks
- ✓ Duplication detection

### Basic Mode (Without API Key)
- ✓ All quality checks except AI
- ✓ Readability metrics
- ✓ Style guide compliance
- ✓ IA validation
- ✓ Consistency checks
- ✓ Duplication detection
- ✗ AI clarity analysis
- ✗ AI semantic gaps

To run in basic mode: set `ENABLE_AI_ANALYSIS=false` or omit `ANTHROPIC_API_KEY`

## Docker Commands

### Run Analysis
```bash
docker-compose up
```

### Run Tests
```bash
docker-compose --profile testing run test
```

### Interactive Shell
```bash
docker-compose --profile dev run shell
```

### Build Only
```bash
docker-compose build
```

### Custom Command
```bash
docker-compose run analyzer python doc_analyzer.py /app/docs_input --format json
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'dotenv'"
```bash
pip install python-dotenv
# Or run: ./setup.sh
```

### "Permission denied" on Docker
```bash
# Dockerfile uses UID 1000 - ensure your user can access mounted volumes
sudo chown -R $(id -u):$(id -g) docs_input reports
```

### AI analysis not working
```bash
# Check API key is set
echo $ANTHROPIC_API_KEY

# Check .env file exists and has key
cat .env | grep ANTHROPIC_API_KEY

# Enable debug mode
export ENABLE_AI_ANALYSIS=true
```

### Virtual environment issues
```bash
# Remove and recreate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Documentation Quality

on: [pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Run analyzer
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          ENABLE_AI_ANALYSIS: true
        run: |
          pip install -r requirements.txt
          python doc_analyzer.py ./docs --format json

      - name: Upload report
        uses: actions/upload-artifact@v2
        with:
          name: quality-report
          path: doc_analysis_report.json
```

## Testing

### Run Integration Tests
```bash
# Test environment configuration
python3 test_env_integration.py

# Run all tests
pytest test_analyzer.py -v

# With coverage
pytest test_analyzer.py --cov=doc_analyzer
```

## Best Practices

1. **Never commit .env**: Always use .env.example as template
2. **Use Docker for consistency**: Ensures same environment everywhere
3. **Enable AI when possible**: Provides deeper analysis
4. **Run in CI/CD**: Catch documentation issues early
5. **Review reports**: Generated HTML reports are interactive
6. **Use venv locally**: Isolate dependencies from system Python
7. **Pin dependencies**: Requirements.txt ensures reproducibility

## Migration Guide

If you have an existing setup:

1. Update dependencies:
   ```bash
   pip install python-dotenv
   ```

2. Create .env file:
   ```bash
   cp .env.example .env
   # Move API key from config.yaml to .env
   ```

3. Update config.yaml:
   - Remove `claude_api.api_key_env`
   - Remove `claude_api.default_model` (now in .env)

4. Test:
   ```bash
   python3 test_env_integration.py
   ```

## Support

- **Issues**: Check logs in Docker with `docker-compose logs`
- **Dependencies**: Ensure Python 3.8+ and pip are up to date
- **Docker**: Ensure Docker and Docker Compose are installed
- **Permissions**: Ensure write access to `./reports/` directory
