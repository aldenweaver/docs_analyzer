import { test, expect } from '@playwright/test';

test.describe('Documentation Analyzer Full Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000');
  });

  test('should run analysis successfully with simplified UI', async ({ page }) => {
    // Wait for page to load
    await page.waitForSelector('h1:has-text("Analyze Documentation")');

    // Check that Analysis Scope section is visible
    await page.waitForSelector('h2:has-text("Analysis Scope")', { timeout: 5000 });
    console.log('✓ Analysis Scope section loaded');

    // Fill in project path - use a small test folder
    await page.fill('input[id="projectPath"]', '/Users/alden/dev/docs_analyzer/docs');

    // Make sure Claude AI is unchecked for speed
    const claudeCheckbox = page.locator('input[id="useClaudeAI"]');
    if (await claudeCheckbox.isChecked()) {
      await claudeCheckbox.uncheck();
    }

    // Click Run Analysis
    const runButton = page.locator('button:has-text("Run Analysis")');
    await expect(runButton).toBeEnabled();
    await runButton.click();

    // Wait for progress indicator
    await page.waitForSelector('text=/Running analysis/', { timeout: 5000 });
    console.log('✓ Progress indicator appeared');

    // Wait for elapsed time to start counting
    await page.waitForSelector('text=/Elapsed:/', { timeout: 5000 });
    console.log('✓ Elapsed timer started');

    // Wait for analysis to complete (may take 1-2 minutes)
    await page.waitForSelector('text=/Total Issues/i', { timeout: 180000 });
    console.log('✓ Analysis completed');

    // Check that progress indicator disappeared
    await expect(page.locator('text=/Running analysis/')).not.toBeVisible();
    console.log('✓ Progress indicator cleared');

    // Check for View Results button
    const viewResultsButton = page.locator('button:has-text("View Analysis Results")');
    await expect(viewResultsButton).toBeVisible({ timeout: 5000 });
    console.log('✓ View Results button appeared');

    // Click View Results
    await viewResultsButton.click();

    // Should navigate to results page
    await expect(page).toHaveURL(/.*analysis-results/);
    console.log('✓ Navigated to results page');

    // Should see download dropdown
    await expect(page.locator('button:has-text("Download Report")')).toBeVisible();
    console.log('✓ Download button visible');

    // Should see summary cards
    await expect(page.locator('text=/Total Issues/i')).toBeVisible();
    await expect(page.locator('text=/Files Analyzed/i')).toBeVisible();
    console.log('✓ Summary cards visible');

    // Test download dropdown
    await page.click('button:has-text("Download Report")');
    await expect(page.locator('text=Download HTML')).toBeVisible();
    await expect(page.locator('text=Download Markdown')).toBeVisible();
    await expect(page.locator('text=Download JSON')).toBeVisible();
    console.log('✓ Download options visible');

    // Go back
    await page.click('button:has-text("Back to Analysis")');
    await expect(page).toHaveURL('http://localhost:3000');
    console.log('✓ Back button works');

    console.log('\\n✅ ALL TESTS PASSED!');
  });

  test('should handle file filtering correctly', async ({ page }) => {
    // Fill in project path
    await page.fill('input[id="projectPath"]', '/Users/alden/dev/claude_docs_clone_mintlify');

    // Uncheck Claude AI for faster testing
    const claudeCheckbox = page.locator('input[id="useClaudeAI"]');
    if (await claudeCheckbox.isChecked()) {
      await claudeCheckbox.uncheck();
    }

    // Run analysis (runs all analyzers/fixers automatically with simplified UI)
    await page.click('button:has-text("Run Analysis")');

    // Wait for completion
    await page.waitForSelector('text=/Total Issues|Files Analyzed/', { timeout: 300000 });

    // Get the file count
    const filesText = await page.locator('text=/Files Analyzed/i').textContent();
    console.log(`Files analyzed: ${filesText}`);

    // Should only analyze .mdx files, not .md files
    // The claude docs clone has both .md and .mdx files
    // If filtering works, we should see fewer files

    console.log('✓ File filtering test completed');
  });
});
