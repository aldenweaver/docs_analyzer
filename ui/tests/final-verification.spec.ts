import { test, expect } from '@playwright/test';

test('Final verification: UI displays correct Files Analyzed count', async ({ page }) => {
  // Navigate to the app
  await page.goto('http://localhost:3001');

  // Enter the test docs path
  await page.fill('#projectPath', '/Users/alden/dev/docs_analyzer/test_docs');

  // Start analysis
  await page.click('button:text("Run Analysis")');

  // Wait for Results section to appear (not waiting for specific text)
  await page.waitForSelector('h2:text("Results")', { timeout: 30000 });

  // Small delay to ensure DOM updates
  await page.waitForTimeout(1000);

  // Get the Files Analyzed value
  const filesAnalyzedElement = await page.locator('text=Files Analyzed').locator('..').locator('.text-3xl');
  const filesCount = await filesAnalyzedElement.textContent();

  console.log('✅ Files Analyzed displays:', filesCount);

  // Verify it shows 4 (not 0!)
  expect(parseInt(filesCount || '0')).toBe(4);

  // Get Total Issues value for comparison
  const totalIssuesElement = await page.locator('text=Total Issues').locator('..').locator('.text-3xl');
  const issuesCount = await totalIssuesElement.textContent();

  console.log('✅ Total Issues displays:', issuesCount);
  expect(parseInt(issuesCount || '0')).toBe(9);

  console.log('\n🎉 SUCCESS! The bug is fixed!');
  console.log('Files Analyzed now correctly shows the actual count from the API.');
});