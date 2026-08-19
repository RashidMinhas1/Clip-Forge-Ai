import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import React from 'react';
import { render, screen, act, waitFor } from '@testing-library/react';
import { AuthProvider, useAuth } from '@/contexts/AuthContext';
import { supabase } from '@/lib/supabase';
import { useRouter, usePathname } from 'next/navigation';

// Mock Next.js navigation
vi.mock('next/navigation', () => ({
  useRouter: vi.fn(),
  usePathname: vi.fn(),
}));

// Mock Supabase client
vi.mock('@/lib/supabase', () => ({
  supabase: {
    auth: {
      getSession: vi.fn(),
      onAuthStateChange: vi.fn(),
      signOut: vi.fn(),
    },
  },
}));

// Dummy component to consume the context
const TestComponent = () => {
  const { user, isLoading, logout } = useAuth();
  
  if (isLoading) return <div>Loading...</div>;
  if (!user) return <div>Not Authenticated</div>;
  
  return (
    <div>
      <span>User: {user.email}</span>
      <button onClick={logout}>Logout</button>
    </div>
  );
};

describe('AuthContext', () => {
  let mockPush: any;

  beforeEach(() => {
    mockPush = vi.fn();
    (useRouter as any).mockReturnValue({ push: mockPush });
    (usePathname as any).mockReturnValue('/');
    
    // Default mock implementation
    (supabase.auth.getSession as any).mockResolvedValue({
      data: { session: null }
    });
    
    (supabase.auth.onAuthStateChange as any).mockReturnValue({
      data: { subscription: { unsubscribe: vi.fn() } }
    });
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  it('renders loading state initially', async () => {
    // Delay resolution of getSession to verify loading state
    let resolveSession: any;
    (supabase.auth.getSession as any).mockReturnValue(
      new Promise(resolve => {
        resolveSession = resolve;
      })
    );

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    expect(screen.getByText('Loading...')).toBeInTheDocument();
    
    // Resolve it
    resolveSession({ data: { session: null } });
    
    await waitFor(() => {
      expect(screen.queryByText('Loading...')).not.toBeInTheDocument();
    });
  });

  it('provides user data when authenticated', async () => {
    const mockUser = { email: 'test@example.com' };
    (supabase.auth.getSession as any).mockResolvedValue({
      data: { session: { user: mockUser, access_token: 'fake-token' } }
    });

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    await waitFor(() => {
      expect(screen.getByText('User: test@example.com')).toBeInTheDocument();
    });
  });

  it('redirects to login when unauthenticated on a private route', async () => {
    (usePathname as any).mockReturnValue('/projects');
    (supabase.auth.getSession as any).mockResolvedValue({
      data: { session: null }
    });

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith('/auth?mode=login');
    });
  });
  
  it('does not redirect on public routes when unauthenticated', async () => {
    (usePathname as any).mockReturnValue('/pricing');
    (supabase.auth.getSession as any).mockResolvedValue({
      data: { session: null }
    });

    render(
      <AuthProvider>
        <TestComponent />
      </AuthProvider>
    );

    await waitFor(() => {
      expect(mockPush).not.toHaveBeenCalled();
    });
  });
});
