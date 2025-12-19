import React from 'react';
import Chat from '../components/chat/Chat';
import UserMenu from '../components/UserMenu';
import '../css/chatkit-custom.css';

// Root component that wraps the entire app
export default function Root({children}) {
  return (
    <>
      {children}
      <Chat />
    </>
  );
}
