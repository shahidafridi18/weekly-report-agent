import React, { useEffect, useRef, useState } from 'react';
import { ArrowUp, Bot, History, MessageSquare, Plus, Sparkles, UserRound } from 'lucide-react';
import { useChat } from '../../hooks';
import { formatDate } from '../../utils/formatters';

const suggestions = [
  'Compare Net CE between week 1 and week 2',
];

export const ChatInterface: React.FC = () => {
  const { messages, loading, error, sessionId, sessions, historyLoading, historyError, sendMessage, selectSession, clearMessages } = useChat();
  const [draft, setDraft] = useState('');
  const [historyOpen, setHistoryOpen] = useState(false);
  const messageArea = useRef<HTMLDivElement>(null);
  const composer = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    const area = messageArea.current;
    if (area) area.scrollTop = area.scrollHeight;
  }, [messages, loading]);

  const submit = async (text = draft) => {
    const message = text.trim();
    if (!message || loading) return;
    setDraft('');
    await sendMessage(message);
    composer.current?.focus();
  };

  const startNewChat = () => {
    if (loading) return;
    clearMessages();
    setDraft('');
    setHistoryOpen(false);
    composer.current?.focus();
  };

  return (
    <section className="flex h-full min-h-0 flex-col overflow-hidden rounded-2xl border border-mid-grey bg-white shadow-md">
      <header className="flex flex-shrink-0 items-center justify-between gap-3 border-b border-mid-grey bg-navy px-4 py-4 text-white sm:px-6">
        <div className="flex min-w-0 items-center gap-3">
          <div className="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-xl bg-blue">
            <MessageSquare className="h-5 w-5" />
          </div>
          <div className="min-w-0">
            <h1 className="truncate text-lg font-semibold sm:text-xl">Weekly insights chat</h1>
            <p className="truncate text-xs text-blue-100 sm:text-sm">Ask questions about your weekly reports</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
        <button type="button" onClick={() => setHistoryOpen(open => !open)}
          aria-label="Toggle chat history" className="rounded-lg border border-blue-200 p-2 text-white md:hidden">
          <History className="h-5 w-5" />
        </button>
        <button type="button" onClick={startNewChat} disabled={loading || historyLoading}
          className="inline-flex flex-shrink-0 items-center gap-2 rounded-lg border border-blue-200 bg-blue px-3 py-2 text-sm font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-white disabled:opacity-50"
          title="Start a fresh chat session">
          <Plus className="h-4 w-4" /><span>New chat</span>
        </button>
        </div>
      </header>

      <div className="flex min-h-0 flex-1 overflow-hidden">
      <aside className={`${historyOpen ? 'flex' : 'hidden'} w-full flex-shrink-0 flex-col border-r border-mid-grey bg-white md:flex md:w-60 lg:w-64`}>
        <div className="border-b border-mid-grey px-4 py-3">
          <h2 className="text-sm font-semibold text-navy">Conversation history</h2>
          <p className="text-xs text-dark-grey">Select a conversation to continue</p>
        </div>
        <div className="min-h-0 flex-1 space-y-1 overflow-y-auto p-2">
          {historyError && <p role="alert" className="rounded-lg bg-red-50 p-2 text-xs text-danger">{historyError}</p>}
          {sessions.length === 0 && !historyError && (
            <p className="px-3 py-5 text-center text-sm text-dark-grey">Your conversations will appear here after your first message.</p>
          )}
          {sessions.map(session => (
            <button key={session.session_id} type="button" disabled={loading || historyLoading}
              onClick={() => {
                void selectSession(session.session_id).then(opened => {
                  if (opened) {
                    setHistoryOpen(false);
                    setDraft('');
                  }
                });
              }}
              className={`w-full rounded-lg px-3 py-3 text-left transition-colors disabled:opacity-50 ${sessionId === session.session_id ? 'bg-light-blue text-navy' : 'text-dark-grey hover:bg-pale-blue'}`}
              title={session.title}
            >
              <p className="truncate text-sm font-medium">{session.title}</p>
              <p className="mt-1 truncate text-xs text-dark-grey">{session.turn_count} {session.turn_count === 1 ? 'exchange' : 'exchanges'} · {new Date(session.updated_at).toLocaleDateString()}</p>
            </button>
          ))}
        </div>
      </aside>

      <div className={`${historyOpen ? 'hidden md:flex' : 'flex'} min-h-0 min-w-0 flex-1 flex-col`}>
      <div ref={messageArea} role="log" aria-label="Chat messages" aria-live="polite"
        className="min-h-0 flex-1 overflow-y-auto overscroll-contain bg-pale-blue px-3 py-5 sm:px-6">
        {messages.length === 0 ? (
          <div className="mx-auto flex h-full max-w-xl flex-col items-center justify-center gap-5 py-8 text-center">
            <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-light-blue text-blue shadow-sm">
              <Sparkles className="h-8 w-8" />
            </div>
            <div className="space-y-2">
              <h2 className="text-xl font-semibold text-navy sm:text-2xl">What would you like to know?</h2>
              <p className="text-sm leading-relaxed text-dark-grey">
                Explore week-over-week changes, key metrics, and the counterparties behind them.
              </p>
            </div>
            <div className="grid w-full gap-2">
              {suggestions.map(suggestion => (
                <button key={suggestion} type="button" onClick={() => { setDraft(suggestion); composer.current?.focus(); }}
                  className="rounded-xl border border-mid-grey bg-white px-4 py-3 text-left text-sm text-navy shadow-sm transition-colors hover:border-blue hover:bg-light-blue focus:outline-none focus:ring-2 focus:ring-blue">
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="mx-auto max-w-3xl space-y-5">
            {messages.map(message => (
              <div key={message.id} className={`flex gap-2 sm:gap-3 ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                {message.role === 'assistant' && (
                  <div className="mt-1 flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-light-blue text-blue">
                    <Bot className="h-4 w-4" />
                  </div>
                )}
                <div className={`max-w-[85%] min-w-0 rounded-2xl px-4 py-3 shadow-sm sm:max-w-[78%] ${message.role === 'user' ? 'rounded-br-sm bg-blue text-white' : 'rounded-bl-sm border border-mid-grey bg-white text-navy'}`}>
                  <p className="whitespace-pre-wrap break-words text-sm leading-relaxed sm:text-base">{message.content}</p>
                  <p className={`mt-2 text-right text-xs ${message.role === 'user' ? 'text-blue-100' : 'text-dark-grey'}`}>
                    {formatDate(message.timestamp)}
                  </p>
                </div>
                {message.role === 'user' && (
                  <div className="mt-1 flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-light-blue text-blue">
                    <UserRound className="h-4 w-4" />
                  </div>
                )}
              </div>
            ))}
            {loading && (
              <div className="flex items-center gap-3 text-sm text-dark-grey" role="status">
                <span className="flex h-8 w-8 items-center justify-center rounded-full bg-light-blue text-blue"><Bot className="h-4 w-4" /></span>
                <span className="rounded-xl border border-mid-grey bg-white px-4 py-3">Analyzing your question...</span>
              </div>
            )}
          </div>
        )}
      </div>

      <footer className="flex-shrink-0 border-t border-mid-grey bg-white p-3 sm:p-4">
        <div className="mx-auto max-w-3xl">
          {error && <div role="alert" className="mb-3 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-danger">{error}</div>}
          <form onSubmit={event => { event.preventDefault(); void submit(); }}
            className="flex items-end gap-2 rounded-xl border border-mid-grey bg-white p-2 shadow-sm focus-within:border-blue focus-within:ring-2 focus-within:ring-blue-100 sm:gap-3">
            <textarea ref={composer} rows={2} value={draft} onChange={event => setDraft(event.target.value)}
              onKeyDown={event => { if (event.key === 'Enter' && !event.shiftKey) { event.preventDefault(); void submit(); } }}
              placeholder="Ask about your weekly report..." aria-label="Chat message" disabled={loading}
              className="max-h-32 min-h-[2.8rem] w-full min-w-0 flex-1 resize-none border-0 bg-transparent px-2 py-2 text-sm text-navy outline-none focus:outline-none focus:ring-0 disabled:opacity-60 sm:text-base" />
            <button type="submit" disabled={!draft.trim() || loading} aria-label="Send message"
              className="flex h-11 w-11 flex-shrink-0 items-center justify-center rounded-lg bg-blue text-white hover:bg-navy focus:outline-none focus:ring-2 focus:ring-blue disabled:cursor-not-allowed disabled:opacity-40">
              <ArrowUp className="h-5 w-5" />
            </button>
          </form>
          <p className="mt-2 text-center text-xs text-dark-grey">Press Enter to send · Shift + Enter for a new line</p>
        </div>
      </footer>
      </div>
      </div>
    </section>
  );
};
