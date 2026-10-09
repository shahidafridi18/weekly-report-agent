import { useCallback, useEffect, useState } from 'react';
import { useAppDispatch, useAppSelector } from './useRedux';
import { addMessage, setLoading, setError, setSessionId, openChat, clearChat } from '../store/slices/chatSlice';
import { chatService } from '../services';
import { ChatMessage, ChatSessionSummary } from '../types';
import { getApiErrorMessage } from '../utils/api';

export const useChat = () => {
  const dispatch = useAppDispatch();
  const { messages, loading, error, sessionId } = useAppSelector(state => state.chat);
  const [sessions, setSessions] = useState<ChatSessionSummary[]>([]);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [historyError, setHistoryError] = useState<string | null>(null);

  const refreshSessions = useCallback(async () => {
    try {
      const items = await chatService.listSessions();
      setSessions(items);
      setHistoryError(null);
    } catch (err) {
      setHistoryError(getApiErrorMessage(err, 'Could not load conversation history'));
    }
  }, []);

  useEffect(() => {
    void refreshSessions();
  }, [refreshSessions]);

  const sendMessage = async (content: string) => {
    if (loading) return;
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
      dispatch(addMessage({
        id: crypto.randomUUID(),
        role: 'assistant',
        content: response.answer,
        timestamp: new Date(),
      }));
      await refreshSessions();
    } catch (err) {
      dispatch(setError(getApiErrorMessage(err, 'Chat service failed')));
    } finally {
      dispatch(setLoading(false));
    }
  };

  const selectSession = async (selectedId: string) => {
    if (loading || historyLoading) return false;
    setHistoryLoading(true);
    setHistoryError(null);
    try {
      const detail = await chatService.getSession(selectedId);
      const restored: ChatMessage[] = detail.turns.flatMap((turn, index) => {
        const timestamp = new Date(turn.created_at);
        return [
          { id: `${selectedId}-user-${index}`, role: 'user' as const, content: turn.message, timestamp },
          { id: `${selectedId}-assistant-${index}`, role: 'assistant' as const, content: turn.answer, timestamp },
        ];
      });
      dispatch(openChat({ sessionId: selectedId, messages: restored }));
      return true;
    } catch (err) {
      setHistoryError(getApiErrorMessage(err, 'Could not open conversation'));
      return false;
    } finally {
      setHistoryLoading(false);
    }
  };

  const clearMessages = () => {
    if (!loading && !historyLoading) dispatch(clearChat());
  };

  return {
    messages,
    loading,
    error,
    sessionId,
    sessions,
    historyLoading,
    historyError,
    sendMessage,
    selectSession,
    refreshSessions,
    clearMessages,
  };
};
