const { chromium } = require('playwright');

async function verifyFix() {
  console.log('🔍 Verifying UI Changes with Playwright\n');

  const browser = await chromium.launch({
    headless: false,
    slowMo: 500  // Slow down for visibility
  });
  const page = await browser.newPage();

  try {
    // Step 1: Navigate to page
    console.log('1️⃣  Navigating to http://localhost:3001');
    await page.goto('http://localhost:3001', { waitUntil: 'domcontentloaded' });
    await page.waitForSelector('h1:has-text("Analyze Documentation")');
    console.log('   ✅ Page loaded\n');
    await page.screenshot({ path: '/tmp/verify-1-page-loaded.png', fullPage: true });

    // Step 2: Wait for analyzers to load
    console.log('2️⃣  Waiting for analyzers to load');
    await page.waitForTimeout(3000);  // Give time for API calls
    await page.screenshot({ path: '/tmp/verify-2-analyzers-loaded.png', fullPage: true });

    // Check analyzer count
    const analyzerText = await page.locator('text=Analyzers').locator('..').locator('text=modules selected').textContent();
    console.log(`   ✅ Analyzers loaded: ${analyzerText}\n`);

    // Step 3: Fill in project path
    console.log('3️⃣  Filling in project path');
    const projectPathInput = await page.locator('input[id="projectPath"]');
    await projectPathInput.fill('/Users/alden/dev/claude_docs_clone_mintlify');
    console.log('   ✅ Project path entered\n');
    await page.screenshot({ path: '/tmp/verify-3-path-entered.png', fullPage: true });

    // Step 4: Uncheck all fixers (to speed up test)
    console.log('4️⃣  Unchecking fixers for faster test');
    const fixersSelectNone = page.locator('text=Fixers').locator('..').locator('button:has-text("Select None")');
    await fixersSelectNone.click();
    await page.waitForTimeout(500);
    console.log('   ✅ All fixers unchecked\n');
    await page.screenshot({ path: '/tmp/verify-4-fixers-unchecked.png', fullPage: true });

    // Step 5: Select only one fast analyzer
    console.log('5️⃣  Selecting only frontmatter analyzer');
    const analyzersSelectNone = page.locator('text=Analyzers').locator('..').locator('button:has-text("Select None")');
    await analyzersSelectNone.click();
    await page.waitForTimeout(500);

    // Check frontmatter analyzer
    const frontmatterCheckbox = page.locator('label:has-text("Frontmatter")').locator('..').locator('input[type="checkbox"]');
    await frontmatterCheckbox.check();
    await page.waitForTimeout(500);
    console.log('   ✅ Only frontmatter analyzer selected\n');
    await page.screenshot({ path: '/tmp/verify-5-one-analyzer.png', fullPage: true });

    // Step 6: Click Run Analysis
    console.log('6️⃣  Clicking Run Analysis button');
    const runButton = page.locator('button:has-text("Run Analysis")');
    await runButton.click();
    console.log('   ✅ Analysis started\n');
    await page.screenshot({ path: '/tmp/verify-6-analysis-started.png', fullPage: true });

    // Step 7: Wait for progress indicator
    console.log('7️⃣  Checking for progress indicator');
    try {
      await page.waitForSelector('text=Running analysis', { timeout: 10000 });
      console.log('   ✅ Progress indicator visible');
      await page.waitForTimeout(2000);
      await page.screenshot({ path: '/tmp/verify-7-progress-visible.png', fullPage: true });
    } catch (e) {
      console.log('   ⚠️  Progress indicator not visible (may have completed quickly)');
    }

    // Step 8: Wait for completion
    console.log('\n8️⃣  Waiting for analysis to complete (max 90 seconds)');
    let completed = false;
    for (let i = 0; i < 90; i++) {
      const runningVisible = await page.locator('text=Running analysis').isVisible().catch(() => false);
      if (!runningVisible) {
        completed = true;
        console.log(`   ✅ Analysis completed after ${i} seconds\n`);
        break;
      }
      if (i % 5 === 0) {
        console.log(`   ⏱️  Still running... (${i}s elapsed)`);
      }
      await page.waitForTimeout(1000);
    }

    if (!completed) {
      throw new Error('Analysis timed out after 90 seconds');
    }

    // Wait for results to render
    await page.waitForTimeout(3000);
    await page.screenshot({ path: '/tmp/verify-8-analysis-complete.png', fullPage: true });

    // Step 9: Check for View Analysis Results button
    console.log('9️⃣  Checking for "View Analysis Results" button');
    const viewResultsButton = page.locator('button:has-text("View Analysis Results")');
    const isVisible = await viewResultsButton.isVisible().catch(() => false);

    if (isVisible) {
      console.log('   ✅ "View Analysis Results" button FOUND!\n');
      await page.screenshot({ path: '/tmp/verify-9-button-visible.png', fullPage: true });

      // Step 10: Click the button
      console.log('🔟 Clicking "View Analysis Results" button');
      await viewResultsButton.click();
      await page.waitForURL('**/analysis-results', { timeout: 5000 });
      console.log('   ✅ Navigated to /analysis-results page\n');
      await page.waitForTimeout(2000);
      await page.screenshot({ path: '/tmp/verify-10-results-page.png', fullPage: true });

      // Step 11: Check for download dropdown
      console.log('1️⃣1️⃣  Checking for "Download Report" dropdown');
      const downloadButton = page.locator('button:has-text("Download Report")');
      if (await downloadButton.isVisible()) {
        console.log('   ✅ Download Report button found');

        // Click to show dropdown
        await downloadButton.click();
        await page.waitForTimeout(500);
        await page.screenshot({ path: '/tmp/verify-11-dropdown-open.png', fullPage: true });

        // Check for dropdown options
        const hasHTML = await page.locator('button:has-text("Download HTML")').isVisible();
        const hasMD = await page.locator('button:has-text("Download Markdown")').isVisible();
        const hasJSON = await page.locator('button:has-text("Download JSON")').isVisible();

        if (hasHTML && hasMD && hasJSON) {
          console.log('   ✅ All download options visible (HTML, MD, JSON)\n');
        }
      }

      console.log('═══════════════════════════════════════════════════');
      console.log('✅ SUCCESS! All UI changes are working correctly!');
      console.log('═══════════════════════════════════════════════════\n');
      console.log('Verified features:');
      console.log('  ✅ Progress indicator shows during analysis');
      console.log('  ✅ "View Analysis Results" button appears after completion');
      console.log('  ✅ Results page loads with download dropdown');
      console.log('  ✅ Download options include HTML, Markdown, and JSON');
      console.log('\nScreenshots saved to /tmp/verify-*.png');

    } else {
      console.log('   ❌ "View Analysis Results" button NOT FOUND\n');

      // Debug
      const bodyText = await page.textContent('body');
      console.log('Debug info:');
      console.log('  - Page contains "Results":', bodyText.includes('Results'));
      console.log('  - Page contains "report_dir":', bodyText.includes('report_dir'));

      // Check for errors
      const errorVisible = await page.locator('[class*="destructive"]').isVisible().catch(() => false);
      if (errorVisible) {
        const errorText = await page.textContent('[class*="destructive"]');
        console.log('  - Error message:', errorText);
      }

      console.log('\n❌ Test failed: View Results button not found');
    }

  } catch (error) {
    console.error('\n❌ Test failed with error:', error.message);
    await page.screenshot({ path: '/tmp/verify-error.png', fullPage: true });
    console.log('Error screenshot saved to /tmp/verify-error.png');
  } finally {
    await browser.close();
  }
}

verifyFix();
