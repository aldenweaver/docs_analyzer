const { chromium } = require('playwright');

async function takeScreenshots() {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  try {
    console.log('1. Navigate to localhost:3001');
    await page.goto('http://localhost:3001', { waitUntil: 'domcontentloaded' });

    // Wait for the main heading instead of networkidle
    await page.waitForSelector('h1:has-text("Analyze Documentation")', { timeout: 10000 });
    console.log('   ✓ Page loaded');

    // Wait a bit for API calls to complete
    await page.waitForTimeout(3000);
    await page.screenshot({ path: '/tmp/test-1-initial-page.png', fullPage: true });
    console.log('   ✓ Initial page screenshot taken');

    // Check if analyzers loaded
    const analyzersText = await page.textContent('text=Analyzers >> .. >> text=of');
    console.log(`   Analyzers loaded: ${analyzersText}`);

    // Fill in project path
    console.log('\n2. Fill project path');
    const projectPathInput = await page.locator('input[id="projectPath"]');
    await projectPathInput.fill('/Users/alden/dev/claude_docs_clone_mintlify');
    await page.screenshot({ path: '/tmp/test-2-filled-form.png', fullPage: true });
    console.log('   ✓ Project path filled');

    // Select all analyzers (using Select All button)
    console.log('\n3. Select all analyzers');
    const selectAllButton = page.locator('text=Analyzers >> .. >> button:has-text("Select All")').first();
    await selectAllButton.click();
    await page.waitForTimeout(500);
    await page.screenshot({ path: '/tmp/test-3-analyzers-selected.png', fullPage: true });
    console.log('   ✓ Analyzers selected');

    // Click Run Analysis
    console.log('\n4. Click Run Analysis button');
    const runButton = page.locator('button:has-text("Run Analysis")');
    await runButton.click();
    await page.screenshot({ path: '/tmp/test-4-analysis-started.png', fullPage: true });
    console.log('   ✓ Analysis started');

    // Wait for progress indicator
    console.log('\n5. Check progress indicator');
    const progressIndicator = page.locator('text=Running analysis');
    await progressIndicator.waitFor({ state: 'visible', timeout: 10000 });
    console.log('   ✓ Progress indicator visible');
    await page.waitForTimeout(2000);
    await page.screenshot({ path: '/tmp/test-5-in-progress.png', fullPage: true });

    // Wait for analysis to complete (max 90 seconds)
    console.log('\n6. Wait for analysis to complete (max 90s)');
    await page.waitForSelector('text=Running analysis', { state: 'detached', timeout: 90000 });
    console.log('   ✓ Analysis completed');

    // Wait a bit for results to render
    await page.waitForTimeout(2000);
    await page.screenshot({ path: '/tmp/test-6-analysis-complete.png', fullPage: true });

    // Check if View Results buttons appear
    console.log('\n7. Check for View Analysis Results button');
    const viewResultsButton = page.locator('button:has-text("View Analysis Results")');
    const isVisible = await viewResultsButton.isVisible().catch(() => false);

    if (isVisible) {
      console.log('   ✅ View Analysis Results button found!');
      await page.screenshot({ path: '/tmp/test-7-results-buttons-visible.png', fullPage: true });

      // Click the button
      console.log('\n8. Click View Analysis Results');
      await viewResultsButton.click();
      await page.waitForURL('**/analysis-results', { timeout: 5000 });
      console.log('   ✓ Navigated to analysis-results page');

      await page.waitForTimeout(2000);
      await page.screenshot({ path: '/tmp/test-8-results-page.png', fullPage: true });

      // Check for download button
      const downloadButton = page.locator('button:has-text("Download Report")');
      if (await downloadButton.isVisible()) {
        console.log('   ✓ Download Report button found');

        // Click to show dropdown
        await downloadButton.click();
        await page.waitForTimeout(500);
        await page.screenshot({ path: '/tmp/test-9-download-dropdown.png', fullPage: true });
        console.log('   ✓ Download dropdown visible');
      }

      console.log('\n✅ All new features working!');
    } else {
      console.log('   ❌ View Analysis Results button NOT found');

      // Debug: check page content
      console.log('\nDebugging info:');
      const bodyText = await page.textContent('body');
      console.log('Page contains "Results":', bodyText.includes('Results'));
      console.log('Page contains "View":', bodyText.includes('View'));
      console.log('Page contains "report_dir":', bodyText.includes('report_dir'));

      // Check if there's an error message
      const errorDiv = page.locator('[class*="destructive"]');
      if (await errorDiv.isVisible().catch(() => false)) {
        const errorText = await errorDiv.textContent();
        console.log('Error message:', errorText);
      }
    }

  } catch (error) {
    console.error('\n❌ Test failed:', error.message);
    await page.screenshot({ path: '/tmp/test-error.png', fullPage: true });
  } finally {
    console.log('\nScreenshots saved to /tmp/test-*.png');
    await browser.close();
  }
}

takeScreenshots();
