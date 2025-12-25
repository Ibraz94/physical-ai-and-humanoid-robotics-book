import React from 'react';
import { useSession, authClient } from '@site/src/components/auth/auth-client';
import sessionStorage from '@site/src/components/auth/session-storage';
import { useHistory } from '@docusaurus/router';
import useBaseUrl from '@docusaurus/useBaseUrl';
import Content from '@theme-original/Navbar/Content';

export default function ContentWrapper(props) {
  const { data: session, isLoading } = useSession();
  const history = useHistory();
  const baseUrl = useBaseUrl('/');
  
  // Check localStorage for session (since cookies don't work cross-domain)
  const localSession = sessionStorage.getSession();
  const isAuthenticated = !!localSession?.user;

  const handleSignOut = async () => {
    await authClient.signOut();
    sessionStorage.clearSession(); // Clear localStorage
    history.push(baseUrl);
    setTimeout(() => window.location.reload(), 100);
  };

  return (
    <>
      <Content {...props} />
      {isAuthenticated && (
        <div 
          className="navbar-user-info"
          style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: '0.75rem',
            marginLeft: '1rem',
            paddingLeft: '1rem',
            borderLeft: '1px solid var(--ifm-color-emphasis-300)'
          }}>
          <span style={{ 
            fontSize: '0.9rem', 
            color: 'var(--ifm-color-emphasis-800)',
            fontWeight: '500',
            whiteSpace: 'nowrap',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            maxWidth: '200px'
          }}>
            {localSession.user.email}
          </span>
          <button 
            onClick={handleSignOut}
            className="navbar-signout-button"
          >
            Sign Out
          </button>
        </div>
      )}
    </>
  );
}