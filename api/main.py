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
    {"id": "h1_heading", "name": "H1 Heading", "description": "Ensures exactly one H1 heading per file", "category": "core"},
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
    {"id": "h1_heading_fixer", "name": "H1 Heading Fixer", "description": "Fixes H1 heading issues", "category": "core"},
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
            "--format", "json"
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
            timeout=300  # 5 minute timeout
        )

        # Parse output - look for JSON in stdout
        output_lines = result.stdout.strip().split('\n') if result.stdout else []
        json_output = None

        for line in output_lines:
            if line.strip().startswith('{'):
                try:
                    json_output = json.loads(line)
                    break
                except json.JSONDecodeError:
                    continue

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

        return json_output

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Analysis timed out after 5 minutes")
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
            timeout=600  # 10 minute timeout for fixes
        )

        # Parse output - look for JSON in stdout
        output_lines = result.stdout.strip().split('\n') if result.stdout else []
        json_output = None

        for line in output_lines:
            if line.strip().startswith('{'):
                try:
                    json_output = json.loads(line)
                    break
                except json.JSONDecodeError:
                    continue

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

        return json_output

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Fix generation timed out after 10 minutes")
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.post("/api/apply-fixes")
async def apply_fixes(request: ApplyFixesRequest) -> Dict[str, Any]:
    """
    Apply selected fixes to the documentation

    Note: This is a placeholder. In production, you'd want more sophisticated
    fix selection and application logic.
    """
    # TODO: Implement selective fix application
    raise HTTPException(
        status_code=501,
        detail="Selective fix application not yet implemented. Use dry-run to preview fixes."
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
