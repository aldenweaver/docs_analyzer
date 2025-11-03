"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { runAnalysis, generateFixes } from "@/lib/api";

export default function AnalyzePage() {
  const router = useRouter();

  // State for form inputs
  const [projectPath, setProjectPath] = useState("");
  const [useClaudeAI, setUseClaudeAI] = useState(false);
  const [apiKey, setApiKey] = useState("");
  const [claudeModel, setClaudeModel] = useState("claude-3-5-sonnet-20241022");
  const [maxTokens, setMaxTokens] = useState(4096);

  // State for analysis
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [fixResult, setFixResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [progressMessage, setProgressMessage] = useState<string>("");
  const [startTime, setStartTime] = useState<number | null>(null);

  // Update elapsed time every second while analyzing
  const [elapsedTime, setElapsedTime] = useState(0);
  useEffect(() => {
    if (isAnalyzing && startTime) {
      const interval = setInterval(() => {
        setElapsedTime(Math.floor((Date.now() - startTime) / 1000));
      }, 100); // Update every 100ms for smooth display
      return () => clearInterval(interval);
    } else {
      // Reset elapsed time when not analyzing
      setElapsedTime(0);
    }
  }, [isAnalyzing, startTime]);

  const handleAnalyze = async () => {
    if (!projectPath) {
      setError("Please enter a project path");
      return;
    }

    setIsAnalyzing(true);
    setError(null);
    setAnalysisResult(null);
    setFixResult(null);
    setStartTime(Date.now());

    try {
      // Run analysis with all analyzers
      setProgressMessage("Running comprehensive documentation analysis...");
      const analyzeRequest = {
        project_path: projectPath,
        repo_type: "mintlify",
        use_claude_ai: useClaudeAI,
        claude_api_key: useClaudeAI ? apiKey : undefined,
        claude_model: useClaudeAI ? claudeModel : undefined,
        max_tokens: useClaudeAI ? maxTokens : undefined,
      };

      const result = await runAnalysis(analyzeRequest);
      setAnalysisResult(result);
      setProgressMessage("Analysis complete! Generating fixes...");

      // Automatically generate fixes after analysis
      try {
        const fixRequest = {
          project_path: projectPath,
          use_claude_ai: useClaudeAI,
          claude_api_key: useClaudeAI ? apiKey : undefined,
          claude_model: useClaudeAI ? claudeModel : undefined,
          max_tokens: useClaudeAI ? maxTokens : undefined,
        };

        const fixResult = await generateFixes(fixRequest);
        setFixResult(fixResult);
        setProgressMessage("Analysis and fix generation complete!");
      } catch (fixErr: any) {
        // Log fix generation error but don't show it as error - analysis was still successful
        console.error("Fix generation error:", fixErr);
        const errorMsg = fixErr.code === 'ECONNABORTED'
          ? "Fix generation timed out, but you can try again"
          : (fixErr.message || "Fix generation had an issue");
        setProgressMessage(`Analysis complete! ${errorMsg}`);
      }
    } catch (err: any) {
      // Extract detailed error message from backend
      const errorDetail = err.response?.data?.detail || err.message || "Analysis failed";
      setError(errorDetail);
      console.error("Analysis error:", err);
    } finally {
      setIsAnalyzing(false);
      setProgressMessage("");
      setStartTime(null);
      setElapsedTime(0); // Explicitly reset timer
    }
  };

  const handleGenerateFixes = async () => {
    if (!projectPath) {
      setError("Please enter a project path");
      return;
    }

    setIsAnalyzing(true);
    setError(null);
    setFixResult(null);
    setStartTime(Date.now());
    setProgressMessage("Generating documentation fixes...");

    try {
      const fixRequest = {
        project_path: projectPath,
        use_claude_ai: useClaudeAI,
        claude_api_key: useClaudeAI ? apiKey : undefined,
        claude_model: useClaudeAI ? claudeModel : undefined,
        max_tokens: useClaudeAI ? maxTokens : undefined,
      };

      const result = await generateFixes(fixRequest);
      setFixResult(result);
      setProgressMessage("Fix generation complete!");
    } catch (err: any) {
      const errorDetail = err.response?.data?.detail || err.message || "Fix generation failed";
      setError(errorDetail);
      console.error("Fix generation error:", err);
    } finally {
      setIsAnalyzing(false);
      setProgressMessage("");
      setStartTime(null);
      setElapsedTime(0);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <header className="mb-8">
        <h1 className="text-4xl font-bold text-foreground mb-2">
          Analyze Documentation
        </h1>
        <p className="text-muted-foreground">
          Configure analysis settings. Analysis process may take several minutes depending on project size.
        </p>
      </header>

      {/* Error Display */}
      {error && (
        <div className="bg-destructive/10 border border-destructive text-destructive rounded-lg p-4 mb-6">
          <h3 className="font-semibold mb-2">Error</h3>
          <pre className="text-sm whitespace-pre-wrap font-mono bg-destructive/5 p-3 rounded overflow-auto max-h-96">
            {error}
          </pre>
        </div>
      )}

      {/* Progress Display */}
      {isAnalyzing && (
        <div className="bg-primary/10 border border-primary rounded-lg p-4 mb-6">
          <div className="flex items-center space-x-3">
            <div className="animate-spin h-5 w-5 border-2 border-primary border-t-transparent rounded-full"></div>
            <div className="flex-1">
              <h3 className="font-semibold text-primary">{progressMessage}</h3>
              <p className="text-sm text-muted-foreground mt-1">
                Elapsed: {elapsedTime}s
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Input Section */}
      <div className="space-y-6 mb-8">
        <div className="bg-card rounded-lg border p-6">
          <h2 className="text-2xl font-semibold mb-4">Project Settings</h2>

          <div className="space-y-4">
            {/* Project Path */}
            <div>
              <label htmlFor="projectPath" className="block text-sm font-medium mb-2">
                Project Path <span className="text-destructive">*</span>
              </label>
              <input
                type="text"
                id="projectPath"
                value={projectPath}
                onChange={(e) => setProjectPath(e.target.value)}
                placeholder="/path/to/your/docs"
                className="w-full px-3 py-2 border rounded-md bg-background"
              />
              <p className="text-xs text-muted-foreground mt-1">
                Absolute path to your documentation directory
              </p>
            </div>

            {/* Claude AI Toggle */}
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="useClaudeAI"
                checked={useClaudeAI}
                onChange={(e) => setUseClaudeAI(e.target.checked)}
                className="w-4 h-4 rounded border-input cursor-pointer"
              />
              <label htmlFor="useClaudeAI" className="text-sm font-medium cursor-pointer">
                Use Claude AI for advanced analysis
              </label>
            </div>

            {/* Claude AI Settings (conditional) */}
            {useClaudeAI && (
              <>
                <div>
                  <label htmlFor="apiKey" className="block text-sm font-medium mb-2">
                    Claude API Key
                  </label>
                  <input
                    type="password"
                    id="apiKey"
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                    placeholder="sk-ant-..."
                    className="w-full px-3 py-2 border rounded-md bg-background"
                  />
                  <p className="text-xs text-muted-foreground mt-1">
                    Your API key is only stored in your session and never sent to our servers
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="claudeModel" className="block text-sm font-medium mb-2">
                      Claude Model
                    </label>
                    <select
                      id="claudeModel"
                      value={claudeModel}
                      onChange={(e) => setClaudeModel(e.target.value)}
                      className="w-full px-3 py-2 border rounded-md bg-background"
                    >
                      <option value="claude-3-5-sonnet-20241022">Claude 3.5 Sonnet (Latest)</option>
                      <option value="claude-3-5-haiku-20241022">Claude 3.5 Haiku</option>
                      <option value="claude-3-opus-20240229">Claude 3 Opus</option>
                      <option value="claude-3-sonnet-20240229">Claude 3 Sonnet</option>
                      <option value="claude-3-haiku-20240307">Claude 3 Haiku</option>
                    </select>
                  </div>

                  <div>
                    <label htmlFor="maxTokens" className="block text-sm font-medium mb-2">
                      Max Tokens
                    </label>
                    <input
                      type="number"
                      id="maxTokens"
                      value={maxTokens}
                      onChange={(e) => setMaxTokens(parseInt(e.target.value) || 4096)}
                      min="1024"
                      max="8192"
                      step="512"
                      className="w-full px-3 py-2 border rounded-md bg-background"
                    />
                    <p className="text-xs text-muted-foreground mt-1">
                      Maximum tokens per AI request (1024-8192)
                    </p>
                  </div>
                </div>
              </>
            )}
          </div>

          {/* Run Analysis button at bottom right */}
          <div className="flex justify-end mt-6">
            <button
              onClick={handleAnalyze}
              disabled={isAnalyzing || !projectPath}
              className="px-6 py-2 bg-primary text-primary-foreground rounded-md font-semibold hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isAnalyzing ? "Analyzing..." : "Run Analysis"}
            </button>
          </div>
        </div>

        {/* Info about what will be analyzed */}
        <div className="bg-card rounded-lg border p-6">
          <h2 className="text-xl font-semibold mb-4">Analysis Scope</h2>
          <div className="space-y-2 text-sm text-muted-foreground">
            <p>✓ Runs comprehensive analysis with all quality checks</p>
            <p>✓ Analyzes .mdx documentation files only</p>
            <p>✓ Excludes node_modules, build artifacts, and README files</p>
            <p>✓ Generates HTML, Markdown, and JSON reports</p>
            <p>✓ Automatically generates fixes after analysis</p>
          </div>
        </div>
      </div>

      {/* Results Section - Just buttons */}
      {(analysisResult || fixResult) && (
        <div className="bg-card rounded-lg border p-6">
          <h2 className="text-2xl font-semibold mb-4">Results</h2>
          <p className="text-muted-foreground mb-6">
            {analysisResult && !fixResult
              ? "Analysis complete! Generating fixes... You can view the analysis results while fixes are being generated."
              : "Analysis and fix generation complete! View detailed results and downloadable reports."}
          </p>

          {/* View Results Buttons */}
          <div className="flex gap-4 justify-center">
            {analysisResult && analysisResult.report_dir && (
              <button
                onClick={() => {
                  // Pass data via URL parameters for cross-tab access
                  const params = new URLSearchParams({
                    dir: analysisResult.report_dir || '',
                    files: JSON.stringify(analysisResult.report_files || {}),
                    summary: JSON.stringify(analysisResult.summary || {})
                  });
                  window.open(`/analysis-results?${params.toString()}`, '_blank');
                }}
                className="px-6 py-3 bg-primary text-primary-foreground rounded-md font-semibold hover:opacity-90 flex items-center gap-2"
              >
                View Analysis
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
              </button>
            )}
            {fixResult && fixResult.report_dir && (
              <button
                onClick={() => {
                  // Pass data via URL parameters for cross-tab access
                  const params = new URLSearchParams({
                    dir: fixResult.report_dir || '',
                    files: JSON.stringify(fixResult.report_files || {}),
                    summary: JSON.stringify(fixResult.summary || {}),
                    projectPath: projectPath
                  });
                  window.open(`/fix-results?${params.toString()}`, '_blank');
                }}
                className="px-6 py-3 bg-green-600 text-white rounded-md font-semibold hover:bg-green-700 flex items-center gap-2"
              >
                View Fixes
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
