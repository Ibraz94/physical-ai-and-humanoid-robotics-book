import React, { useState, useEffect } from 'react';

/**
 * Floating chat button that opens/closes the chat overlay
 */
const ChatIcon = ({ onToggle, isOpen, isAuthenticated = true }) => {
  const [isDarkMode, setIsDarkMode] = useState(true);
  const [showTooltip, setShowTooltip] = useState(false);

  useEffect(() => {
    // Detect theme from HTML data-theme attribute
    const detectTheme = () => {
      const theme = document.documentElement.getAttribute('data-theme');
      setIsDarkMode(theme === 'dark' || !theme);
    };

    detectTheme();

    // Watch for theme changes
    const observer = new MutationObserver(detectTheme);
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['data-theme']
    });

    return () => observer.disconnect();
  }, []);

  const buttonStyle = {
    position: 'fixed',
    bottom: '24px',
    right: '24px',
    zIndex: 9999,
    width: isOpen ? '60px' : 'auto',
    minWidth: '60px',
    height: '60px',
    padding: isOpen ? '0' : '0 24px',
    borderRadius: '30px',
    border: 'none',
    background: isDarkMode 
      ? 'linear-gradient(135deg, #00cfd9 0%, #00aabb 100%)'
      : 'linear-gradient(135deg, #000000 0%, #333333 100%)',
    color: '#ffffff',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '10px',
    boxShadow: isDarkMode
      ? '0 4px 20px rgba(0, 207, 217, 0.4)'
      : '0 4px 20px rgba(0, 0, 0, 0.3)',
    transition: 'all 0.3s ease',
    fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    fontSize: '15px',
    fontWeight: '600',
    transform: isOpen ? 'scale(0.9)' : 'scale(1)',
    whiteSpace: 'nowrap',
    opacity: isAuthenticated ? 1 : 0.8
  };

  const tooltipStyle = {
    position: 'fixed',
    bottom: '94px',
    right: '24px',
    zIndex: 9998,
    background: isDarkMode ? '#1a1d29' : '#ffffff',
    color: isDarkMode ? '#ffffff' : '#000000',
    padding: '12px 16px',
    borderRadius: '8px',
    boxShadow: isDarkMode
      ? '0 4px 12px rgba(0, 0, 0, 0.3)'
      : '0 4px 12px rgba(0, 0, 0, 0.15)',
    fontSize: '14px',
    fontWeight: '500',
    whiteSpace: 'nowrap',
    border: isDarkMode ? '1px solid rgba(0, 243, 255, 0.2)' : '1px solid #e5e7eb',
    opacity: showTooltip ? 1 : 0,
    transform: showTooltip ? 'translateY(0)' : 'translateY(10px)',
    transition: 'all 0.2s ease',
    pointerEvents: 'none'
  };

  return (
    <>
      {!isAuthenticated && showTooltip && (
        <div style={tooltipStyle}>
          Sign in to access AI Assistant
        </div>
      )}
      <button
        onClick={onToggle}
        style={buttonStyle}
        onMouseEnter={(e) => {
          if (!isAuthenticated) {
            setShowTooltip(true);
          }
          e.target.style.transform = isOpen ? 'scale(0.9)' : 'scale(1.05)';
          e.target.style.boxShadow = isDarkMode
            ? '0 6px 24px rgba(0, 207, 217, 0.5)'
            : '0 6px 24px rgba(0, 0, 0, 0.4)';
        }}
        onMouseLeave={(e) => {
          setShowTooltip(false);
          e.target.style.transform = isOpen ? 'scale(0.9)' : 'scale(1)';
          e.target.style.boxShadow = isDarkMode
            ? '0 4px 20px rgba(0, 207, 217, 0.4)'
            : '0 4px 20px rgba(0, 0, 0, 0.3)';
        }}
        aria-label={isAuthenticated ? "Toggle chat" : "Sign in to use chat"}
        title={isAuthenticated ? "" : "Sign in to access AI Assistant"}
      >
        {isOpen ? (
          <svg width="26" height="26" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        ) : (
          <>
            <svg width="22" height="22" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
            </svg>
            <span>Ask Me</span>
          </>
        )}
      </button>
    </>
  );
};

export default ChatIcon;
