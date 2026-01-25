'use client';

import React, { useEffect, useRef } from 'react';
import { authService } from '@/lib/auth';
import { apiClient } from '@/lib/api';
import ReactMarkdown from 'react-markdown';
import { useTaskContext } from '@/contexts/TaskContext';
import { useChatContext } from '@/contexts/ChatContext';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatInterfaceProps {
  onTaskAdded?: () => void;
}


const ChatInterface = React.memo(({ onTaskAdded }: ChatInterfaceProps = {}) => {
  const { fetchTasks } = useTaskContext();
  const { state, addMessage, setInputValue, setIsLoading, initializeChat } = useChatContext();
  const { messages, inputValue, isLoading } = state;
  const messagesEndRef = useRef<null | HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Initialize chat on mount
  useEffect(() => {
    initializeChat();
  }, []);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    // Add user message to chat
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    addMessage(userMessage);
    setInputValue('');
    setIsLoading(true);

    try {
      // Get the user ID from auth service
      const userId = authService.getCurrentUserId();
      if (!userId) {
        throw new Error('User not authenticated');
      }

      // Call the backend chat API
      const response = await apiClient.sendChatMessage(userId, inputValue, null);

      // Add assistant response to chat
      const assistantMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: response.response || 'I processed your request',
        timestamp: new Date(),
      };

      addMessage(assistantMessage);

      // Check for different operation types and update state accordingly
      const responseText = response.response.toLowerCase();

      // Check if the response indicates a task was added
      const taskAddedPhrases = [
        'added a task',
        'i\'ve added',
        'i have added',
        'created a task',
        'got it! i\'ve added',
        'got it! i have added',
        'added to your list',
        'created for you'
      ];

      // Check if the response indicates a task was updated
      const taskUpdatedPhrases = [
        'updated',
        'changed',
        'modified',
        'updated the task'
      ];

      // Check if the response indicates a task was completed
      const taskCompletedPhrases = [
        'marked as completed',
        'completed',
        'finished',
        'done',
        'marked the task as completed'
      ];

      // Check if the response indicates a task was deleted
      const taskDeletedPhrases = [
        'deleted',
        'removed',
        'deleted the task',
        'removed the task'
      ];

      if (taskAddedPhrases.some(phrase => responseText.includes(phrase))) {
        console.log("Task operation success – keeping chat open, history intact");
        // Refresh tasks to get the newly added task
        setTimeout(() => {
          fetchTasks();
          // Refocus input after operation
          if (inputRef.current) {
            inputRef.current.focus();
          }
        }, 500);
      } else if (taskUpdatedPhrases.some(phrase => responseText.includes(phrase))) {
        console.log("Task operation success – keeping chat open, history intact");
        // Refresh tasks to get the updated task
        setTimeout(() => {
          fetchTasks();
          // Refocus input after operation
          if (inputRef.current) {
            inputRef.current.focus();
          }
        }, 500);
      } else if (taskCompletedPhrases.some(phrase => responseText.includes(phrase))) {
        console.log("Task operation success – keeping chat open, history intact");
        // Refresh tasks to get the completed status
        setTimeout(() => {
          fetchTasks();
          // Refocus input after operation
          if (inputRef.current) {
            inputRef.current.focus();
          }
        }, 500);
      } else if (taskDeletedPhrases.some(phrase => responseText.includes(phrase))) {
        console.log("Task operation success – keeping chat open, history intact");
        // Refresh tasks to remove the deleted task
        setTimeout(() => {
          fetchTasks();
          // Refocus input after operation
          if (inputRef.current) {
            inputRef.current.focus();
          }
        }, 500);
      }
    } catch (error) {
      console.error('Error communicating with chat API:', error);

      // Add error message to chat
      const errorMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      };

      addMessage(errorMessage);
    } finally {
      setIsLoading(false);
      // Always refocus input after operation
      if (inputRef.current) {
        inputRef.current.focus();
      }
    }
  };

  // Ripple effect for send button
  const triggerRipple = (e: React.MouseEvent<HTMLButtonElement>) => {
    const button = e.currentTarget;
    const circle = document.createElement("span");
    const diameter = Math.max(button.clientWidth, button.clientHeight);
    const radius = diameter / 2;

    circle.style.width = circle.style.height = `${diameter}px`;
    circle.style.left = `${e.clientX - button.getBoundingClientRect().left - radius}px`;
    circle.style.top = `${e.clientY - button.getBoundingClientRect().top - radius}px`;
    circle.classList.add("absolute", "rounded-full", "bg-white/30", "animate-ripple");

    const ripple = button.getElementsByClassName("animate-ripple")[0];
    if (ripple) {
      ripple.remove();
    }

    button.appendChild(circle);
  };

  return (
    <div className="flex flex-col h-full max-w-4xl mx-auto bg-transparent">
      {/* Messages container */}
      <div className="flex-1 overflow-y-auto space-y-4 p-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-2xl px-4 py-3 transform transition-all duration-300 ${
                message.role === 'user'
                  ? 'bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-br-none opacity-0 animate-fade-in shadow-lg'
                  : 'bg-gradient-to-r from-slate-200 to-slate-300 text-gray-800 rounded-bl-none opacity-0 animate-fade-in shadow-md'
              }`}
            >
              <div className="prose prose-sm max-w-none">
                <ReactMarkdown
                  components={{
                    p: ({node, ...props}) => <p className="mb-2" {...props} />,
                    strong: ({node, ...props}) => <strong className="font-bold" {...props} />,
                    em: ({node, ...props}) => <em className="italic" {...props} />,
                    ol: ({node, ...props}) => <ol className="list-decimal list-inside mb-2" {...props} />,
                    ul: ({node, ...props}) => <ul className="list-disc list-inside mb-2" {...props} />,
                    li: ({node, ...props}) => <li className="mb-1 ml-4" {...props} />,
                  }}
                >
                  {message.content}
                </ReactMarkdown>
              </div>
              <p className={`text-xs mt-1 ${message.role === 'user' ? 'text-indigo-100' : 'text-gray-600'}`}>
                {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </p>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gradient-to-r from-slate-200 to-slate-300 text-gray-800 rounded-2xl rounded-bl-none px-4 py-3 shadow-md">
              <div className="flex items-center">
                <p>AI is thinking</p>
                <div className="ml-2 flex space-x-1">
                  <div className="w-2 h-2 bg-gray-600 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-600 rounded-full animate-bounce delay-75"></div>
                  <div className="w-2 h-2 bg-gray-600 rounded-full animate-bounce delay-150"></div>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input form */}
      <form onSubmit={handleSubmit} className="mt-2 p-2">
        <div className="relative flex gap-2">
          <input
            ref={inputRef}
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Message AI Assistant..."
            className="flex-1 border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-sm transition-all duration-200 bg-white"
            disabled={isLoading}
          />
          <button
            type="submit"
            onClick={triggerRipple}
            className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white px-6 py-3 rounded-xl hover:from-indigo-600 hover:to-purple-700 disabled:opacity-50 flex items-center justify-center shadow-md transition-all duration-200 hover:shadow-lg relative overflow-hidden group"
            disabled={isLoading || !inputValue.trim()}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
            <span className="absolute -top-1 -left-1 w-0 h-0 border-l-[10px] border-r-[10px] border-t-[10px] border-transparent border-t-white/30 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></span>
          </button>
        </div>
        <p className="mt-2 text-xs text-gray-500 text-center">
          Examples: "Add task to buy groceries", "Show my tasks", "Mark task 1 as complete"
        </p>
      </form>
    </div>
  );
});

export default ChatInterface;