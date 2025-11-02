import { test, expect } from '@playwright/test';

test.describe('Quick UI Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000');
  });

  test('analysis scope section displays correctly', async ({ page }) => {
    console.log('Testing analysis scope section...');

    // Wait for page to load
    await page.waitForSelector('h1:has-text("Analyze Documentation")');
    console.log('✓ Page loaded');

    // Check for Analysis Scope section
    await page.waitForSelector('h2:has-text("Analysis Scope")', { timeout: 5000 });
    console.log('✓ Analysis Scope section visible');

    // Check that scope descriptions are visible
    await expect(page.locator('text=Runs comprehensive analysis with all quality checks')).toBeVisible();
    console.log('✓ Comprehensive analysis text visible');

    await expect(page.locator('text=Analyzes .mdx documentation files only')).toBeVisible();
    console.log('✓ MDX files text visible');

    await expect(page.locator('text=Excludes node_modules, build artifacts, and README files')).toBeVisible();
    console.log('✓ Exclusions text visible');

    await expect(page.locator('text=Generates HTML, Markdown, and JSON reports')).toBeVisible();
    console.log('✓ Report formats text visible');

    console.log('\\n✅ Analysis scope test PASSED!');
  });

  test('form validation works', async ({ page }) => {
    console.log('Testing form validation...');

    // Run Analysis button should be disabled with no path
    const runButton = page.locator('button:has-text("Run Analysis")');

    // With no path, button should be disabled
    await expect(runButton).toBeDisabled();
    console.log('✓ Button disabled with no path');

    // Fill in a path
    await page.fill('input[id="projectPath"]', '/Users/alden/dev/docs_analyzer/docs');

    // Button should be enabled
    await expect(runButton).toBeEnabled();
    console.log('✓ Button enabled with path');

    console.log('\\n✅ Form validation test PASSED!');
  });

  test('UI components render correctly', async ({ page }) => {
    console.log('Testing UI components...');

    // Check all major sections exist
    await expect(page.locator('h1:has-text("Analyze Documentation")')).toBeVisible();
    console.log('✓ Header visible');

    await expect(page.locator('h2:has-text("Project Settings")')).toBeVisible();
    console.log('✓ Project Settings section visible');

    await expect(page.locator('h2:has-text("Analysis Scope")')).toBeVisible();
    console.log('✓ Analysis Scope section visible');

    await expect(page.locator('button:has-text("Run Analysis")')).toBeVisible();
    console.log('✓ Run Analysis button visible');

    // Check Claude AI checkbox
    await expect(page.locator('label:has-text("Use Claude AI")')).toBeVisible();
    console.log('✓ Claude AI option visible');

    // Check project path input
    await expect(page.locator('input[id="projectPath"]')).toBeVisible();
    console.log('✓ Project path input visible');

    console.log('\\n✅ UI components test PASSED!');
  });
});
