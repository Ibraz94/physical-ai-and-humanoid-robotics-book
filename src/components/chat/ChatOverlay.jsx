import React, { useState, useEffect, useRef } from 'react';
import APIAdapter from './APIAdapter';

/**
 * Chat overlay component that displays the chat interface
 */
const ChatOverlay = ({ isOpen, onClose, selectedText }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isDarkMode, setIsDarkMode] = useState(true);
  const messagesEndRef = useRef(null);
  const apiAdapter = useRef(new APIAdapter('http://localhost:8000')).current;

  useEffect(() => {
    // Detect theme
    const detectTheme = () => {
      const theme = document.documentElement.getAttribute('data-theme');
      setIsDarkMode(theme === 'dark' || !theme);
    };

    detectTheme();

    const observer = new MutationObserver(detectTheme);
    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ['data-theme']
    });

    return () => observer.disconnect();
  }, []);

  useEffect(() => {
    // Auto-scroll to bottom when new messages arrive
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  useEffect(() => {
    // If selected text is provided, add it as context
    if (selectedText && isOpen) {
      setInputValue(`About: "${selectedText.substring(0, 100)}${selectedText.length > 100 ? '...' : ''}"`);
    }
  }, [selectedText, isOpen]);

  const handleSendMessage = async (messageText = null) => {
    const text = messageText || inputValue.trim();
    if (!text || isLoading) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      text: text,
      sender: 'user',
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Send to backend
      const response = await apiAdapter.sendToBackend({
        text: text,
        selectedText: selectedText
      });

      // Add assistant response
      const assistantMessage = {
        id: Date.now() + 1,
        text: response.text,
        sender: 'assistant',
        timestamp: new Date().toISOString(),
        citations: response.citations
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Add error message
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'assistant',
        timestamp: new Date().toISOString(),
        error: true
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  if (!isOpen) return null;

  // Theme colors
  const colors = isDarkMode ? {
    overlayBg: 'rgba(17, 24, 39, 0.95)',
    headerBg: 'rgba(31, 41, 55, 0.8)',
    border: 'rgba(75, 85, 99, 0.3)',
    title: '#ffffff',
    text: '#e5e7eb',
    textMuted: '#9ca3af',
    messageBg: 'rgba(31, 41, 55, 0.6)',
    promptBg: 'rgba(0, 207, 217, 0.1)',
    promptBorder: 'rgba(0, 207, 217, 0.3)',
    inputBg: 'rgba(31, 41, 55, 0.6)',
    inputBorder: 'rgba(75, 85, 99, 0.5)',
    userMessageBg: 'linear-gradient(135deg, #00cfd9 0%, #00aabb 100%)',
    sendButtonBg: 'linear-gradient(135deg, #00cfd9 0%, #00aabb 100%)',
    sendButtonHoverBg: 'linear-gradient(135deg, #00aabb 0%, #008899 100%)'
  } : {
    overlayBg: 'rgba(255, 255, 255, 0.95)',
    headerBg: 'rgba(249, 250, 251, 0.9)',
    border: 'rgba(229, 231, 235, 0.8)',
    title: '#111827',
    text: '#374151',
    textMuted: '#6b7280',
    messageBg: 'rgba(249, 250, 251, 0.8)',
    promptBg: 'rgba(243, 244, 246, 0.8)',
    promptBorder: 'rgba(209, 213, 219, 0.8)',
    inputBg: 'rgba(255, 255, 255, 0.9)',
    inputBorder: 'rgba(209, 213, 219, 0.8)',
    userMessageBg: 'linear-gradient(135deg, #000000 0%, #333333 100%)',
    sendButtonBg: 'linear-gradient(135deg, #000000 0%, #333333 100%)',
    sendButtonHoverBg: 'linear-gradient(135deg, #333333 0%, #555555 100%)'
  };

  const overlayStyle = {
    position: 'fixed',
    bottom: '100px',
    right: '24px',
    zIndex: 9999,
    width: '400px',
    height: '550px',
    maxHeight: '80vh',
    background: colors.overlayBg,
    backdropFilter: 'blur(20px)',
    border: `1px solid ${colors.border}`,
    borderRadius: '16px',
    boxShadow: isDarkMode 
      ? '0 8px 32px rgba(0, 0, 0, 0.4)'
      : '0 8px 32px rgba(0, 0, 0, 0.1)',
    display: 'flex',
    flexDirection: 'column',
    fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    animation: 'slideInUp 0.1s ease-out',
    overflow: 'hidden'
  };

  const headerStyle = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '20px',
    borderBottom: `1px solid ${colors.border}`,
    background: colors.headerBg,
    borderTopLeftRadius: '16px',
    borderTopRightRadius: '16px'
  };

  const titleStyle = {
    fontSize: '18px',
    fontWeight: '600',
    color: colors.title,
    margin: 0
  };

  const closeButtonStyle = {
    background: 'transparent',
    border: 'none',
    color: colors.title,
    cursor: 'pointer',
    padding: '4px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    transition: 'all 0.3s ease'
  };

  const messagesContainerStyle = {
    flex: 1,
    overflowY: 'auto',
    padding: '20px',
    display: 'flex',
    flexDirection: 'column',
    gap: '16px'
  };

  const inputContainerStyle = {
    padding: '16px 20px',
    borderTop: `1px solid ${colors.border}`,
    display: 'flex',
    gap: '12px',
    alignItems: 'center',
    background: colors.headerBg
  };

  const inputStyle = {
    flex: 1,
    padding: '12px 16px',
    borderRadius: '12px',
    border: `1px solid ${colors.inputBorder}`,
    background: colors.inputBg,
    color: colors.text,
    fontSize: '14px',
    fontFamily: 'inherit',
    outline: 'none',
    transition: 'all 0.3s ease'
  };

  const sendButtonStyle = {
    width: '44px',
    height: '44px',
    borderRadius: '12px',
    border: 'none',
    background: colors.sendButtonBg,
    color: '#ffffff',
    cursor: isLoading ? 'not-allowed' : 'pointer',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    transition: 'all 0.3s ease',
    opacity: isLoading ? 0.6 : 1
  };

  return (
    <div style={overlayStyle} className="chatkit-overlay">
      {/* Header */}
      <div style={headerStyle}>
        <h2 style={titleStyle}>AI Assistant</h2>
      </div>

      {/* Messages Container */}
      <div style={messagesContainerStyle}>
        {messages.length === 0 && (
          <div style={{ textAlign: 'center', color: colors.textMuted, marginTop: '40px' }}>
            <p style={{ marginBottom: '20px', fontSize: '14px', lineHeight: '1.5' }}>
              {selectedText 
                ? `Ask me about: "${selectedText.substring(0, 50)}${selectedText.length > 50 ? '...' : ''}"`
                : 'Ask me anything about the course'}
            </p>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <button
                onClick={() => handleSendMessage('How do I get started?')}
                style={{
                  width: '100%',
                  textAlign: 'left',
                  padding: '12px 16px',
                  borderRadius: '12px',
                  border: `1px solid ${colors.promptBorder}`,
                  background: colors.promptBg,
                  color: colors.text,
                  cursor: 'pointer',
                  fontSize: '13px',
                  transition: 'all 0.3s ease'
                }}
                onMouseEnter={(e) => e.target.style.transform = 'translateX(4px)'}
                onMouseLeave={(e) => e.target.style.transform = 'translateX(0)'}
              >
                How do I get started?
              </button>
              <button
                onClick={() => handleSendMessage('What is Physical AI?')}
                style={{
                  width: '100%',
                  textAlign: 'left',
                  padding: '12px 16px',
                  borderRadius: '12px',
                  border: `1px solid ${colors.promptBorder}`,
                  background: colors.promptBg,
                  color: colors.text,
                  cursor: 'pointer',
                  fontSize: '13px',
                  transition: 'all 0.3s ease'
                }}
                onMouseEnter={(e) => e.target.style.transform = 'translateX(4px)'}
                onMouseLeave={(e) => e.target.style.transform = 'translateX(0)'}
              >
                What is Physical AI?
              </button>
              <button
                onClick={() => handleSendMessage('Tell me about ROS 2')}
                style={{
                  width: '100%',
                  textAlign: 'left',
                  padding: '12px 16px',
                  borderRadius: '12px',
                  border: `1px solid ${colors.promptBorder}`,
                  background: colors.promptBg,
                  color: colors.text,
                  cursor: 'pointer',
                  fontSize: '13px',
                  transition: 'all 0.3s ease'
                }}
                onMouseEnter={(e) => e.target.style.transform = 'translateX(4px)'}
                onMouseLeave={(e) => e.target.style.transform = 'translateX(0)'}
              >
                Tell me about ROS 2
              </button>
            </div>
          </div>
        )}
        
        {messages.map((message) => {
          const isUser = message.sender === 'user';
          const isError = message.error;
          
          const messageWrapperStyle = {
            display: 'flex',
            justifyContent: isUser ? 'flex-end' : 'flex-start'
          };
          
          const messageBubbleStyle = {
            maxWidth: '80%',
            padding: '12px 16px',
            borderRadius: isUser ? '18px 18px 4px 18px' : '18px 18px 18px 4px',
            background: isUser 
              ? colors.userMessageBg
              : isError
              ? (isDarkMode ? 'rgba(239, 68, 68, 0.2)' : 'rgba(254, 226, 226, 0.9)')
              : colors.messageBg,
            color: isUser ? '#ffffff' : isError ? (isDarkMode ? '#fca5a5' : '#991b1b') : colors.text,
            border: isUser ? 'none' : `1px solid ${isError ? (isDarkMode ? 'rgba(239, 68, 68, 0.4)' : 'rgba(239, 68, 68, 0.3)') : colors.border}`,
            boxShadow: isUser 
              ? (isDarkMode ? '0 2px 8px rgba(0, 207, 217, 0.25)' : '0 2px 8px rgba(0, 0, 0, 0.15)')
              : (isDarkMode ? '0 2px 8px rgba(0, 0, 0, 0.2)' : '0 2px 8px rgba(0, 0, 0, 0.05)'),
            fontSize: '14px',
            lineHeight: '1.5'
          };
          
          return (
            <div key={message.id} style={messageWrapperStyle}>
              <div style={messageBubbleStyle}>
                <p style={{ margin: 0, whiteSpace: 'pre-wrap' }}>{message.text}</p>
              </div>
            </div>
          );
        })}
        
        {isLoading && (
          <div style={{ display: 'flex', justifyContent: 'flex-start' }}>
            <div style={{
              padding: '12px 16px',
              borderRadius: '18px 18px 18px 4px',
              background: colors.messageBg,
              border: `1px solid ${colors.border}`,
              color: colors.textMuted,
              fontSize: '14px'
            }}>
              Thinking...
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input Container */}
      <div style={inputContainerStyle}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask a question..."
          style={inputStyle}
          disabled={isLoading}
          onFocus={(e) => e.target.style.borderColor = isDarkMode ? 'rgba(0, 207, 217, 0.5)' : 'rgba(0, 0, 0, 0.3)'}
          onBlur={(e) => e.target.style.borderColor = colors.inputBorder}
        />
        <button
          onClick={() => handleSendMessage()}
          style={sendButtonStyle}
          disabled={isLoading || !inputValue.trim()}
          onMouseEnter={(e) => {
            if (!isLoading && inputValue.trim()) {
              e.target.style.background = colors.sendButtonHoverBg;
              e.target.style.transform = 'scale(1.05)';
            }
          }}
          onMouseLeave={(e) => {
            e.target.style.background = colors.sendButtonBg;
            e.target.style.transform = 'scale(1)';
          }}
          aria-label="Send message"
        >
          <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24" style={{ transform: 'rotate(90deg)' }}>
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
          </svg>
        </button>
      </div>
    </div>
  );
};

export default ChatOverlay;
