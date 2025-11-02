import { test, expect } from '@playwright/test';
import * as fs from 'fs';
import * as path from 'path';

// Use the same test docs directory
const TEST_DOCS_DIR = path.join(process.cwd(), '../test_docs');

test.describe('Bug Fix Verification', () => {
  test('Files Analyzed should display correct count (not 0)', async ({ page }) => {
    // Navigate to the app
    await page.goto('http://localhost:3001');

    // Wait for page to load
    await expect(page).toHaveTitle('Documentation Analyzer');

    // Enter project path
    const projectPathField = page.locator('#projectPath');
    await projectPathField.fill(TEST_DOCS_DIR);

    // Click Run Analysis
    const runButton = page.locator('button:text("Run Analysis")');
    await runButton.click();

    // Wait for analysis to start (should show progress)
    await expect(page.locator('text=Running comprehensive documentation analysis')).toBeVisible({ timeout: 5000 });

    // Wait for analysis to complete with longer timeout
    const analysisCompleteLocator = page.locator('text=Analysis complete!');
    try {
      await expect(analysisCompleteLocator).toBeVisible({ timeout: 30000 });
    } catch (error) {
      // If "Analysis complete!" doesn't appear, check if results are shown anyway
      const resultsHeader = page.locator('h2:text("Results")');
      await expect(resultsHeader).toBeVisible({ timeout: 5000 });
    }

    // Check that Files Analyzed shows a number greater than 0
    const filesAnalyzedCard = page.locator('text=Files Analyzed').locator('..');
    await expect(filesAnalyzedCard).toBeVisible();

    const filesCount = await filesAnalyzedCard.locator('.text-3xl').textContent();
    console.log('Files Analyzed displays:', filesCount);

    // The count should be 4 (we created 4 test files)
    expect(parseInt(filesCount || '0')).toBeGreaterThan(0);
    expect(parseInt(filesCount || '0')).toBe(4);

    // Also check Total Issues
    const totalIssuesCard = page.locator('text=Total Issues').locator('..');
    const issuesCount = await totalIssuesCard.locator('.text-3xl').textContent();
    console.log('Total Issues displays:', issuesCount);
    expect(parseInt(issuesCount || '0')).toBeGreaterThan(0);

    // Navigate to Analysis Results page
    const viewResultsButton = page.locator('button:text("View Analysis Results")');
    await expect(viewResultsButton).toBeVisible();
    await viewResultsButton.click();

    // Should navigate to results page
    await expect(page).toHaveURL(/analysis-results/);

    // Check Files Analyzed on results page too
    const filesOnResultsPage = await page.locator('text=Files Analyzed').locator('..').locator('.text-3xl').textContent();
    console.log('Files Analyzed on results page:', filesOnResultsPage);
    expect(parseInt(filesOnResultsPage || '0')).toBe(4);
  });

  test('API response should include total_files in summary', async ({ page, request }) => {
    // Make direct API call to verify response structure
    const response = await request.post('http://localhost:8001/api/analyze', {
      data: {
        project_path: TEST_DOCS_DIR,
        repo_type: 'mintlify'
      }
    });

    expect(response.status()).toBe(200);

    const data = await response.json();
    console.log('API Response Summary:', data.summary);

    // Verify API returns total_files
    expect(data.summary).toHaveProperty('total_files');
    expect(data.summary.total_files).toBeGreaterThan(0);
    expect(data.summary.total_files).toBe(4);

    // Verify API returns total_issues
    expect(data.summary).toHaveProperty('total_issues');
    expect(data.summary.total_issues).toBeGreaterThan(0);
  });

  test('UI correctly parses API response data', async ({ page }) => {
    // Navigate and start analysis
    await page.goto('http://localhost:3001');

    const projectPathField = page.locator('#projectPath');
    await projectPathField.fill(TEST_DOCS_DIR);

    // Intercept the API response to verify UI parsing
    let apiResponseData: any = null;

    page.on('response', async (response) => {
      if (response.url().includes('/api/analyze') && response.status() === 200) {
        apiResponseData = await response.json();
      }
    });

    const runButton = page.locator('button:text("Run Analysis")');
    await runButton.click();

    // Wait for response to be captured
    await page.waitForTimeout(5000);

    // Wait for UI to update
    const resultsSection = page.locator('h2:text("Results")');
    await expect(resultsSection).toBeVisible({ timeout: 30000 });

    if (apiResponseData) {
      console.log('Captured API Response:', {
        total_files: apiResponseData.summary?.total_files,
        total_issues: apiResponseData.summary?.total_issues
      });

      // Verify UI displays the same values as API response
      const filesAnalyzedCard = page.locator('text=Files Analyzed').locator('..');
      const filesCount = await filesAnalyzedCard.locator('.text-3xl').textContent();

      expect(parseInt(filesCount || '0')).toBe(apiResponseData.summary.total_files);

      const totalIssuesCard = page.locator('text=Total Issues').locator('..');
      const issuesCount = await totalIssuesCard.locator('.text-3xl').textContent();

      expect(parseInt(issuesCount || '0')).toBe(apiResponseData.summary.total_issues);
    }
  });
});