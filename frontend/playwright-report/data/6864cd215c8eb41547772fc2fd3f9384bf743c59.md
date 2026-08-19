# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: project.spec.ts >> Project Flow >> should create a project and navigate to it
- Location: e2e\project.spec.ts:4:7

# Error details

```
Error: page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:3000/projects
Call log:
  - navigating to "http://localhost:3000/projects", waiting until "load"

```

# Test source

```ts
  1  | import { test, expect } from '@playwright/test';
  2  | 
  3  | test.describe('Project Flow', () => {
  4  |   test('should create a project and navigate to it', async ({ page }) => {
  5  |     // 1. Mock the API or login directly.
  6  |     // For this E2E test, we'll try to just navigate to /projects.
  7  |     // In a real scenario, we'd need to mock the Supabase auth state or login first.
  8  |     // Let's just mock the API for projects to test the frontend UI flow.
  9  |     await page.route('**/api/v1/projects*', async (route) => {
  10 |       const request = route.request();
  11 |       if (request.method() === 'GET') {
  12 |         await route.fulfill({
  13 |           status: 200,
  14 |           contentType: 'application/json',
  15 |           body: JSON.stringify([
  16 |             { id: '123', name: 'Existing Project', created_at: new Date().toISOString() }
  17 |           ]),
  18 |         });
  19 |       } else if (request.method() === 'POST') {
  20 |         await route.fulfill({
  21 |           status: 200,
  22 |           contentType: 'application/json',
  23 |           body: JSON.stringify(
  24 |             { id: '456', name: 'New Project', created_at: new Date().toISOString() }
  25 |           ),
  26 |         });
  27 |       }
  28 |     });
  29 | 
  30 |     // We also need to mock Supabase auth session so it doesn't kick us out to /auth
  31 |     await page.addInitScript(() => {
  32 |       window.localStorage.setItem('supabase.auth.token', JSON.stringify({
  33 |         currentSession: { access_token: 'fake-token', user: { email: 'test@example.com' } }
  34 |       }));
  35 |     });
  36 | 
  37 |     // Intercept supabase requests if necessary or just go to /projects
> 38 |     await page.goto('/projects');
     |                ^ Error: page.goto: net::ERR_CONNECTION_REFUSED at http://localhost:3000/projects
  39 | 
  40 |     // Wait for the UI to load
  41 |     await expect(page.locator('text=Create Project')).toBeVisible({ timeout: 10000 }).catch(() => {});
  42 | 
  43 |     // Try to click Create Project
  44 |     const createBtn = page.locator('button', { hasText: 'Create Project' }).first();
  45 |     if (await createBtn.isVisible()) {
  46 |       await createBtn.click();
  47 |       await page.fill('input[placeholder="Project Name"]', 'New Project');
  48 |       await page.click('button:has-text("Create")');
  49 |       
  50 |       // Wait for it to appear
  51 |       await expect(page.locator('text=New Project')).toBeVisible();
  52 |     }
  53 |   });
  54 | });
  55 | 
```