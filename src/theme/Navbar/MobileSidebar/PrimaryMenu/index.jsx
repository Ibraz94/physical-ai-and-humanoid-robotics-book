import React from 'react';
import PrimaryMenu from '@theme-original/Navbar/MobileSidebar/PrimaryMenu';
import { authClient } from '@site/src/components/auth/auth-client';
import sessionStorage from '@site/src/components/auth/session-storage';
import { useHistory } from '@docusaurus/router';
import useBaseUrl from '@docusaurus/useBaseUrl';

export default function PrimaryMenuWrapper(props) {
  const history = useHistory();
  const baseUrl = useBaseUrl('/');
  
  // Check localStorage for session
  const localSession = sessionStorage.getSession();
  const isAuthenticated = !!localSession?.user;

  const handleSignOut = async () => {
    await authClient.signOut();
    sessionStorage.clearSession();
    history.push(baseUrl);
    setTimeout(() => window.location.reload(), 100);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      <div style={{ flex: 1, overflowY: 'auto' }}>
        <PrimaryMenu {...props} />
      </div>
      
      {isAuthenticated && (
        <div style={{
          padding: '1rem',
          borderTop: '2px solid var(--ifm-color-emphasis-300)',
          backgroundColor: 'var(--ifm-navbar-background-color)',
          marginTop: 'auto'
        }}>
          <div style={{
            fontSize: '0.9rem',
            color: 'var(--ifm-font-color-base)',
            fontWeight: '600',
            marginBottom: '0.75rem',
            wordBreak: 'break-word',
            padding: '0.5rem',
            backgroundColor: 'var(--ifm-color-emphasis-100)',
            borderRadius: '4px'
          }}>
            {localSession.user.email}
          </div>
          <button 
            onClick={handleSignOut}
            style={{
              background: 'var(--ifm-color-primary)',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              padding: '0.75rem 1rem',
              fontSize: '0.95rem',
              fontWeight: '600',
              cursor: 'pointer',
              width: '100%',
              transition: 'all 0.2s'
            }}
            onMouseDown={(e) => {
              e.currentTarget.style.transform = 'scale(0.98)';
            }}
            onMouseUp={(e) => {
              e.currentTarget.style.transform = 'scale(1)';
            }}
          >
            Sign Out
          </button>
        </div>
      )}
    </div>
  );
}
