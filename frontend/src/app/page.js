'use client';

import React, { useState } from 'react';
import { ChatInterface } from '@/components/ChatInterface';
import { useResearchStream } from '@/hooks/useResearchStream';
import { ThemeToggle } from '@/components/ThemeToggle';

export default function Home() {
  const { messages, isLoading, startResearch, stopResearch } = useResearchStream();
  const [userMessages, setUserMessages] = useState([]);

  const handleSend = (topic) => {
    const userMessage = {
      type: 'user',
      content: topic,
      timestamp: Date.now()
    };
    setUserMessages(prev => [...prev, userMessage]);
    startResearch(topic);
  };

  const handleStop = () => {
    stopResearch();
  };

  const displayMessages = [
    ...userMessages,
    ...messages
  ].sort((a, b) => a.timestamp - b.timestamp);

  return (
    <div className="flex h-screen w-full flex-col bg-gray-50 dark:bg-gray-950 font-sans text-slate-900 dark:text-gray-100 overflow-hidden">
      <header className="h-16 flex-none border-b border-gray-200 dark:border-gray-800 flex items-center px-4 sm:px-6 bg-white dark:bg-gray-900 justify-between z-10">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-gradient-to-br from-blue-600 to-purple-600 rounded-lg flex items-center justify-center text-white font-bold shadow-lg">
            RA
          </div>
          <h1 className="font-bold text-lg sm:text-xl bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent hidden sm:block">
            ResearchAgent Pro
          </h1>
          <h1 className="font-bold text-lg bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent sm:hidden">
            RA Pro
          </h1>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-xs sm:text-sm text-gray-500 dark:text-gray-400 hidden sm:block">
            Powered by CrewAI & LangGraph
          </div>
          <ThemeToggle />
        </div>
      </header>

      <main className="flex-1 flex flex-col min-h-0 w-full max-w-5xl mx-auto bg-white dark:bg-gray-900 shadow-xl border-x border-gray-200 dark:border-gray-800">
        <ChatInterface
          messages={displayMessages}
          isLoading={isLoading}
          onSend={handleSend}
          onStop={handleStop}
        />
      </main>
    </div>
  );
}
