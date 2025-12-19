import React, { useState } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import { authClient } from '../components/auth/auth-client';
import { useHistory } from '@docusaurus/router';
import styles from './auth.module.css';

export default function SigninPage() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    rememberMe: false
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const history = useHistory();

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const result = await authClient.signIn.email({
        email: formData.email,
        password: formData.password,
        rememberMe: formData.rememberMe
      });

      if (result.error) {
        setError(result.error.message || 'Failed to sign in. Please check your credentials.');
        setLoading(false);
        return;
      }

      // Redirect to homepage on success
      history.push('/physical-ai-and-humanoid-robotics-book/');
    } catch (err) {
      setError(err.message || 'An unexpected error occurred. Please try again.');
      setLoading(false);
    }
  };

  return (
    <Layout title="Sign In" description="Sign in to your account">
      <div className={styles.authContainer}>
        <div className={styles.authCard}>
          <div className={styles.authHeader}>
            <h1 className={styles.authTitle}>Welcome Back</h1>
            <p className={styles.authSubtitle}>Sign in to continue your learning journey</p>
          </div>

          {error && (
            <div className={styles.errorAlert}>
              <svg className={styles.alertIcon} fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className={styles.authForm}>
            <div className={styles.formGroup}>
              <label htmlFor="email" className={styles.formLabel}>
                Email Address
              </label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className={styles.formInput}
                placeholder="you@example.com"
                required
                disabled={loading}
              />
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="password" className={styles.formLabel}>
                Password
              </label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className={styles.formInput}
                placeholder="••••••••"
                required
                minLength="6"
                disabled={loading}
              />
            </div>

            <div className={styles.formCheckbox}>
              <input
                type="checkbox"
                id="rememberMe"
                name="rememberMe"
                checked={formData.rememberMe}
                onChange={handleChange}
                className={styles.checkbox}
                disabled={loading}
              />
              <label htmlFor="rememberMe" className={styles.checkboxLabel}>
                Remember me for 7 days
              </label>
            </div>

            <button
              type="submit"
              className={styles.submitButton}
              disabled={loading}
            >
              {loading ? (
                <>
                  <svg className={styles.spinner} viewBox="0 0 24 24">
                    <circle className={styles.spinnerCircle} cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  </svg>
                  Signing In...
                </>
              ) : (
                'Sign In'
              )}
            </button>
          </form>

          <div className={styles.authFooter}>
            <p className={styles.footerText}>
              Don't have an account?{' '}
              <Link to="/signup" className={styles.footerLink}>
                Sign up
              </Link>
            </p>
          </div>
        </div>
      </div>
    </Layout>
  );
}
