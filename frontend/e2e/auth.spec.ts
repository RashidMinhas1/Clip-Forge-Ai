import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test('should navigate to auth page from landing page', async ({ page }) => {
    await page.goto('/');
    
    // Click on Get Started or Sign Up
    const getStartedButton = page.locator('text=Get Started').first();
    await expect(getStartedButton).toBeVisible();
    await getStartedButton.click();
    
    // Verify we are on the auth page
    await expect(page).toHaveURL(/.*\/auth\?mode=signup/);
    await expect(page.locator('h1')).toContainText('Create an account');
  });

  test('should toggle between login and signup', async ({ page }) => {
    await page.goto('/auth?mode=login');
    
    // Verify login mode
    await expect(page.locator('h1')).toContainText('Welcome back');
    await expect(page.locator('button[type="submit"]')).toContainText('Sign In');
    
    // Toggle to signup
    await page.click('text=Sign up for free');
    
    // Verify signup mode
    await expect(page).toHaveURL(/.*\/auth\?mode=signup/);
    await expect(page.locator('h1')).toContainText('Create an account');
    await expect(page.locator('button[type="submit"]')).toContainText('Get Started');
  });
});
