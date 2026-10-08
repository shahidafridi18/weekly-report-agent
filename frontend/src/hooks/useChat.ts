import { useAppDispatch, useAppSelector } from './useRedux';
import { setMessages, addMessage, setLoading, setError } from '../store/slices/chatSlice';
import { chatService } from '../services';
import { ChatMessage } from '../types';
import { v4 as uuidv4 } from 'crypto';

export const useChat = () => {
  const dispatch = useAppDispatch();
  const { messages, loading, error } = useAppSelector(state => state.chat);

  const sendMessage = async (content: string) => {
    const userMessage: ChatMessage = {
      id: uuidv4(),
      role: 'user',
      content,
      timestamp: new Date(),
    };

    dispatch(addMessage(userMessage));
    dispatch(setLoading(true));
    dispatch(setError(null));

    try {
      const response = await chatService.sendMessage(content);
      const assistantMessage: ChatMessage = {
        id: uuidv4(),
        role: 'assistant',
        content: response.message,
        timestamp: new Date(),
      };
      dispatch(addMessage(assistantMessage));
      dispatch(setLoading(false));
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Chat service failed';
      dispatch(setError(errorMessage));
      dispatch(setLoading(false));
    }
  };

  const clearMessages = () => {
    dispatch(setMessages([]));
  };

  return {
    messages,
    loading,
    error,
    sendMessage,
    clearMessages,
  };
};
