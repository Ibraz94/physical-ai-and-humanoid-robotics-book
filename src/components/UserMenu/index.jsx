import React from 'react';
import { useSession, authClient } from '../auth/auth-client';
import { useHistory } from '@docusaurus/router';
import styles from './styles.module.css';

export default function UserMenu() {
  const { data: session, isLoading } = useSession();
  const history = useHistory();

  const handleSignOut = async () => {
    await authClient.signOut();
    history.push('/');
  };

  if (isLoading) {
    return null;
  }

  if (!session?.user) {
    return null;
  }

  return (
    <div className={styles.userMenu}>
      <span className={styles.userEmail}>{session.user.email}</span>
      <button onClick={handleSignOut} className={styles.signOutButton}>
        Sign Out
      </button>
    </div>
  );
}
