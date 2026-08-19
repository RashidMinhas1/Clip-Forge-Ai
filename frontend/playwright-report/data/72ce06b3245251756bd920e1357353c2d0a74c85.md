# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: auth.spec.ts >> Authentication Flow >> should navigate to auth page from landing page
- Location: e2e\auth.spec.ts:4:7

# Error details

```
Error: page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:3000/
Call log:
  - navigating to "http://localhost:3000/", waiting until "load"

```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | 
  3  | test.describe('Authentication Flow', () => {
  4  |   test('should navigate to auth page from landing page', async ({ page }) => {
> 5  |     await page.goto('/');
     |                ^ Error: page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:3000/
  6  |     
  7  |     // Click on Get Started or Sign Up
  8  |     const getStartedButton = page.locator('text=Get Started').first();
  9  |     await expect(getStartedButton).toBeVisible();
  10 |     await getStartedButton.click();
  11 |     
  12 |     // Verify we are on the auth page
  13 |     await expect(page).toHaveURL(/.*\/auth\?mode=signup/);
  14 |     await expect(page.locator('h1')).toContainText('Create an account');
  15 |   });
  16 | 
  17 |   test('should toggle between login and signup', async ({ page }) => {
  18 |     await page.goto('/auth?mode=login');
  19 |     
  20 |     // Verify login mode
  21 |     await expect(page.locator('h1')).toContainText('Welcome back');
  22 |     await expect(page.locator('button[type="submit"]')).toContainText('Sign In');
  23 |     
  24 |     // Toggle to signup
  25 |     await page.click('text=Sign up for free');
  26 |     
  27 |     // Verify signup mode
  28 |     await expect(page).toHaveURL(/.*\/auth\?mode=signup/);
  29 |     await expect(page.locator('h1')).toContainText('Create an account');
  30 |     await expect(page.locator('button[type="submit"]')).toContainText('Get Started');
  31 |   });
  32 | });
  33 | 
```