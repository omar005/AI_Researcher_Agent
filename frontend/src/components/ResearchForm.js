// frontend/src/components/ResearchForm.js
import React, { useState, useEffect } from 'react';
import { researchService } from '../services/api';

const ResearchForm = ({ onSubmit, isLoading, onNewChat, hasCompleted }) => {
  const [query, setQuery] = useState('');
  const [model, setModel] = useState('');
  const [models, setModels] = useState([]);
  const [loadingModels, setLoadingModels] = useState(true);
  const [modelError, setModelError] = useState('');

  useEffect(() => {
    const fetchModels = async () => {
      try {
        const data = await researchService.getModels();
        setModels(data.models || []);
        setModel(data.default || '');
      } catch (error) {
        console.error('Error fetching models:', error);
        setModelError('Failed to load models. Please refresh the page.');
      } finally {
        setLoadingModels(false);
      }
    };
    
    fetchModels();
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() && model) {
      onSubmit(query, model);
    }
  };

  const handleNewChatClick = () => {
    setQuery('');
    onNewChat();
  };

  return (
    <div className="mb-8 bg-white p-6 rounded-lg shadow-md relative">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold text-gray-800">AI Research Assistant</h2>
        <button
          type="button"
          onClick={handleNewChatClick}
          className="w-10 h-10 rounded-full bg-blue-600 text-white hover:bg-blue-700 flex items-center justify-center shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          title="New chat"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
        </button>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="mb-4 relative">
          <label htmlFor="query" className="block text-sm font-medium text-gray-700 mb-1">
            What would you like to research?
          </label>
          <textarea
            id="query"
            name="query"
            rows="3"
            className={`w-full px-3 py-2 pr-12 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 ${
              (isLoading || hasCompleted) ? 'bg-gray-100' : ''
            }`}
            placeholder="Enter your research topic or question..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            disabled={isLoading || hasCompleted}
            required
          />
        </div>
        
        <div className="mb-4">
          <label htmlFor="model" className="block text-sm font-medium text-gray-700 mb-1">
            Select Model
          </label>
          {modelError ? (
            <div className="text-red-500 text-sm mb-2">{modelError}</div>
          ) : (
            <select
              id="model"
              name="model"
              className={`w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 ${
                (isLoading || hasCompleted) ? 'bg-gray-100' : ''
              }`}
              value={model}
              onChange={(e) => setModel(e.target.value)}
              disabled={isLoading || loadingModels || hasCompleted}
              required
            >
              {loadingModels ? (
                <option value="">Loading models...</option>
              ) : models.length === 0 ? (
                <option value="">No models available</option>
              ) : (
                <>
                  <option value="">Select a model</option>
                  {models.map((modelName) => (
                    <option key={modelName} value={modelName}>
                      {modelName}
                    </option>
                  ))}
                </>
              )}
            </select>
          )}
        </div>
        
        <button
          type="submit"
          disabled={isLoading || loadingModels || !model || hasCompleted}
          className={`w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors ${
            (isLoading || loadingModels || !model || hasCompleted) ? 'opacity-50 cursor-not-allowed' : ''
          }`}
        >
          {isLoading ? 'Researching...' : 'Start Research'}
        </button>
      </form>
    </div>
  );
};

export default ResearchForm;
