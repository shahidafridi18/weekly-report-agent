import React, { useState, useRef, useEffect } from 'react';
import { useChat } from '../../hooks';
import { Button, Loading } from '../common';
import { Send, MessageCircle } from 'lucide-react';
import { CHAT_PLACEHOLDER } from '../../utils/constants';
import { formatDate } from '../../utils/formatters';

export const ChatInterface: React.FC = () => {
  const { messages, loading, sendMessage } = useChat();
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const message = inputValue;
    setInputValue('');
    await sendMessage(message);
  };

  return (
    <div className="flex flex-col h-screen bg-white">
      {/* Header */}
      <div className="bg-navy text-white p-4 md:p-6 shadow-md">
        <div className="flex items-center gap-3">
          <MessageCircle className="w-6 h-6" />
          <div>
            <h1 className="text-xl font-bold">Chat with AI</h1>
            <p className="text-sm text-gray-200">Ask questions about your analysis</p>
          </div>
        </div>
      </div>

      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-4 bg-pale-blue">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <MessageCircle className="w-16 h-16 text-mid-grey mx-auto mb-4" />
              <p className="text-dark-grey">No messages yet. Start by asking a question!</p>
            </div>
          </div>
        ) : (
          <>
            {messages.map(msg => (
              <div
                key={msg.id}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-xs md:max-w-md lg:max-w-lg px-4 py-3 rounded-lg ${
                    msg.role === 'user'
                      ? 'bg-blue text-white rounded-br-none'
                      : 'bg-white text-dark-grey border border-mid-grey rounded-bl-none'
                  }`}
                >
                  <p className="text-sm mb-1">{msg.content}</p>
                  <p className={`text-xs ${msg.role === 'user' ? 'text-blue-100' : 'text-dark-grey'}`}>
                    {formatDate(msg.timestamp)}
                  </p>
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-white text-dark-grey border border-mid-grey px-4 py-3 rounded-lg">
                  <div className="flex gap-2">
                    <div className="w-2 h-2 bg-mid-grey rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-mid-grey rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-mid-grey rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Input Form */}
      <form onSubmit={handleSubmit} className="bg-white border-t border-mid-grey p-4 md:p-6">
        <div className="flex gap-3">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder={CHAT_PLACEHOLDER}
            disabled={loading}
            className="flex-1 px-4 py-2 border border-mid-grey rounded-lg focus:outline-none focus:ring-2 focus:ring-blue disabled:bg-gray-100"
          />
          <Button
            type="submit"
            variant="primary"
            size="md"
            isLoading={loading}
            disabled={loading || !inputValue.trim()}
          >
            <Send className="w-4 h-4" />
          </Button>
        </div>
      </form>
    </div>
  );
};
