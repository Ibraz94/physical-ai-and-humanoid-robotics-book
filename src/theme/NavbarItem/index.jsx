import React from 'react';
import NavbarItem from '@theme-original/NavbarItem';
import { useSession } from '@site/src/components/auth/auth-client';
import sessionStorage from '@site/src/components/auth/session-storage';

export default function NavbarItemWrapper(props) {
  const { data: session, isLoading } = useSession();
  
  // Check localStorage for session (since cookies don't work cross-domain)
  const localSession = sessionStorage.getSession();
  const isAuthenticated = !!localSession?.user;

  // Hide Sign In and Sign Up buttons when user is authenticated
  if (isAuthenticated && (props.to === '/signin' || props.to === '/signup')) {
    return null;
  }

  return <NavbarItem {...props} />;
}
