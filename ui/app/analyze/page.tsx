"use client";

import { useState, useEffect } from "react";
import ModuleSelector, { type Module } from "@/components/ModuleSelector";
import { getAnalyzers, getFixers, runAnalysis, generateFixes } from "@/lib/api";

export default function AnalyzePage() {
  // State for modules
  const [analyzers, setAnalyzers] = useState<Module[]>([]);
  const [fixers, setFixers] = useState<Module[]>([]);
  const [selectedAnalyzers, setSelectedAnalyzers] = useState<string[]>([]);
  const [selectedFixers, setSelectedFixers] = useState<string[]>([]);

  // State for form inputs
  const [projectPath, setProjectPath] = useState("");
  const [useClaudeAI, setUseClaudeAI] = useState(false);
  const [apiKey, setApiKey] = useState("");

  // State for analysis
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [fixResult, setFixResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  // Load modules on mount
  useEffect(() => {
    loadModules();
  }, []);

  const loadModules = async () => {
    try {
      const [analyzersData, fixersData] = await Promise.all([
        getAnalyzers(),
        getFixers(),
      ]);
      setAnalyzers(analyzersData);
      setFixers(fixersData);

      // Select all by default
      setSelectedAnalyzers(analyzersData.map((a) => a.id));
      setSelectedFixers(fixersData.map((f) => f.id));
    } catch (err) {
      setError("Failed to load modules. Is the backend running?");
      console.error(err);
    }
  };

  const handleAnalyze = async () => {
    if (!projectPath) {
      setError("Please enter a project path");
      return;
    }

    setIsAnalyzing(true);
    setError(null);
    setAnalysisResult(null);
    setFixResult(null);

    try {
      // Run analysis
      const analyzeRequest = {
        project_path: projectPath,
        repo_type: "mintlify",
        enabled_analyzers: selectedAnalyzers,
        use_claude_ai: useClaudeAI,
        claude_api_key: useClaudeAI ? apiKey : undefined,
      };

      const result = await runAnalysis(analyzeRequest);
      setAnalysisResult(result);

      // Run fixes if any fixers are selected
      if (selectedFixers.length > 0) {
        const fixRequest = {
          project_path: projectPath,
          enabled_fixers: selectedFixers,
          use_claude_ai: useClaudeAI,
          claude_api_key: useClaudeAI ? apiKey : undefined,
        };

        const fixes = await generateFixes(fixRequest);
        setFixResult(fixes);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || "Analysis failed");
      console.error(err);
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <header className="mb-8">
        <h1 className="text-4xl font-bold text-foreground mb-2">
          Analyze Documentation
        </h1>
        <p className="text-muted-foreground">
          Configure analysis settings and select modules to run
        </p>
      </header>

      {/* Error Display */}
      {error && (
        <div className="bg-destructive/10 border border-destructive text-destructive rounded-lg p-4 mb-6">
          <h3 className="font-semibold mb-1">Error</h3>
          <p className="text-sm">{error}</p>
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

            {/* API Key (conditional) */}
            {useClaudeAI && (
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
            )}
          </div>
        </div>

        {/* Module Selectors */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <ModuleSelector
            title="Analyzers"
            modules={analyzers}
            selectedModules={selectedAnalyzers}
            onSelectionChange={setSelectedAnalyzers}
          />

          <ModuleSelector
            title="Fixers"
            modules={fixers}
            selectedModules={selectedFixers}
            onSelectionChange={setSelectedFixers}
          />
        </div>

        {/* Run Button */}
        <div className="flex justify-center">
          <button
            onClick={handleAnalyze}
            disabled={isAnalyzing || !projectPath}
            className="px-8 py-3 bg-primary text-primary-foreground rounded-md font-semibold hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isAnalyzing ? "Analyzing..." : "Run Analysis"}
          </button>
        </div>
      </div>

      {/* Results Section */}
      {(analysisResult || fixResult) && (
        <div className="space-y-6">
          <h2 className="text-2xl font-semibold">Results</h2>

          {/* Analysis Results */}
          {analysisResult && (
            <div className="bg-card rounded-lg border p-6">
              <h3 className="text-xl font-semibold mb-4">Analysis Summary</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div>
                  <div className="text-2xl font-bold text-primary">
                    {analysisResult.summary?.total_issues || 0}
                  </div>
                  <div className="text-sm text-muted-foreground">Total Issues</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-primary">
                    {analysisResult.summary?.files_analyzed || 0}
                  </div>
                  <div className="text-sm text-muted-foreground">Files Analyzed</div>
                </div>
              </div>

              {analysisResult.raw_output && (
                <details className="mt-4">
                  <summary className="cursor-pointer text-sm font-medium text-primary">
                    View raw output
                  </summary>
                  <pre className="mt-2 p-4 bg-secondary rounded-md text-xs overflow-auto max-h-96">
                    {analysisResult.raw_output}
                  </pre>
                </details>
              )}
            </div>
          )}

          {/* Fix Results */}
          {fixResult && (
            <div className="bg-card rounded-lg border p-6">
              <h3 className="text-xl font-semibold mb-4">Generated Fixes</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div>
                  <div className="text-2xl font-bold text-primary">
                    {fixResult.summary?.total_fixes || 0}
                  </div>
                  <div className="text-sm text-muted-foreground">Total Fixes</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-primary">
                    {fixResult.summary?.files_modified || 0}
                  </div>
                  <div className="text-sm text-muted-foreground">Files Modified</div>
                </div>
              </div>

              {fixResult.raw_output && (
                <details className="mt-4">
                  <summary className="cursor-pointer text-sm font-medium text-primary">
                    View raw output
                  </summary>
                  <pre className="mt-2 p-4 bg-secondary rounded-md text-xs overflow-auto max-h-96">
                    {fixResult.raw_output}
                  </pre>
                </details>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
