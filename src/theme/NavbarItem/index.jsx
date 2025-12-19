import React from 'react';
import NavbarItem from '@theme-original/NavbarItem';
import { useSession } from '@site/src/components/auth/auth-client';

export default function NavbarItemWrapper(props) {
  const { data: session, isLoading } = useSession();
  const isAuthenticated = !isLoading && !!session?.user;

  // Hide Sign In and Sign Up buttons when user is authenticated
  if (isAuthenticated && (props.to === '/signin' || props.to === '/signup')) {
    return null;
  }

  return <NavbarItem {...props} />;
}
