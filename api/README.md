# Documentation Analyzer API

FastAPI backend that wraps the Python documentation analyzer and fixer modules with HTTP endpoints.

## Installation

```bash
cd api
pip install -r requirements.txt
```

## Running the API

```bash
# From the api directory
python3 main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
- `GET /` - Check API status

### Module Lists
- `GET /api/analyzers` - Get list of available analyzer modules
- `GET /api/fixers` - Get list of available fixer modules

### Analysis & Fixing
- `POST /api/analyze` - Run documentation analysis
- `POST /api/fix` - Generate fixes in dry-run mode (preview only)
- `POST /api/apply-fixes` - Apply selected fixes (not yet implemented)

## Example Usage

### Get Available Analyzers
```bash
curl http://localhost:8000/api/analyzers
```

### Run Analysis
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "project_path": "/path/to/docs",
    "repo_type": "mintlify",
    "use_claude_ai": false
  }'
```

### Generate Fixes (Dry-Run)
```bash
curl -X POST http://localhost:8000/api/fix \
  -H "Content-Type: application/json" \
  -d '{
    "project_path": "/path/to/docs",
    "use_claude_ai": true,
    "claude_api_key": "sk-ant-..."
  }'
```

## Integration with Next.js Frontend

The Next.js app at `/ui` is configured to proxy API requests to this backend:
- Frontend: `http://localhost:3002`
- Backend: `http://localhost:8000`

Frontend requests to `/api/backend/*` are automatically proxied to the FastAPI backend.

## CORS Configuration

The API allows requests from:
- `http://localhost:3000`
- `http://localhost:3001`
- `http://localhost:3002`

## Environment Variables

- `ANTHROPIC_API_KEY` - Claude API key (when using AI-powered features)
- `CLAUDE_MODEL` - Claude model to use (default: claude-3-5-sonnet-20241022)
