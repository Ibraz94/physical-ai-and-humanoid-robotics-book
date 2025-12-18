import React, { createContext, useContext } from 'react';

/**
 * Chat configuration context
 */
const ChatConfigContext = createContext({
  backendUrl: 'http://localhost:8000',
  apiKey: 'test-api-key-12345'
});

export const ChatConfigProvider = ({ children, config = {} }) => {
  const defaultConfig = {
    backendUrl: config.backendUrl || 'http://localhost:8000',
    apiKey: config.apiKey || 'test-api-key-12345'
  };

  return (
    <ChatConfigContext.Provider value={defaultConfig}>
      {children}
    </ChatConfigContext.Provider>
  );
};

export const useChatConfig = () => {
  return useContext(ChatConfigContext);
};

export default ChatConfigContext;
