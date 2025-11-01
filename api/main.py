"""
FastAPI backend for Documentation Analyzer
Wraps the Python analyzer and fixer modules with HTTP endpoints
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import subprocess
import json
import tempfile
import shutil
import os
from pathlib import Path

app = FastAPI(title="Documentation Analyzer API")

# Configure CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class AnalyzeRequest(BaseModel):
    """Request to analyze documentation"""
    project_path: str
    repo_type: str = "mintlify"
    enabled_analyzers: Optional[List[str]] = None
    use_claude_ai: bool = False
    claude_api_key: Optional[str] = None
    claude_model: str = "claude-3-5-sonnet-20241022"
    max_tokens: Optional[int] = 4096


class FixRequest(BaseModel):
    """Request to generate fixes (dry-run)"""
    project_path: str
    enabled_fixers: Optional[List[str]] = None
    use_claude_ai: bool = False
    claude_api_key: Optional[str] = None
    claude_model: str = "claude-3-5-sonnet-20241022"
    max_tokens: Optional[int] = 4096


class ApplyFixesRequest(BaseModel):
    """Request to apply selected fixes"""
    project_path: str
    fixes_to_apply: List[str]  # List of fix IDs or patterns


class ModuleInfo(BaseModel):
    """Information about an analyzer/fixer module"""
    id: str
    name: str
    description: str
    category: str


# Available analyzers and fixers metadata
ANALYZERS = [
    # Core Analyzers
    {"id": "frontmatter", "name": "Frontmatter", "description": "Validates required frontmatter fields", "category": "core"},
    {"id": "code_blocks", "name": "Code Blocks", "description": "Checks for language tags on code blocks", "category": "core"},
    {"id": "broken_links", "name": "Broken Links", "description": "Detects broken internal links", "category": "core"},
    {"id": "images", "name": "Images", "description": "Validates image paths and alt text", "category": "core"},
    {"id": "headings_hierarchy", "name": "Headings Hierarchy", "description": "Checks proper heading level progression", "category": "core"},

    # High-Impact Analyzers
    {"id": "code_examples", "name": "Code Examples", "description": "Validates code example quality", "category": "high-impact"},
    {"id": "readability", "name": "Readability", "description": "Analyzes content readability", "category": "high-impact"},
    {"id": "navigation", "name": "Navigation", "description": "Validates navigation structure", "category": "high-impact"},
    {"id": "search_keywords", "name": "Search Keywords", "description": "Checks SEO and search optimization", "category": "high-impact"},
    {"id": "consistency", "name": "Consistency", "description": "Checks formatting consistency", "category": "high-impact"},
    {"id": "toc", "name": "Table of Contents", "description": "Validates TOC structure", "category": "high-impact"},

    # Advanced Analyzers
    {"id": "style_guide", "name": "Style Guide (AI)", "description": "AI-powered style guide validation", "category": "advanced"},
    {"id": "completeness", "name": "Completeness", "description": "Checks documentation completeness", "category": "advanced"},
    {"id": "freshness", "name": "Freshness", "description": "Detects outdated content", "category": "advanced"},
    {"id": "accessibility", "name": "Accessibility", "description": "Validates WCAG compliance", "category": "advanced"},
    {"id": "structure", "name": "Structure", "description": "Analyzes document structure", "category": "advanced"},
    {"id": "cross_references", "name": "Cross References", "description": "Validates cross-references", "category": "advanced"},
]

FIXERS = [
    # Core Fixers
    {"id": "frontmatter_fixer", "name": "Frontmatter Fixer", "description": "Adds/fixes frontmatter fields", "category": "core"},
    {"id": "code_blocks_fixer", "name": "Code Blocks Fixer", "description": "Adds language tags to code blocks", "category": "core"},
    {"id": "broken_links_fixer", "name": "Broken Links Fixer", "description": "Fixes broken internal links", "category": "core"},
    {"id": "images_fixer", "name": "Images Fixer", "description": "Fixes image paths and adds alt text", "category": "core"},
    {"id": "headings_hierarchy_fixer", "name": "Headings Hierarchy Fixer", "description": "Fixes heading level issues", "category": "core"},

    # High-Impact Fixers
    {"id": "code_examples_fixer", "name": "Code Examples Fixer", "description": "Improves code examples", "category": "high-impact"},
    {"id": "readability_fixer", "name": "Readability Fixer", "description": "Improves content readability", "category": "high-impact"},
    {"id": "navigation_fixer", "name": "Navigation Fixer", "description": "Fixes navigation structure", "category": "high-impact"},
    {"id": "search_keywords_fixer", "name": "Search Keywords Fixer", "description": "Improves SEO", "category": "high-impact"},
    {"id": "consistency_fixer", "name": "Consistency Fixer", "description": "Fixes formatting inconsistencies", "category": "high-impact"},
    {"id": "toc_fixer", "name": "Table of Contents Fixer", "description": "Fixes TOC structure", "category": "high-impact"},

    # Advanced Fixers
    {"id": "style_guide_fixer", "name": "Style Guide Fixer (AI)", "description": "AI-powered style fixes", "category": "advanced"},
    {"id": "completeness_fixer", "name": "Completeness Fixer", "description": "Adds missing content", "category": "advanced"},
    {"id": "freshness_fixer", "name": "Freshness Fixer", "description": "Updates outdated content", "category": "advanced"},
    {"id": "accessibility_fixer", "name": "Accessibility Fixer", "description": "Fixes accessibility issues", "category": "advanced"},
    {"id": "structure_fixer", "name": "Structure Fixer", "description": "Fixes document structure", "category": "advanced"},
    {"id": "cross_references_fixer", "name": "Cross References Fixer", "description": "Fixes cross-references", "category": "advanced"},
]


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "Documentation Analyzer API",
        "version": "1.0.0"
    }


@app.get("/api/analyzers")
async def get_analyzers() -> List[ModuleInfo]:
    """Get list of available analyzer modules"""
    return ANALYZERS


@app.get("/api/fixers")
async def get_fixers() -> List[ModuleInfo]:
    """Get list of available fixer modules"""
    return FIXERS


@app.post("/api/analyze")
async def analyze_docs(request: AnalyzeRequest) -> Dict[str, Any]:
    """
    Run documentation analysis

    Returns:
        - summary: Overall statistics
        - issues: List of issues found by category
        - files_analyzed: Number of files analyzed
    """
    try:
        # Build command
        cmd = [
            "python3",
            "doc_analyzer.py",
            request.project_path,
            "--repo-type", request.repo_type,
            "--format", "all"  # Generate HTML, MD, and JSON
        ]

        # Add Claude AI integration if enabled
        if request.use_claude_ai and request.claude_api_key:
            os.environ["ANTHROPIC_API_KEY"] = request.claude_api_key
            os.environ["CLAUDE_MODEL"] = request.claude_model

        # Run analyzer from parent directory
        analyzer_dir = Path(__file__).parent.parent
        result = subprocess.run(
            cmd,
            cwd=analyzer_dir,
            capture_output=True,
            text=True,
            timeout=1800  # 30 minute timeout
        )

        # Parse output - look for JSON and report directory in stdout
        output_lines = result.stdout.strip().split('\n') if result.stdout else []
        json_output = None
        report_dir = None

        for line in output_lines:
            # Look for JSON output
            if line.strip().startswith('{'):
                try:
                    json_output = json.loads(line)
                except json.JSONDecodeError:
                    continue
            # Look for report directory (e.g., "Report exported to: reports/2025-10-31_19-30-15")
            if "Report exported to:" in line or "reports/" in line:
                import re
                match = re.search(r'reports/[\d\-_]+', line)
                if match:
                    report_dir = match.group(0)

        # If no JSON output and command failed, raise error
        if not json_output and result.returncode != 0:
            error_msg = f"Analysis failed with return code {result.returncode}"
            if result.stderr:
                error_msg += f"\n\nError output:\n{result.stderr[:500]}"
            if result.stdout:
                error_msg += f"\n\nStandard output:\n{result.stdout[:500]}"
            raise HTTPException(
                status_code=500,
                detail=error_msg
            )

        if not json_output:
            # Return raw output if JSON parsing fails but command succeeded
            return {
                "summary": {"total_issues": 0, "files_analyzed": 0},
                "issues": [],
                "raw_output": result.stdout,
                "stderr": result.stderr if result.stderr else None
            }

        # Add report directory and file paths to response
        if report_dir:
            json_output["report_dir"] = report_dir
            json_output["report_files"] = {
                "json": "doc_analysis_report.json",
                "html": "doc_analysis_report.html",
                "markdown": "doc_analysis_report.md"
            }

        return json_output

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Analysis timed out after 30 minutes")
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.post("/api/fix")
async def generate_fixes(request: FixRequest) -> Dict[str, Any]:
    """
    Generate fixes in dry-run mode (preview only)

    Returns:
        - fixes: List of proposed fixes with before/after diffs
        - summary: Statistics about fixes
    """
    try:
        # Build command
        cmd = [
            "python3",
            "doc_fixer.py",
            request.project_path,
            "--dry-run"
        ]

        # Add Claude AI integration if enabled
        if request.use_claude_ai and request.claude_api_key:
            os.environ["ANTHROPIC_API_KEY"] = request.claude_api_key
            os.environ["CLAUDE_MODEL"] = request.claude_model

        # Run fixer from parent directory
        fixer_dir = Path(__file__).parent.parent
        result = subprocess.run(
            cmd,
            cwd=fixer_dir,
            capture_output=True,
            text=True,
            timeout=1800  # 30 minute timeout for fixes
        )

        # Parse output - look for JSON and report directory in stdout
        output_lines = result.stdout.strip().split('\n') if result.stdout else []
        json_output = None
        report_dir = None

        for line in output_lines:
            # Look for JSON output
            if line.strip().startswith('{'):
                try:
                    json_output = json.loads(line)
                except json.JSONDecodeError:
                    continue
            # Look for report directory
            if "Report exported to:" in line or "reports/" in line:
                import re
                match = re.search(r'reports/[\d\-_]+', line)
                if match:
                    report_dir = match.group(0)

        # If no JSON output and command failed, raise error
        if not json_output and result.returncode != 0:
            error_msg = f"Fix generation failed with return code {result.returncode}"
            if result.stderr:
                error_msg += f"\n\nError output:\n{result.stderr[:500]}"
            if result.stdout:
                error_msg += f"\n\nStandard output:\n{result.stdout[:500]}"
            raise HTTPException(
                status_code=500,
                detail=error_msg
            )

        if not json_output:
            # Return raw output if JSON parsing fails but command succeeded
            return {
                "summary": {"total_fixes": 0, "files_modified": 0},
                "fixes": [],
                "raw_output": result.stdout,
                "stderr": result.stderr if result.stderr else None
            }

        # Add report directory and file paths to response
        if report_dir:
            json_output["report_dir"] = report_dir
            json_output["report_files"] = {
                "json": "doc_fix_report.json",
                "html": "doc_fix_report.html",
                "markdown": "doc_fix_report.md"
            }

        return json_output

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Fix generation timed out after 30 minutes")
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.post("/api/apply-fixes")
async def apply_fixes(request: ApplyFixesRequest) -> Dict[str, Any]:
    """
    Apply fixes to the documentation (removes --dry-run flag)

    WARNING: This will modify your documentation files!
    """
    try:
        # Build command without --dry-run to actually apply fixes
        cmd = [
            "python3",
            "doc_fixer.py",
            request.project_path
        ]

        # Run fixer from parent directory
        fixer_dir = Path(__file__).parent.parent
        result = subprocess.run(
            cmd,
            cwd=fixer_dir,
            capture_output=True,
            text=True,
            timeout=1800  # 30 minute timeout
        )

        # Parse output
        output_lines = result.stdout.strip().split('\n') if result.stdout else []
        json_output = None
        report_dir = None

        for line in output_lines:
            # Look for JSON output
            if line.strip().startswith('{'):
                try:
                    json_output = json.loads(line)
                except json.JSONDecodeError:
                    continue
            # Look for report directory
            if "Report exported to:" in line or "reports/" in line:
                import re
                match = re.search(r'reports/[\d\-_]+', line)
                if match:
                    report_dir = match.group(0)

        # If no JSON output and command failed, raise error
        if not json_output and result.returncode != 0:
            error_msg = f"Fix application failed with return code {result.returncode}"
            if result.stderr:
                error_msg += f"\n\nError output:\n{result.stderr[:500]}"
            if result.stdout:
                error_msg += f"\n\nStandard output:\n{result.stdout[:500]}"
            raise HTTPException(
                status_code=500,
                detail=error_msg
            )

        if not json_output:
            # Return raw output if JSON parsing fails but command succeeded
            return {
                "summary": {
                    "total_fixes_applied": 0,
                    "files_modified": 0,
                    "success": True
                },
                "message": "Fixes applied successfully (no detailed output available)",
                "raw_output": result.stdout,
                "stderr": result.stderr if result.stderr else None
            }

        # Add report directory and success flag to response
        json_output["success"] = True
        json_output["message"] = "Fixes applied successfully to your documentation files"
        if report_dir:
            json_output["report_dir"] = report_dir
            json_output["report_files"] = {
                "json": "doc_fix_report.json",
                "html": "doc_fix_report.html",
                "markdown": "doc_fix_report.md"
            }

        return json_output

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Fix application timed out after 30 minutes")
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.get("/api/reports/{report_dir}/{filename}")
async def serve_report(report_dir: str, filename: str):
    """
    Serve report files (HTML, MD, JSON) for viewing or download

    Args:
        report_dir: Report directory name (e.g., '2025-10-31_19-30-15')
        filename: Report filename (e.g., 'doc_analysis_report.html')

    Returns:
        FileResponse: The requested report file
    """
    from fastapi.responses import FileResponse
    import os

    # Validate report directory name (prevent directory traversal)
    if '..' in report_dir or '/' in report_dir or '\\' in report_dir:
        raise HTTPException(status_code=400, detail="Invalid report directory")

    # Validate filename
    allowed_files = [
        'doc_analysis_report.json', 'doc_analysis_report.html', 'doc_analysis_report.md',
        'doc_fix_report.json', 'doc_fix_report.html', 'doc_fix_report.md'
    ]
    if filename not in allowed_files:
        raise HTTPException(status_code=400, detail="Invalid filename")

    # Construct file path
    reports_base = Path(__file__).parent.parent / "reports"
    file_path = reports_base / report_dir / filename

    # Check if file exists
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Report file not found")

    # Determine media type based on extension
    media_types = {
        '.json': 'application/json',
        '.html': 'text/html',
        '.md': 'text/markdown'
    }
    ext = os.path.splitext(filename)[1]
    media_type = media_types.get(ext, 'text/plain')

    return FileResponse(
        path=str(file_path),
        media_type=media_type,
        filename=filename
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
