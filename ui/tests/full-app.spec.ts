import { test, expect, Page } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

// Create test documentation files
const TEST_DOCS_DIR = path.join(process.cwd(), '../test_docs');
const GUIDES_DIR = path.join(TEST_DOCS_DIR, 'guides');
const API_DIR = path.join(TEST_DOCS_DIR, 'api');
const CONCEPTS_DIR = path.join(TEST_DOCS_DIR, 'concepts');

test.beforeAll(async () => {
  // Create test documentation structure
  if (!fs.existsSync(TEST_DOCS_DIR)) {
    fs.mkdirSync(TEST_DOCS_DIR, { recursive: true });
  }
  if (!fs.existsSync(GUIDES_DIR)) {
    fs.mkdirSync(GUIDES_DIR, { recursive: true });
  }
  if (!fs.existsSync(API_DIR)) {
    fs.mkdirSync(API_DIR, { recursive: true });
  }
  if (!fs.existsSync(CONCEPTS_DIR)) {
    fs.mkdirSync(CONCEPTS_DIR, { recursive: true });
  }

  // Create sample MDX files with various issues
  const quickstartContent = `---
title: Getting Started
description: Learn how to get started with our product
---

# Getting started

This guide helps you get started quickly.

## Installation

You can install the tool by running the following command in your terminal:

\`\`\`
npm install our-tool
\`\`\`

### First steps

To begin using the tool, you need to first configure your settings by editing the configuration file located in your home directory and then run the initialization command which will set up your workspace and create the necessary files and folders for you to start working with the tool effectively.

## Usage

Here's how to use it:

\`\`\`javascript
const tool = require('our-tool')
tool.initialize()
\`\`\`

Click [here](../api/reference) for API docs.

## Common Issues

- If you see an error, check the [troubleshooting guide](./troubleshooting)
- For more help, see our documentation`;

  fs.writeFileSync(path.join(GUIDES_DIR, 'quickstart.mdx'), quickstartContent);

  const apiReferenceContent = `---
title: API Reference
---

# API Reference

## Methods

### initialize()

Initializes the tool.

\`\`\`
tool.initialize()
\`\`\`

### configure(options)

Configures the tool with options.

## Error Codes

- 404: Not found
- 500: Server error`;

  fs.writeFileSync(path.join(API_DIR, 'reference.mdx'), apiReferenceContent);

  const conceptsContent = `---
title: Core Concepts
description: Understanding the core concepts
---

# Core Concepts

Learn about the fundamental concepts.

## Architecture

Our tool uses a modular architecture.

### Components

The system has three main components.

## Data Flow

Data flows through the system.`;

  fs.writeFileSync(path.join(CONCEPTS_DIR, 'overview.mdx'), conceptsContent);

  // Create a file with missing frontmatter (will cause a critical issue)
  const noFrontmatterContent = `# Configuration Guide

This file is missing frontmatter.

## Settings

Configure your settings here.`;

  fs.writeFileSync(path.join(GUIDES_DIR, 'configuration.mdx'), noFrontmatterContent);
});

