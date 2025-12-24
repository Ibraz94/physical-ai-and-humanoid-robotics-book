/**
 * Session Storage Helper
 * 
 * Stores session data in localStorage since cookies don't work
 * across different domains (GitHub Pages vs Hugging Face Spaces)
 */

const SESSION_KEY = 'better_auth_session';

export const sessionStorage = {
  /**
   * Save session data to localStorage
   */
  setSession(sessionData) {
    if (sessionData) {
      localStorage.setItem(SESSION_KEY, JSON.stringify(sessionData));
    }
  },

  /**
   * Get session data from localStorage
   */
  getSession() {
    try {
      const data = localStorage.getItem(SESSION_KEY);
      return data ? JSON.parse(data) : null;
    } catch (error) {
      console.error('Error reading session from localStorage:', error);
      return null;
    }
  },

  /**
   * Clear session data
   */
  clearSession() {
    localStorage.removeItem(SESSION_KEY);
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated() {
    const session = this.getSession();
    return !!session?.user;
  }
};

export default sessionStorage;
