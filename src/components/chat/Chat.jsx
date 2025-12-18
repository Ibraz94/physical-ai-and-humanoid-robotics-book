import React, { useState } from 'react';
import ChatOverlay from './ChatOverlay';
import ChatIcon from './ChatIcon';
import SelectionHandler from './SelectionHandler';
import { ChatConfigProvider } from './ChatConfig';

/**
 * Main Chat component that integrates all chat functionality
 * Includes the chat icon, overlay, and selection handler
 */
const Chat = () => {
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [selectedText, setSelectedText] = useState(null);

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  const closeChat = () => {
    setIsChatOpen(false);
  };

  const handleAskQuestion = (text) => {
    setSelectedText(text);
    setIsChatOpen(true);
  };

  return (
    <>
      <ChatConfigProvider>
        <SelectionHandler onAskQuestion={handleAskQuestion} />
        <ChatIcon onToggle={toggleChat} isOpen={isChatOpen} />
        <ChatOverlay
          isOpen={isChatOpen}
          onClose={closeChat}
          selectedText={selectedText}
        />
      </ChatConfigProvider>
    </>
  );
};

export default Chat;
