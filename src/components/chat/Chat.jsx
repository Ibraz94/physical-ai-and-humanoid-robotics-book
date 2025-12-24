import React, { useState } from 'react';
import ChatOverlay from './ChatOverlay';
import ChatIcon from './ChatIcon';
import SelectionHandler from './SelectionHandler';
import { ChatConfigProvider } from './ChatConfig';
import { useSession } from '../auth/auth-client';
import sessionStorage from '../auth/session-storage';
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

  // We use localStorage for sessions, so no need to verify with server
  // Just check localStorage directly
  React.useEffect(() => {
    // Quick check - no server call needed since we use localStorage
    setIsVerifying(false);
  }, []);

  const toggleChat = () => {
    // Check localStorage for authentication
    const localSession = sessionStorage.getSession();
    const hasValidSession = !!localSession?.user;
    console.log('Toggle chat clicked. Has valid session:', hasValidSession);
    console.log('Local session:', localSession);
    
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
    // Check localStorage for authentication
    const localSession = sessionStorage.getSession();
    const hasValidSession = !!localSession?.user;
    if (!hasValidSession) {
      // Don't do anything if not authenticated
      return;
    }
    setSelectedText(text);
    setIsChatOpen(true);
  };

  // Check if session is valid (check localStorage since cookies don't work cross-domain)
  const localSession = sessionStorage.getSession();
  const isAuthenticated = !!localSession?.user;
  
  // Debug logging
  React.useEffect(() => {
    console.log('Chat component - isAuthenticated:', isAuthenticated);
    console.log('Chat component - localSession:', localSession);
  }, [isAuthenticated, localSession]);

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