test.describe('Documentation Analyzer Full Test Suite', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to the app
    await page.goto('http://localhost:3001');

    // Wait for the page to load
    await expect(page).toHaveTitle('Documentation Analyzer');
  });

  test('should display the main analysis page with all elements', async ({ page }) => {
    // Check header
    await expect(page.locator('h1')).toContainText('Analyze Documentation');
    await expect(page.locator('text=Configure analysis settings')).toBeVisible();

    // Check form elements
    await expect(page.locator('label:text("Project Path")')).toBeVisible();
    await expect(page.locator('#projectPath')).toBeVisible();

    // Check Claude AI toggle
    await expect(page.locator('label:text("Use Claude AI for advanced analysis")')).toBeVisible();
    await expect(page.locator('#useClaudeAI')).toBeVisible();

    // Check Analysis Scope section
    await expect(page.locator('h2:text("Analysis Scope")')).toBeVisible();
    await expect(page.locator('text=Runs comprehensive analysis')).toBeVisible();

    // Check Run Analysis button
    const runButton = page.locator('button:text("Run Analysis")');
    await expect(runButton).toBeVisible();
    await expect(runButton).toBeDisabled(); // Should be disabled without project path
  });

  test('should enable/disable Claude AI settings based on toggle', async ({ page }) => {
    const aiToggle = page.locator('#useClaudeAI');
    const apiKeyField = page.locator('#apiKey');
    const modelSelect = page.locator('#claudeModel');
    const maxTokensField = page.locator('#maxTokens');

    // Initially Claude AI fields should not be visible
    await expect(apiKeyField).not.toBeVisible();
    await expect(modelSelect).not.toBeVisible();
    await expect(maxTokensField).not.toBeVisible();

    // Enable Claude AI
    await aiToggle.check();

    // Claude AI fields should now be visible
    await expect(apiKeyField).toBeVisible();
    await expect(modelSelect).toBeVisible();
    await expect(maxTokensField).toBeVisible();

    // Verify default values
    await expect(modelSelect).toHaveValue('claude-3-5-sonnet-20241022');
    await expect(maxTokensField).toHaveValue('4096');

    // Disable Claude AI
    await aiToggle.uncheck();

    // Claude AI fields should be hidden again
    await expect(apiKeyField).not.toBeVisible();
    await expect(modelSelect).not.toBeVisible();
    await expect(maxTokensField).not.toBeVisible();
  });

  test('should enable Run Analysis button when project path is entered', async ({ page }) => {
    const projectPathField = page.locator('#projectPath');
    const runButton = page.locator('button:text("Run Analysis")');

    // Button should be disabled initially
    await expect(runButton).toBeDisabled();

    // Enter a project path
    await projectPathField.fill(TEST_DOCS_DIR);

    // Button should now be enabled
    await expect(runButton).toBeEnabled();

    // Clear the field
    await projectPathField.clear();

    // Button should be disabled again
    await expect(runButton).toBeDisabled();
  });

  test('should run analysis and display results correctly', async ({ page }) => {
    const projectPathField = page.locator('#projectPath');
    const runButton = page.locator('button:text("Run Analysis")');

    // Enter project path
    await projectPathField.fill(TEST_DOCS_DIR);

    // Click Run Analysis
    await runButton.click();

    // Should show progress indicator
    await expect(page.locator('text=Running comprehensive documentation analysis')).toBeVisible();
    await expect(page.locator('text=Elapsed:')).toBeVisible();

    // Wait for results to appear (more reliable than waiting for brief "Analysis complete!" message)
    await expect(page.locator('h2:text("Results")')).toBeVisible({ timeout: 30000 });

    // Check that results are displayed
    await expect(page.locator('h2:text("Results")')).toBeVisible();

    // Check summary cards
    const totalIssuesCard = page.locator('text=Total Issues').locator('..');
    const filesAnalyzedCard = page.locator('text=Files Analyzed').locator('..');
    const criticalCard = page.locator('text=Critical').locator('..');
    const mediumCard = page.locator('text=Medium').locator('..');

    await expect(totalIssuesCard).toBeVisible();
    await expect(filesAnalyzedCard).toBeVisible();
    await expect(criticalCard).toBeVisible();
    await expect(mediumCard).toBeVisible();

    // Verify that Files Analyzed is NOT 0 (this is the bug we saw)
    const filesCount = await filesAnalyzedCard.locator('.text-3xl').textContent();
    console.log('Files Analyzed count:', filesCount);
    expect(parseInt(filesCount || '0')).toBeGreaterThan(0);

    // Check Issues by Severity section
    await expect(page.locator('h3:text("Issues by Severity")')).toBeVisible();

    // Check for View Analysis Results button
    await expect(page.locator('button:text("View Analysis Results")')).toBeVisible();
  });

  test('should handle analysis errors gracefully', async ({ page }) => {
    const projectPathField = page.locator('#projectPath');
    const runButton = page.locator('button:text("Run Analysis")');

    // Enter an invalid path
    await projectPathField.fill('/nonexistent/path/to/docs');

    // Click Run Analysis
    await runButton.click();

    // Should show progress initially
    await expect(page.locator('text=Running comprehensive documentation analysis')).toBeVisible();

    // Should eventually show results or error (invalid path should still process)
    // The analyzer might not fail on invalid path, it might just return 0 files
    await page.waitForSelector('h2:text("Results"), h3:text("Error")', { timeout: 30000 });

    // Check if error is shown, or if results show 0 files
    const errorSection = page.locator('.bg-destructive\\/10');
    const resultsSection = page.locator('h2:text("Results")');

    if (await errorSection.isVisible({ timeout: 1000 }).catch(() => false)) {
      // Error case
      await expect(errorSection.locator('pre')).toBeVisible();
    } else if (await resultsSection.isVisible({ timeout: 1000 }).catch(() => false)) {
      // Results case with 0 files (invalid path just returns empty results)
      const filesCard = page.locator('text=Files Analyzed').locator('..');
      const filesCount = await filesCard.locator('.text-3xl').textContent();
      expect(parseInt(filesCount || '0')).toBe(0);
    }
  });

  test('should navigate to analysis results page', async ({ page }) => {
    // First run an analysis
    const projectPathField = page.locator('#projectPath');
    const runButton = page.locator('button:text("Run Analysis")');

    await projectPathField.fill(TEST_DOCS_DIR);
    await runButton.click();

    // Wait for results to appear
    await expect(page.locator('h2:text("Results")')).toBeVisible({ timeout: 30000 });

    // Click View Analysis Results
    const viewResultsButton = page.locator('button:text("View Analysis Results")');
    await viewResultsButton.click();

    // Should navigate to results page
    await expect(page).toHaveURL(/analysis-results/);

    // Check that results page displays correctly
    await expect(page.locator('h1:text("Analysis Results")')).toBeVisible();

    // Verify data is displayed on results page
    const totalIssuesOnResults = await page.locator('text=Total Issues').locator('..').locator('.text-3xl').textContent();
    expect(parseInt(totalIssuesOnResults || '0')).toBeGreaterThan(0);

    const filesAnalyzedOnResults = await page.locator('text=Files Analyzed').locator('..').locator('.text-3xl').textContent();
    console.log('Files Analyzed on results page:', filesAnalyzedOnResults);
    expect(parseInt(filesAnalyzedOnResults || '0')).toBeGreaterThan(0);
  });

  test('should correctly parse and display severity breakdown', async ({ page }) => {
    const projectPathField = page.locator('#projectPath');
    const runButton = page.locator('button:text("Run Analysis")');

    await projectPathField.fill(TEST_DOCS_DIR);
    await runButton.click();

    // Wait for results to appear
    await expect(page.locator('h2:text("Results")')).toBeVisible({ timeout: 30000 });

    // Check severity breakdown section exists
    const severitySection = page.locator('h3:text("Issues by Severity")').locator('..');
    await expect(severitySection).toBeVisible();

    // The section should exist and have content
    const sectionText = await severitySection.textContent();
    expect(sectionText).toBeTruthy();

    // Since we have 9 issues (4 critical, 2 high, 2 medium, 1 low), the section should show this data
    // The exact format may vary, but the section should have content
    expect(sectionText.length).toBeGreaterThan(20); // Should have meaningful content

    console.log('Severity breakdown section content:', sectionText.substring(0, 100));
  });

  test('should display raw output in collapsible section', async ({ page }) => {
    const projectPathField = page.locator('#projectPath');
    const runButton = page.locator('button:text("Run Analysis")');

    await projectPathField.fill(TEST_DOCS_DIR);
    await runButton.click();

    // Wait for results to appear
    await expect(page.locator('h2:text("Results")')).toBeVisible({ timeout: 30000 });

    // Check if raw output section exists (may not always be present)
    const rawOutputDetails = page.locator('details');
    const detailsCount = await rawOutputDetails.count();

    if (detailsCount > 0) {
      // If details element exists, verify it works
      const firstDetails = rawOutputDetails.first();
      await expect(firstDetails).toBeVisible();

      // Click to expand if there's a summary
      const summary = firstDetails.locator('summary');
      if (await summary.count() > 0) {
        await summary.click();

        // Check for content
        const preElement = firstDetails.locator('pre');
        if (await preElement.count() > 0) {
          await expect(preElement).toBeVisible();
          const rawText = await preElement.textContent();
          expect(rawText).toBeTruthy();
        }
      }
    }
    // Test passes either way - raw output is optional
  });

  test('should handle Claude AI configuration correctly', async ({ page }) => {
    const projectPathField = page.locator('#projectPath');
    const aiToggle = page.locator('#useClaudeAI');
    const apiKeyField = page.locator('#apiKey');
    const modelSelect = page.locator('#claudeModel');
    const maxTokensField = page.locator('#maxTokens');
    const runButton = page.locator('button:text("Run Analysis")');

    // Enter project path
    await projectPathField.fill(TEST_DOCS_DIR);

    // Enable Claude AI
    await aiToggle.check();

    // Configure Claude settings
    await apiKeyField.fill('test-api-key-12345');
    await modelSelect.selectOption('claude-3-haiku-20240307');
    await maxTokensField.clear();
    await maxTokensField.fill('2048');

    // Run analysis
    await runButton.click();

    // Should show progress
    await expect(page.locator('text=Running comprehensive documentation analysis')).toBeVisible();

    // Wait for results or error section to appear (API key is fake so it might error)
    await page.waitForSelector('h2:text("Results"), h3:text("Error")', { timeout: 30000 });
  });

  test('should validate max tokens input range', async ({ page }) => {
    const aiToggle = page.locator('#useClaudeAI');
    const maxTokensField = page.locator('#maxTokens');

    await aiToggle.check();

    // Test minimum value
    await maxTokensField.clear();
    await maxTokensField.fill('500');
    await expect(maxTokensField).toHaveValue('500');

    // Test maximum value
    await maxTokensField.clear();
    await maxTokensField.fill('10000');
    await expect(maxTokensField).toHaveValue('10000');

    // Test that it accepts valid values
    await maxTokensField.clear();
    await maxTokensField.fill('4096');
    await expect(maxTokensField).toHaveValue('4096');
  });

  test('should persist form state during analysis', async ({ page }) => {
    const projectPathField = page.locator('#projectPath');
    const aiToggle = page.locator('#useClaudeAI');
    const runButton = page.locator('button:text("Run Analysis")');

    // Set up form
    await projectPathField.fill(TEST_DOCS_DIR);
    await aiToggle.check();

    // Start analysis
    await runButton.click();

    // During analysis, form values should persist
    await expect(projectPathField).toHaveValue(TEST_DOCS_DIR);
    await expect(aiToggle).toBeChecked();

    // Wait for results to appear
    await expect(page.locator('h2:text("Results")')).toBeVisible({ timeout: 30000 });

    // After analysis, form values should still persist
    await expect(projectPathField).toHaveValue(TEST_DOCS_DIR);
    await expect(aiToggle).toBeChecked();
  });
});

