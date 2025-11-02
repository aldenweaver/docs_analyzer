"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001/api";

export default function FixResultsPage() {
  const router = useRouter();
  const [reportDir, setReportDir] = useState<string>("");
  const [reportFiles, setReportFiles] = useState<any>({});
  const [summary, setSummary] = useState<any>({});
  const [htmlContent, setHtmlContent] = useState<string>("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showDropdown, setShowDropdown] = useState(false);
  const [showConfirmDialog, setShowConfirmDialog] = useState(false);
  const [applying, setApplying] = useState(false);
  const [applySuccess, setApplySuccess] = useState(false);
  const [projectPath, setProjectPath] = useState<string>("");

  useEffect(() => {
    // Load data from sessionStorage
    const dir = sessionStorage.getItem('fixReportDir');
    const files = sessionStorage.getItem('fixReportFiles');
    const summaryData = sessionStorage.getItem('fixSummary');
    const path = sessionStorage.getItem('fixProjectPath');

    if (!dir || !files) {
      setError("No fix results found. Please generate fixes first.");
      setLoading(false);
      return;
    }

    setReportDir(dir);
    setReportFiles(JSON.parse(files));
    setSummary(JSON.parse(summaryData || '{}'));
    setProjectPath(path || '');

    // Fetch HTML content
    fetchHtmlReport(dir, JSON.parse(files).html);
  }, []);

  const fetchHtmlReport = async (dir: string, filename: string) => {
    try {
      const response = await fetch(`${API_BASE}/reports/${dir}/${filename}`);
      if (!response.ok) {
        throw new Error(`Failed to fetch report: ${response.statusText}`);
      }
      const html = await response.text();
      setHtmlContent(html);
    } catch (err: any) {
      setError(err.message || "Failed to load HTML report");
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = (format: 'html' | 'json' | 'markdown') => {
    const filename = reportFiles[format];
    if (!filename) return;

    const url = `${API_BASE}/reports/${reportDir}/${filename}`;
    window.open(url, '_blank');
    setShowDropdown(false);
  };

  const handleApplyFixes = async () => {
    if (!projectPath) {
      setError("Project path not found. Please generate fixes again.");
      return;
    }

    setApplying(true);
    setShowConfirmDialog(false);

    try {
      const response = await fetch(`${API_BASE}/apply-fixes`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          project_path: projectPath,
          fixes_to_apply: []  // Apply all fixes
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        throw new Error(errorData?.detail || `Failed to apply fixes: ${response.statusText}`);
      }

      const result = await response.json();
      setApplySuccess(true);
      setError(null);

      // Show success message
      alert(`✅ Fixes applied successfully!\n\n${result.message || 'Your documentation files have been updated.'}`);
    } catch (err: any) {
      setError(err.message || "Failed to apply fixes");
      setApplySuccess(false);
    } finally {
      setApplying(false);
    }
  };

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-center">
          <div className="animate-spin h-8 w-8 border-4 border-primary border-t-transparent rounded-full"></div>
          <span className="ml-3 text-lg">Loading report...</span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-destructive/10 border border-destructive text-destructive rounded-lg p-6">
          <h3 className="font-semibold mb-2">Error</h3>
          <p>{error}</p>
          <button
            onClick={() => router.push('/')}
            className="mt-4 px-4 py-2 bg-primary text-primary-foreground rounded-md hover:opacity-90"
          >
            Back to Analysis
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header with Download Button */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-4xl font-bold text-foreground mb-2">
            Fix Results
          </h1>
          <p className="text-muted-foreground">
            Detailed report for generated documentation fixes
          </p>
        </div>
        <div className="flex gap-3">
          {/* Download Dropdown */}
          <div className="relative">
            <button
              onClick={() => setShowDropdown(!showDropdown)}
              className="px-4 py-2 bg-secondary text-secondary-foreground rounded-md font-medium hover:opacity-90 flex items-center gap-2"
            >
              Download Report
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            {showDropdown && (
              <div className="absolute right-0 mt-2 w-48 bg-card border rounded-md shadow-lg z-10">
                <button
                  onClick={() => handleDownload('html')}
                  className="w-full text-left px-4 py-2 hover:bg-secondary rounded-t-md"
                >
                  Download HTML
                </button>
                <button
                  onClick={() => handleDownload('markdown')}
                  className="w-full text-left px-4 py-2 hover:bg-secondary"
                >
                  Download Markdown
                </button>
                <button
                  onClick={() => handleDownload('json')}
                  className="w-full text-left px-4 py-2 hover:bg-secondary rounded-b-md"
                >
                  Download JSON
                </button>
              </div>
            )}
          </div>
          {/* Apply Fixes Button */}
          {!applySuccess && projectPath && (
            <button
              onClick={() => setShowConfirmDialog(true)}
              disabled={applying}
              className="px-4 py-2 bg-orange-600 text-white rounded-md font-medium hover:bg-orange-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {applying ? 'Applying...' : 'Apply Selected Fixes'}
            </button>
          )}
          {/* Back Button */}
          <button
            onClick={() => router.push('/')}
            className="px-4 py-2 bg-primary text-primary-foreground rounded-md font-medium hover:opacity-90"
          >
            Back to Analysis
          </button>
        </div>
      </div>

      {/* Confirmation Dialog */}
      {showConfirmDialog && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-card border rounded-lg shadow-xl p-6 max-w-md mx-4">
            <h3 className="text-xl font-semibold mb-3">Apply Fixes to Documentation?</h3>
            <p className="text-muted-foreground mb-2">
              This will modify your documentation files at:
            </p>
            <p className="text-sm font-mono bg-secondary px-3 py-2 rounded mb-4 break-all">
              {projectPath}
            </p>
            <p className="text-sm text-destructive mb-6">
              ⚠️ Warning: This action will permanently modify your files. Make sure you have a backup or are using version control.
            </p>
            <div className="flex gap-3 justify-end">
              <button
                onClick={() => setShowConfirmDialog(false)}
                className="px-4 py-2 bg-secondary text-secondary-foreground rounded-md font-medium hover:opacity-90"
              >
                Cancel
              </button>
              <button
                onClick={handleApplyFixes}
                className="px-4 py-2 bg-orange-600 text-white rounded-md font-medium hover:bg-orange-700"
              >
                Yes, Apply Fixes
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Summary Cards */}
      {summary && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-card rounded-lg border p-4">
            <div className="text-3xl font-bold text-green-600">
              {summary.total_fixes || 0}
            </div>
            <div className="text-sm text-muted-foreground">Total Fixes</div>
          </div>
          <div className="bg-card rounded-lg border p-4">
            <div className="text-3xl font-bold text-primary">
              {summary.files_modified || 0}
            </div>
            <div className="text-sm text-muted-foreground">Files Modified</div>
          </div>
          <div className="bg-card rounded-lg border p-4">
            <div className="text-3xl font-bold text-primary">
              {summary.total_files || 0}
            </div>
            <div className="text-sm text-muted-foreground">Files Processed</div>
          </div>
          <div className="bg-card rounded-lg border p-4">
            <div className="text-3xl font-bold text-orange-600">
              {summary.mode === 'dry_run' ? 'Preview' : 'Applied'}
            </div>
            <div className="text-sm text-muted-foreground">Mode</div>
          </div>
        </div>
      )}

      {/* HTML Report Display */}
      <div className="bg-card rounded-lg border p-6">
        <h2 className="text-2xl font-semibold mb-4">Full Report</h2>
        <div
          className="prose prose-sm max-w-none"
          dangerouslySetInnerHTML={{ __html: htmlContent }}
        />
      </div>
    </div>
  );
}
