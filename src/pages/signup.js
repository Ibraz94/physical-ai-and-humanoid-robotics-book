import React, { useState } from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import { authClient } from '../components/auth/auth-client';
import { useHistory } from '@docusaurus/router';
import styles from './auth.module.css';

export default function SignupPage() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    softwareBackground: '',
    hardwareBackground: '',
    consentGiven: false
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const history = useHistory();

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
    // Clear error for this field
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    } else if (!/\d/.test(formData.password)) {
      newErrors.password = 'Password must contain at least one number';
    }

    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password';
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    if (!formData.consentGiven) {
      newErrors.consent = 'You must consent to data storage';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setLoading(true);
    setErrors({});

    try {
      const result = await authClient.signUp.email({
        email: formData.email,
        password: formData.password,
        name: formData.email.split('@')[0],
        softwareBackground: formData.softwareBackground,
        hardwareBackground: formData.hardwareBackground,
        consentGiven: formData.consentGiven
      });

      if (result.error) {
        setErrors({ general: result.error.message || 'Failed to create account' });
        setLoading(false);
        return;
      }

      // Redirect to home page on success
      history.push('/physical-ai-and-humanoid-robotics-book/');
    } catch (err) {
      setErrors({ general: err.message || 'An unexpected error occurred' });
      setLoading(false);
    }
  };

  return (
    <Layout title="Sign Up" description="Create your account">
      <div className={styles.authContainer}>
        <div className={styles.authCard}>
          <div className={styles.authHeader}>
            <h1 className={styles.authTitle}>Create Account</h1>
            <p className={styles.authSubtitle}>Join us to start learning Physical AI & Robotics</p>
          </div>

          {errors.general && (
            <div className={styles.errorAlert}>
              <svg className={styles.alertIcon} fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              {errors.general}
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
                className={`${styles.formInput} ${errors.email ? styles.inputError : ''}`}
                placeholder="you@example.com"
                required
                disabled={loading}
              />
              {errors.email && <p className={styles.fieldError}>{errors.email}</p>}
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
                className={`${styles.formInput} ${errors.password ? styles.inputError : ''}`}
                placeholder="At least 6 characters with a number"
                required
                minLength="6"
                disabled={loading}
              />
              {errors.password && <p className={styles.fieldError}>{errors.password}</p>}
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="confirmPassword" className={styles.formLabel}>
                Confirm Password
              </label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                className={`${styles.formInput} ${errors.confirmPassword ? styles.inputError : ''}`}
                placeholder="Re-enter your password"
                required
                disabled={loading}
              />
              {errors.confirmPassword && <p className={styles.fieldError}>{errors.confirmPassword}</p>}
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="softwareBackground" className={styles.formLabel}>
                Software Background <span className={styles.optional}>(Optional)</span>
              </label>
              <textarea
                id="softwareBackground"
                name="softwareBackground"
                value={formData.softwareBackground}
                onChange={handleChange}
                className={styles.formTextarea}
                placeholder="Tell us about your software development experience..."
                rows="3"
                disabled={loading}
              />
            </div>

            <div className={styles.formGroup}>
              <label htmlFor="hardwareBackground" className={styles.formLabel}>
                Hardware Background <span className={styles.optional}>(Optional)</span>
              </label>
              <textarea
                id="hardwareBackground"
                name="hardwareBackground"
                value={formData.hardwareBackground}
                onChange={handleChange}
                className={styles.formTextarea}
                placeholder="Tell us about your hardware/robotics experience..."
                rows="3"
                disabled={loading}
              />
            </div>

            <div className={styles.formCheckbox}>
              <input
                type="checkbox"
                id="consentGiven"
                name="consentGiven"
                checked={formData.consentGiven}
                onChange={handleChange}
                className={styles.checkbox}
                required
                disabled={loading}
              />
              <label htmlFor="consentGiven" className={styles.checkboxLabel}>
                I consent to storing my personal information and background data
              </label>
            </div>
            {errors.consent && <p className={styles.fieldError}>{errors.consent}</p>}

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
                  Creating Account...
                </>
              ) : (
                'Create Account'
              )}
            </button>
          </form>

          <div className={styles.authFooter}>
            <p className={styles.footerText}>
              Already have an account?{' '}
              <Link to="/signin" className={styles.footerLink}>
                Sign in
              </Link>
            </p>
          </div>
        </div>
      </div>
    </Layout>
  );
}
