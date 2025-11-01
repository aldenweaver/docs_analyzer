import { test, expect } from '@playwright/test';

test.describe('Documentation Analyzer UI', () => {
  test('home page loads correctly', async ({ page }) => {
    await page.goto('/');

    // Check title
    await expect(page.locator('h1')).toContainText('Documentation Analyzer');

    // Check for "Start Analysis" button
    await expect(page.getByRole('link', { name: 'Start Analysis' })).toBeVisible();

    // Check for system capabilities section
    await expect(page.getByText('System Capabilities')).toBeVisible();
    await expect(page.getByText('18 Analyzers')).toBeVisible();
    await expect(page.getByText('18 Fixers')).toBeVisible();
    await expect(page.getByText('AI-Powered')).toBeVisible();
  });

  test('can navigate to analyze page', async ({ page }) => {
    await page.goto('/');

    // Click on "Start Analysis" button
    await page.getByRole('link', { name: 'Start Analysis' }).click();

    // Should be on analyze page
    await expect(page).toHaveURL('/analyze');
    await expect(page.locator('h1')).toContainText('Analyze Documentation');
  });

  test('analyze page has required form elements', async ({ page }) => {
    await page.goto('/analyze');

    // Check for form elements
    await expect(page.getByLabel('Project Path')).toBeVisible();
    await expect(page.getByLabel('Use Claude AI for advanced analysis')).toBeVisible();
    await expect(page.getByRole('button', { name: 'Run Analysis' })).toBeVisible();

    // Check for module selectors
    await expect(page.getByText('Analyzers')).toBeVisible();
    await expect(page.getByText('Fixers')).toBeVisible();

    // Check for Select All/None buttons
    const selectAllButtons = page.getByText('Select All');
    await expect(selectAllButtons.first()).toBeVisible();
  });

  test('module selection works correctly', async ({ page }) => {
    await page.goto('/analyze');

    // Wait for modules to load
    await page.waitForTimeout(1000);

    // Find first analyzer checkbox (after category checkboxes)
    const firstAnalyzer = page.locator('input[type="checkbox"]').nth(1);

    // It should be checked by default (Select All is default)
    await expect(firstAnalyzer).toBeChecked();

    // Click Select None
    const analyzerSection = page.locator('text=Analyzers').locator('..');
    await analyzerSection.getByText('Select None').click();

    // First analyzer should now be unchecked
    await expect(firstAnalyzer).not.toBeChecked();
  });

  test('Claude AI toggle shows API key field', async ({ page }) => {
    await page.goto('/analyze');

    // API key field should not be visible initially
    await expect(page.getByLabel('Claude API Key')).not.toBeVisible();

    // Toggle Claude AI
    await page.getByLabel('Use Claude AI for advanced analysis').click();

    // API key field should now be visible
    await expect(page.getByLabel('Claude API Key')).toBeVisible();
  });

  test('run analysis button is disabled without project path', async ({ page }) => {
    await page.goto('/analyze');

    // Button should be disabled initially
    const runButton = page.getByRole('button', { name: 'Run Analysis' });
    await expect(runButton).toBeDisabled();

    // Enter project path
    await page.getByLabel('Project Path').fill('/test/path');

    // Button should now be enabled
    await expect(runButton).toBeEnabled();
  });
});
