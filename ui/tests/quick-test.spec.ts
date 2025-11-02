import { test, expect } from '@playwright/test';

test.describe('Quick UI Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:3000');
  });

  test('modules load correctly', async ({ page }) => {
    console.log('Testing module loading...');

    // Wait for page to load
    await page.waitForSelector('h1:has-text("Analyze Documentation")');
    console.log('✓ Page loaded');

    // Wait for modules to load
    await page.waitForSelector('text=Frontmatter', { timeout: 10000 });
    console.log('✓ Modules loaded');

    // Check that analyzers loaded
    const analyzerCount = await page.locator('[data-testid="analyzer-checkbox"]').count();
    console.log(`✓ Found ${analyzerCount} analyzers`);
    expect(analyzerCount).toBeGreaterThan(0);

    // Check that fixers loaded
    const fixerCount = await page.locator('[data-testid="fixer-checkbox"]').count();
    console.log(`✓ Found ${fixerCount} fixers`);
    expect(fixerCount).toBeGreaterThan(0);

    // Test Select All/None buttons
    const analyzersSection = page.locator('h3:has-text("Analyzers")').locator('..');
    await analyzersSection.locator('button:has-text("Select None")').click();

    // Wait a bit for state to update
    await page.waitForTimeout(500);

    const selectedText = await analyzersSection.locator('text=/\\d+ of \\d+ modules selected/').textContent();
    console.log(`✓ After Select None: ${selectedText}`);
    expect(selectedText).toContain('0 of');

    await analyzersSection.locator('button:has-text("Select All")').click();
    await page.waitForTimeout(500);

    const selectedAllText = await analyzersSection.locator('text=/\\d+ of \\d+ modules selected/').textContent();
    console.log(`✓ After Select All: ${selectedAllText}`);
    expect(selectedAllText).toMatch(/17 of 17/);

    console.log('\\n✅ Module loading test PASSED!');
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

    await expect(page.locator('h3:has-text("Analyzers")')).toBeVisible();
    console.log('✓ Analyzers section visible');

    await expect(page.locator('h3:has-text("Fixers")')).toBeVisible();
    console.log('✓ Fixers section visible');

    await expect(page.locator('button:has-text("Run Analysis")')).toBeVisible();
    console.log('✓ Run Analysis button visible');

    // Check Claude AI checkbox
    await expect(page.locator('label:has-text("Use Claude AI")')).toBeVisible();
    console.log('✓ Claude AI option visible');

    console.log('\\n✅ UI components test PASSED!');
  });
});
