import React, { useState } from 'react';
import ChatOverlay from './ChatOverlay';
import ChatIcon from './ChatIcon';
import SelectionHandler from './SelectionHandler';
import { ChatConfigProvider } from './ChatConfig';
import { useSession } from '../auth/auth-client';
import { useHistory } from '@docusaurus/router';

/**
 * Main Chat component that integrates all chat functionality
 * Includes the chat icon, overlay, and selection handler
 * Requires authentication to use
 */
const Chat = () => {
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [selectedText, setSelectedText] = useState(null);
  const [isVerifying, setIsVerifying] = useState(true);
  const { data: session, isLoading } = useSession();
  const history = useHistory();

  // Verify session on mount
  React.useEffect(() => {
    const verifySession = async () => {
      try {
        // Try to get fresh session from server
        const response = await fetch('https://ibraz-api-ai-book.hf.space/api/auth/session', {
          credentials: 'include'
        });
        
        if (!response.ok) {
          console.log('No valid session found');
          setIsVerifying(false);
          return;
        }
        
        const data = await response.json();
        console.log('Session verified:', data);
        setIsVerifying(false);
      } catch (error) {
        console.error('Error verifying session:', error);
        setIsVerifying(false);
      }
    };

    verifySession();
  }, []);

  const toggleChat = () => {
    const hasValidSession = session?.user && session?.session;
    console.log('Toggle chat clicked. Has valid session:', hasValidSession);
    
    // Don't open chat if not authenticated, just show tooltip
    if (!hasValidSession) {
      console.log('Not authenticated, showing tooltip only');
      return;
    }
    console.log('Authenticated, toggling chat');
    setIsChatOpen(!isChatOpen);
  };

  const closeChat = () => {
    setIsChatOpen(false);
  };

  const handleAskQuestion = (text) => {
    const hasValidSession = session?.user && session?.session;
    if (!hasValidSession) {
      // Don't do anything if not authenticated
      return;
    }
    setSelectedText(text);
    setIsChatOpen(true);
  };

  // Check if session is valid (has both user and session data)
  const isAuthenticated = !isLoading && !isVerifying && !!session?.user && !!session?.session;

  return (
    <>
      <ChatConfigProvider>
        {/* Only show selection handler if authenticated */}
        {isAuthenticated && <SelectionHandler onAskQuestion={handleAskQuestion} />}
        
        {/* Always show chat icon, but with tooltip if not authenticated */}
        <ChatIcon 
          onToggle={toggleChat} 
          isOpen={isChatOpen && isAuthenticated}
          isAuthenticated={isAuthenticated}
        />
        
        {/* Only show overlay if authenticated AND chat is open */}
        {isAuthenticated && isChatOpen && (
          <ChatOverlay
            isOpen={true}
            onClose={closeChat}
            selectedText={selectedText}
          />
        )}
      </ChatConfigProvider>
    </>
  );
};

export default Chat;
