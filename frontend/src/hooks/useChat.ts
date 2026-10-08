import { useAppDispatch, useAppSelector } from './useRedux';
import { addMessage, setLoading, setError, setSessionId, clearChat } from '../store/slices/chatSlice';
import { chatService } from '../services';
import { ChatMessage } from '../types';
import { getApiErrorMessage } from '../utils/api';

export const useChat = () => {
  const dispatch = useAppDispatch();
  const { messages, loading, error, sessionId } = useAppSelector(state => state.chat);

  const sendMessage = async (content: string) => {
    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: 'user',
      content,
      timestamp: new Date(),
    };

    dispatch(addMessage(userMessage));
    dispatch(setLoading(true));
    dispatch(setError(null));

    try {
      const response = await chatService.sendMessage(content, sessionId || undefined);
      dispatch(setSessionId(response.session_id));
      const assistantMessage: ChatMessage = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: response.answer,
        timestamp: new Date(),
      };
      dispatch(addMessage(assistantMessage));
      dispatch(setLoading(false));
    } catch (err: any) {
      const errorMessage = getApiErrorMessage(err, 'Chat service failed');
      dispatch(setError(errorMessage));
      dispatch(setLoading(false));
    }
  };

  const clearMessages = () => {
    dispatch(clearChat());
  };

  return {
    messages,
    loading,
    error,
    sendMessage,
    clearMessages,
  };
};