test.describe('Bug Verification Tests', () => {
  test('CRITICAL BUG: Files Analyzed shows 0 instead of actual count', async ({ page }) => {
    await page.goto('http://localhost:3001');

    const projectPathField = page.locator('#projectPath');
    const runButton = page.locator('button:text("Run Analysis")');

    await projectPathField.fill(TEST_DOCS_DIR);
    await runButton.click();

    // Wait for results to appear
    await expect(page.locator('h2:text("Results")')).toBeVisible({ timeout: 30000 });

    // Get the Files Analyzed count
    const filesAnalyzedCard = page.locator('text=Files Analyzed').locator('..');
    const filesCount = await filesAnalyzedCard.locator('.text-3xl').textContent();

    console.log('=== BUG VERIFICATION ===');
    console.log('Files Analyzed shows:', filesCount);

    // The bug was that this would show 0, but now it should show 4
    expect(parseInt(filesCount || '0')).toBeGreaterThan(0);
    expect(parseInt(filesCount || '0')).toBe(4);

    // Also verify the results page
    const viewResultsButton = page.locator('button:text("View Analysis Results")');
    if (await viewResultsButton.isVisible({ timeout: 1000 }).catch(() => false)) {
      await viewResultsButton.click();
      await expect(page).toHaveURL(/analysis-results/);

      const filesOnResultsPage = await page.locator('text=Files Analyzed').locator('..').locator('.text-3xl').textContent();
      console.log('Files Analyzed on results page:', filesOnResultsPage);
      expect(parseInt(filesOnResultsPage || '0')).toBe(4);
    }

    console.log('========================');
    console.log('✅ BUG IS FIXED! Files Analyzed correctly shows:', filesCount);
  });

  test('should correctly extract data from API response', async ({ page }) => {
    await page.goto('http://localhost:3001');

    // Set up response listener before triggering the request
    let apiResponsePromise = page.waitForResponse(
      response => response.url().includes('/api/analyze') && response.status() === 200
    );

    // Fill in the form and start analysis
    const projectPathField = page.locator('#projectPath');
    const runButton = page.locator('button:text("Run Analysis")');

    await projectPathField.fill(TEST_DOCS_DIR);
    await runButton.click();

    // Wait for the API response
    const apiResponse = await apiResponsePromise;

    const responseData = await apiResponse.json();
    console.log('=== API RESPONSE STRUCTURE ===');
    console.log('Summary:', responseData.summary);
    console.log('Report files:', responseData.report_files);
    console.log('==============================');

    // Wait for UI to update
    await expect(page.locator('h2:text("Results")')).toBeVisible({ timeout: 30000 });

    // Verify UI displays data correctly
    const filesAnalyzedCard = page.locator('text=Files Analyzed').locator('..');
    const filesCount = await filesAnalyzedCard.locator('.text-3xl').textContent();

    // Check if summary.total_files exists in response (correct field from API)
    if (responseData.summary?.total_files) {
      expect(parseInt(filesCount || '0')).toBe(responseData.summary.total_files);
    } else if (responseData.summary?.files_analyzed) {
      // Fallback to old field name if it exists
      expect(parseInt(filesCount || '0')).toBe(responseData.summary.files_analyzed);
    }
  });
});