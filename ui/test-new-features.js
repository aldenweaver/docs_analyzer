const { chromium } = require('playwright');

async function testNewFeatures() {
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  try {
    console.log('1. Navigate to localhost:3001');
    await page.goto('http://localhost:3001');
    await page.waitForLoadState('networkidle');

    // Take screenshot of initial page
    await page.screenshot({ path: '/tmp/test-1-initial-page.png', fullPage: true });
    console.log('   ✓ Initial page loaded');

    // Check if file path input exists
    console.log('\n2. Check form elements');
    const projectPathInput = await page.locator('input[id="projectPath"]');
    await projectPathInput.waitFor({ state: 'visible' });
    console.log('   ✓ Project path input found');

    // Fill in project path
    console.log('\n3. Fill project path');
    await projectPathInput.fill('/Users/alden/dev/claude_docs_clone_mintlify');
    await page.screenshot({ path: '/tmp/test-2-filled-form.png', fullPage: true });
    console.log('   ✓ Project path filled');

    // Uncheck all fixers to speed up test
    console.log('\n4. Uncheck all fixers');
    const fixersSection = page.locator('text=Fixers').locator('..');
    const fixerCheckboxes = fixersSection.locator('input[type="checkbox"]');
    const count = await fixerCheckboxes.count();
    for (let i = 0; i < count; i++) {
      const checkbox = fixerCheckboxes.nth(i);
      if (await checkbox.isChecked()) {
        await checkbox.uncheck();
      }
    }
    console.log(`   ✓ Unchecked ${count} fixers to speed up test`);

    // Select only one analyzer
    console.log('\n5. Select only frontmatter analyzer');
    const analyzersSection = page.locator('text=Analyzers').locator('..');
    const analyzerCheckboxes = analyzersSection.locator('input[type="checkbox"]');
    const analyzerCount = await analyzerCheckboxes.count();
    for (let i = 0; i < analyzerCount; i++) {
      const checkbox = analyzerCheckboxes.nth(i);
      await checkbox.uncheck();
    }
    // Check only frontmatter
    await page.locator('label:has-text("Frontmatter")').locator('..').locator('input[type="checkbox"]').check();
    console.log('   ✓ Selected only frontmatter analyzer');

    // Click Run Analysis
    console.log('\n6. Click Run Analysis button');
    const runButton = page.locator('button:has-text("Run Analysis")');
    await runButton.click();
    await page.screenshot({ path: '/tmp/test-3-analysis-started.png', fullPage: true });
    console.log('   ✓ Analysis started');

    // Wait for progress indicator
    console.log('\n7. Check progress indicator');
    const progressIndicator = page.locator('text=Running analysis');
    await progressIndicator.waitFor({ state: 'visible', timeout: 5000 });
    console.log('   ✓ Progress indicator visible');

    // Check elapsed time is shown
    const elapsedTime = page.locator('text=Elapsed:');
    await elapsedTime.waitFor({ state: 'visible', timeout: 5000 });
    console.log('   ✓ Elapsed timer visible');
    await page.screenshot({ path: '/tmp/test-4-in-progress.png', fullPage: true });

    // Wait for analysis to complete (max 60 seconds)
    console.log('\n8. Wait for analysis to complete (max 60s)');
    await page.waitForSelector('text=Running analysis', { state: 'detached', timeout: 60000 });
    console.log('   ✓ Analysis completed');

    // Wait a bit for results to render
    await page.waitForTimeout(1000);
    await page.screenshot({ path: '/tmp/test-5-analysis-complete.png', fullPage: true });

    // Check if View Results buttons appear
    console.log('\n9. Check for View Analysis Results button');
    const viewResultsButton = page.locator('button:has-text("View Analysis Results")');
    const isVisible = await viewResultsButton.isVisible().catch(() => false);

    if (isVisible) {
      console.log('   ✓ View Analysis Results button found!');
      await page.screenshot({ path: '/tmp/test-6-results-buttons-visible.png', fullPage: true });

      // Click the button
      console.log('\n10. Click View Analysis Results');
      await viewResultsButton.click();
      await page.waitForURL('**/analysis-results');
      console.log('   ✓ Navigated to analysis-results page');

      await page.waitForTimeout(1000);
      await page.screenshot({ path: '/tmp/test-7-results-page.png', fullPage: true });

      // Check for download button
      const downloadButton = page.locator('button:has-text("Download Report")');
      if (await downloadButton.isVisible()) {
        console.log('   ✓ Download Report button found');

        // Click to show dropdown
        await downloadButton.click();
        await page.waitForTimeout(500);
        await page.screenshot({ path: '/tmp/test-8-download-dropdown.png', fullPage: true });
        console.log('   ✓ Download dropdown visible');
      }

      console.log('\n✅ All new features working!');
    } else {
      console.log('   ❌ View Analysis Results button NOT found');
      console.log('\nDebugging info:');
      const bodyText = await page.textContent('body');
      console.log('Page contains "Results":', bodyText.includes('Results'));
      console.log('Page contains "View":', bodyText.includes('View'));
    }

  } catch (error) {
    console.error('\n❌ Test failed:', error.message);
    await page.screenshot({ path: '/tmp/test-error.png', fullPage: true });
  } finally {
    console.log('\nScreenshots saved to /tmp/test-*.png');
    await browser.close();
  }
}

testNewFeatures();
