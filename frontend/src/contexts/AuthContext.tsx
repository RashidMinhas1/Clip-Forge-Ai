'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { supabase } from '@/lib/supabase';
import { User } from '@supabase/supabase-js';
import { apiClient } from '@/lib/api-client';

interface AuthContextType {
  user: User | null;
  token: string | null;
  isActivated: boolean;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isActivated, setIsActivated] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    const publicRoutes = ['/', '/auth', '/pricing', '/activate', '/auth/reset-password'];

    const checkActivation = async (hasSession: boolean) => {
      if (!hasSession) {
        setIsActivated(false);
        return;
      }
      try {
        const res = await apiClient<{activated: boolean}>('/api/v1/access/status');
        setIsActivated(res.activated);
        if (!res.activated && pathname !== '/activate') {
          router.push('/activate');
        }
      } catch (e) {
        console.error("Failed to check activation status:", e);
      }
    };

    const initializeAuth = async () => {
      const { data: { session } } = await supabase.auth.getSession();
      setUser(session?.user ?? null);
      setToken(session?.access_token ?? null);
      
      if (session) {
        await checkActivation(true);
      }
      setIsLoading(false);
      
      if (!session && !publicRoutes.includes(pathname)) {
        router.push('/auth?mode=login');
      }
    };

    initializeAuth();

    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      async (_event, session) => {
        setUser(session?.user ?? null);
        setToken(session?.access_token ?? null);
        
        if (session) {
           await checkActivation(true);
        }
        setIsLoading(false);
        
        if (!session && !publicRoutes.includes(pathname)) {
          router.push('/auth?mode=login');
        } else if (session && pathname === '/auth') {
          // If they just logged in, check if they need activation
          const { data: { session: currentSession } } = await supabase.auth.getSession();
          if (currentSession) {
            try {
              const res = await apiClient<{activated: boolean}>('/api/v1/access/status');
              if (res.activated) {
                router.push('/projects');
              } else {
                router.push('/activate');
              }
            } catch (e) {
              router.push('/projects');
            }
          }
        }
      }
    );

    return () => subscription.unsubscribe();
  }, [pathname, router]);

  const logout = async () => {
    await supabase.auth.signOut();
    setIsActivated(false);
    router.push('/auth?mode=login');
  };

  return (
    <AuthContext.Provider value={{ user, token, isActivated, logout, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
