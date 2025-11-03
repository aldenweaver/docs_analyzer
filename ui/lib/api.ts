/**
 * API client for Documentation Analyzer backend
 */

import axios from "axios";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001/api";

// Configure axios with longer timeout for large documentation analysis
// Especially important for fix generation which can take several minutes
const axiosInstance = axios.create({
  timeout: 3600000, // 60 minutes (1 hour) - generous timeout for AI-powered operations
});

export interface ModuleInfo {
  id: string;
  name: string;
  description: string;
  category: string;
}

export interface AnalyzeRequest {
  project_path: string;
  repo_type?: string;
  enabled_analyzers?: string[];
  use_claude_ai?: boolean;
  claude_api_key?: string;
  claude_model?: string;
  max_tokens?: number;
}

export interface AnalyzeResponse {
  summary: {
    total_issues: number;
    files_analyzed: number;
    [key: string]: any;
  };
  issues: any[];
  raw_output?: string;
  report_dir?: string;
  report_files?: {
    json: string;
    html: string;
    markdown: string;
  };
}

export interface FixRequest {
  project_path: string;
  enabled_fixers?: string[];
  use_claude_ai?: boolean;
  claude_api_key?: string;
  claude_model?: string;
  max_tokens?: number;
}

export interface FixResponse {
  summary: {
    total_fixes: number;
    files_modified: number;
    [key: string]: any;
  };
  fixes: any[];
  raw_output?: string;
  report_dir?: string;
  report_files?: {
    json: string;
    html: string;
    markdown: string;
  };
}

/**
 * Fetch available analyzer modules
 */
export async function getAnalyzers(): Promise<ModuleInfo[]> {
  const response = await axiosInstance.get(`${API_BASE}/analyzers`);
  return response.data;
}

/**
 * Fetch available fixer modules
 */
export async function getFixers(): Promise<ModuleInfo[]> {
  const response = await axiosInstance.get(`${API_BASE}/fixers`);
  return response.data;
}

/**
 * Run documentation analysis
 */
export async function runAnalysis(
  request: AnalyzeRequest
): Promise<AnalyzeResponse> {
  const response = await axiosInstance.post(`${API_BASE}/analyze`, request);
  return response.data;
}

/**
 * Generate fixes in dry-run mode
 */
export async function generateFixes(request: FixRequest): Promise<FixResponse> {
  const response = await axiosInstance.post(`${API_BASE}/fix`, request);
  return response.data;
}
