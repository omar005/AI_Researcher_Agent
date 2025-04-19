// frontend/src/App.js
import React, { useState, useEffect, useCallback } from 'react';
import ResearchForm from './components/ResearchForm';
import ResearchResults from './components/ResearchResults';
import ResearchProgress from './components/ResearchProgress';
import ChatHistory from './components/ChatHistory';
import { researchService } from './services/api';

function App() {
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [hasCompleted, setHasCompleted] = useState(false);
  const [history, setHistory] = useState([]);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  const [progressData, setProgressData] = useState(null);
  const [currentTaskId, setCurrentTaskId] = useState(null);

  const refreshHistory = useCallback(async () => {
    try {
      const updatedHistory = await researchService.getHistory();
      setHistory(updatedHistory);
      
      if (currentTaskId && updatedHistory.length > 0) {
        setResults(updatedHistory[0].results);
        setIsLoading(false);
        setHasCompleted(true);
      }
    } catch (error) {
      console.error('Failed to refresh history:', error);
    }
  }, [currentTaskId]);

  // Load history on component mount
  useEffect(() => {
    const loadHistory = async () => {
      if (localStorage.getItem('user_id')) {
        try {
          setIsLoadingHistory(true);
          const history = await researchService.getHistory();
          setHistory(history);
        } catch (error) {
          console.error('Failed to load history:', error);
        } finally {
          setIsLoadingHistory(false);
        }
      }
    };
    
    loadHistory();
  }, []);

  // Subscribe to progress updates when task ID changes
  useEffect(() => {
    if (!currentTaskId) return;
    
    const unsubscribe = researchService.subscribeToProgress(currentTaskId, (data) => {
      setProgressData(data);
      
      if (data.status === 'completed') {
        refreshHistory();
      }
    });
    
    return () => {
      unsubscribe();
    };
  }, [currentTaskId, refreshHistory]);

  const handleStartResearch = async (query, model) => {
    try {
      setIsLoading(true);
      setHasCompleted(false);
      setResults(null);
      setProgressData(null);
      
      const response = await researchService.startResearch(query, model);
      setCurrentTaskId(response.task_id);
      
      setProgressData({
        status: 'starting',
        message: `Starting research with ${model}...`,
        progress: 0
      });
    } catch (error) {
      setResults({
        error: error.response?.data?.error || 'An error occurred while researching. Please try again.',
        query: query,
      });
      setIsLoading(false);
      setHasCompleted(true);
    }
  };

  const handleSelectQuery = (historyItem) => {
    setResults(historyItem.results);
    setProgressData(null);
    setCurrentTaskId(null);
  };

  const handleClearHistory = async () => {
    try {
      await researchService.clearHistory();
      setHistory([]);
    } catch (error) {
      console.error('Failed to clear history:', error);
    }
  };

  const handleNewChat = () => {
    setResults(null);
    setProgressData(null);
    setCurrentTaskId(null);
    setIsLoading(false);
    setHasCompleted(false);
  };

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <header className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-gray-900">AI Research Agent</h1>
          <p className="mt-2 text-gray-600">
            Ask a research question and get comprehensive information from the web
          </p>
        </header>
        <main>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="md:col-span-1">
              <ChatHistory
                history={history}
                onSelectQuery={handleSelectQuery}
                onClearHistory={handleClearHistory}
                isLoading={isLoading || isLoadingHistory}
              />
            </div>
            <div className="md:col-span-2">
              <ResearchForm 
                onSubmit={handleStartResearch} 
                isLoading={isLoading}
                onNewChat={handleNewChat}
                hasCompleted={hasCompleted}
              />
              {progressData && <ResearchProgress progressData={progressData} />}
              <ResearchResults 
                results={results} 
                isLoading={isLoading && !progressData} 
              />
            </div>
          </div>
        </main>
        <footer className="mt-12 text-center text-gray-500 text-sm">
          <p>AI Research Agent &copy; {new Date().getFullYear()}</p>
        </footer>
      </div>
    </div>
  );
}

export default App;
