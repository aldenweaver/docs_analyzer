/**
 * API client for Documentation Analyzer backend
 */

import axios from "axios";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "/api/backend";

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
}

/**
 * Fetch available analyzer modules
 */
export async function getAnalyzers(): Promise<ModuleInfo[]> {
  const response = await axios.get(`${API_BASE}/analyzers`);
  return response.data;
}

/**
 * Fetch available fixer modules
 */
export async function getFixers(): Promise<ModuleInfo[]> {
  const response = await axios.get(`${API_BASE}/fixers`);
  return response.data;
}

/**
 * Run documentation analysis
 */
export async function runAnalysis(
  request: AnalyzeRequest
): Promise<AnalyzeResponse> {
  const response = await axios.post(`${API_BASE}/analyze`, request);
  return response.data;
}

/**
 * Generate fixes in dry-run mode
 */
export async function generateFixes(request: FixRequest): Promise<FixResponse> {
  const response = await axios.post(`${API_BASE}/fix`, request);
  return response.data;
}
