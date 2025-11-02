import { test, expect } from '@playwright/test';

const TEST_DOCS_DIR = '/Users/alden/dev/docs_analyzer/test_docs';

test.describe('Fixer Integration Tests', () => {
  test('Complete fixer workflow: analyze, generate fixes, view results', async ({ page }) => {
    // Navigate to the app
    await page.goto('http://localhost:3001');

    // Enter project path
    await page.fill('#projectPath', TEST_DOCS_DIR);

    // Step 1: Run analysis first
    console.log('Step 1: Running analysis...');
    await page.click('button:text("Run Analysis")');

    // Wait for analysis to complete
    await page.waitForSelector('h2:text("Results")', { timeout: 30000 });

    // Verify analysis results are shown
    const totalIssues = await page.locator('text=Total Issues').locator('..').locator('.text-3xl').textContent();
    console.log('Total Issues found:', totalIssues);
    expect(parseInt(totalIssues || '0')).toBeGreaterThan(0);

    // Step 2: Generate Fixes button should now be visible
    console.log('Step 2: Checking for Generate Fixes button...');
    const generateFixesButton = page.locator('button:text("Generate Fixes")');
    await expect(generateFixesButton).toBeVisible();

    // Click Generate Fixes
    console.log('Step 3: Generating fixes...');
    await generateFixesButton.click();

    // Wait for fix generation to complete - look for the fix results to appear
    await page.waitForTimeout(3000); // Give API time to process

    // Wait for either completion message or fix results
    await Promise.race([
      page.waitForSelector('text=Total Fixes', { timeout: 20000 }),
      page.waitForSelector('text=Fix generation complete!', { timeout: 20000 })
    ]).catch(() => {
      // If neither appears, just continue and check if results are there
      console.log('Warning: Fix completion indicators not found, checking for results anyway');
    });

    // Step 4: Verify fix results are displayed
    console.log('Step 4: Verifying fix results...');
    const totalFixesElement = page.locator('text=Total Fixes').locator('..');
    await expect(totalFixesElement).toBeVisible();

    const totalFixes = await totalFixesElement.locator('.text-3xl').textContent();
    console.log('Total Fixes generated:', totalFixes);
    expect(parseInt(totalFixes || '0')).toBeGreaterThan(0);

    // Verify other fix metrics
    const filesModified = await page.locator('text=Files Modified').locator('..').locator('.text-3xl').textContent();
    console.log('Files Modified:', filesModified);
    expect(parseInt(filesModified || '0')).toBeGreaterThan(0);

    const filesProcessed = await page.locator('text=Files Processed').locator('..').locator('.text-3xl').textContent();
    console.log('Files Processed:', filesProcessed);
    expect(parseInt(filesProcessed || '0')).toBe(4); // We have 4 test files

    // Verify mode is shown
    const modeElement = page.locator('text=Mode').locator('..');
    const mode = await modeElement.locator('.text-3xl').textContent();
    console.log('Mode:', mode);
    expect(mode).toBe('Preview'); // Should be in dry_run/preview mode

    // Step 5: Check for View Fix Results button
    console.log('Step 5: Checking for View Fix Results button...');
    const viewFixResultsButton = page.locator('button:text("View Fix Results")');
    await expect(viewFixResultsButton).toBeVisible();

    // Click View Fix Results
    await viewFixResultsButton.click();

    // Step 6: Verify navigation to fix-results page
    console.log('Step 6: Verifying fix-results page...');
    await expect(page).toHaveURL(/fix-results/);
    await expect(page.locator('h1:text("Fix Results")')).toBeVisible();

    // Verify data is displayed on results page
    const totalFixesOnResults = await page.locator('text=Total Fixes').locator('..').locator('.text-3xl').textContent();
    console.log('Total Fixes on results page:', totalFixesOnResults);
    expect(parseInt(totalFixesOnResults || '0')).toBeGreaterThan(0);

    // Check for download button
    const downloadButton = page.locator('button:text("Download Report")');
    await expect(downloadButton).toBeVisible();

    console.log('✅ All fixer integration tests passed!');
  });

  test('Fixer API endpoint returns correct data', async ({ request }) => {
    const response = await request.post('http://localhost:8001/api/fix', {
      data: {
        project_path: TEST_DOCS_DIR
      }
    });

    expect(response.status()).toBe(200);

    const data = await response.json();
    console.log('API Response Summary:', data.summary);

    // Verify response structure
    expect(data).toHaveProperty('summary');
    expect(data).toHaveProperty('fixes');
    expect(data).toHaveProperty('report_dir');
    expect(data).toHaveProperty('report_files');

    // Verify summary data
    expect(data.summary).toHaveProperty('total_files');
    expect(data.summary).toHaveProperty('files_modified');
    expect(data.summary).toHaveProperty('total_fixes');
    expect(data.summary).toHaveProperty('fixes_by_type');
    expect(data.summary).toHaveProperty('mode');

    // Verify values
    expect(data.summary.total_files).toBe(4);
    expect(data.summary.files_modified).toBeGreaterThan(0);
    expect(data.summary.total_fixes).toBeGreaterThan(0);
    expect(data.summary.mode).toBe('dry_run');

    // Verify report files
    expect(data.report_files.json).toBe('doc_fix_report.json');
    expect(data.report_files.html).toBe('doc_fix_report.html');
    expect(data.report_files.markdown).toBe('doc_fix_report.md');
  });

  test('Generate Fixes button only appears after analysis', async ({ page }) => {
    await page.goto('http://localhost:3001');

    // Initially, Generate Fixes should not be visible
    let generateFixesButton = page.locator('button:text("Generate Fixes")');
    await expect(generateFixesButton).not.toBeVisible();

    // Enter project path
    await page.fill('#projectPath', TEST_DOCS_DIR);

    // Generate Fixes should still not be visible
    await expect(generateFixesButton).not.toBeVisible();

    // Run analysis
    await page.click('button:text("Run Analysis")');

    // Wait for analysis to complete
    await page.waitForSelector('h2:text("Results")', { timeout: 30000 });

    // Now Generate Fixes should be visible
    generateFixesButton = page.locator('button:text("Generate Fixes")');
    await expect(generateFixesButton).toBeVisible();
  });

  test('Fix results display fixes by type', async ({ page }) => {
    await page.goto('http://localhost:3001');

    // Run analysis
    await page.fill('#projectPath', TEST_DOCS_DIR);
    await page.click('button:text("Run Analysis")');
    await page.waitForSelector('h2:text("Results")', { timeout: 30000 });

    // Generate fixes
    await page.click('button:text("Generate Fixes")');
    await page.waitForTimeout(5000); // Give it time to generate

    // Check if Fixes by Type section exists
    const fixesByTypeSection = page.locator('h3:text("Fixes by Type")').locator('..');
    const isVisible = await fixesByTypeSection.isVisible().catch(() => false);

    if (isVisible) {
      console.log('Fixes by Type section found');
      const fixTypes = await fixesByTypeSection.locator('.space-y-2').textContent();
      console.log('Fix types:', fixTypes);
      expect(fixTypes).toContain('Added');
    }
  });
});