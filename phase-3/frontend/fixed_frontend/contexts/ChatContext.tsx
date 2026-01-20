'use client';

import React, { createContext, useContext, useState, useRef, ReactNode } from 'react';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatState {
  messages: Message[];
  isLoading: boolean;
  inputValue: string;
}

interface ChatContextType {
  state: ChatState;
  addMessage: (message: Message) => void;
  setInputValue: (value: string) => void;
  setIsLoading: (loading: boolean) => void;
  initializeChat: () => void;
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const ChatProvider = ({ children }: { children: ReactNode }) => {
  // Use useRef to initialize messages only once and persist across re-renders
  const messagesRef = useRef<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I\'m your AI Chatbot. How can I help you manage your tasks today?',
      timestamp: new Date(),
    },
  ]);
  
  const [state, setState] = useState<ChatState>({
    messages: messagesRef.current,
    isLoading: false,
    inputValue: ''
  });

  const initializeChat = () => {
    if (messagesRef.current.length === 1) {
      // Only initialize if it hasn't been initialized yet
      messagesRef.current = [
        {
          id: '1',
          role: 'assistant',
          content: 'Hello! I\'m your AI Chatbot. How can I help you manage your tasks today?',
          timestamp: new Date(),
        },
      ];
      setState(prev => ({
        ...prev,
        messages: messagesRef.current
      }));
    }
  };

  const addMessage = (message: Message) => {
    messagesRef.current = [...messagesRef.current, message];
    setState(prev => ({
      ...prev,
      messages: messagesRef.current
    }));
  };

  const setInputValue = (value: string) => {
    setState(prev => ({
      ...prev,
      inputValue: value
    }));
  };

  const setIsLoading = (loading: boolean) => {
    setState(prev => ({
      ...prev,
      isLoading: loading
    }));
  };

  return (
    <ChatContext.Provider value={{ 
      state, 
      addMessage, 
      setInputValue, 
      setIsLoading,
      initializeChat
    }}>
      {children}
    </ChatContext.Provider>
  );
};

export const useChatContext = () => {
  const context = useContext(ChatContext);
  if (!context) {
    throw new Error('useChatContext must be used within a ChatProvider');
  }
  return context;
};