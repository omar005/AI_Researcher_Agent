// frontend/src/components/ChatHistory.js
import React from 'react';

const ChatHistory = ({ history, onSelectQuery, onClearHistory, isLoading }) => {
  if (history.length === 0) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md mb-8">
        <h2 className="text-2xl font-bold mb-4 text-gray-800">Chat History</h2>
        <p className="text-gray-600">No research history yet.</p>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-md mb-8">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold text-gray-800">Chat History</h2>
        <button
          onClick={onClearHistory}
          disabled={isLoading}
          className="px-3 py-1 text-sm text-red-600 hover:text-red-800 focus:outline-none"
        >
          Clear History
        </button>
      </div>
      <div className="max-h-80 overflow-y-auto">
        <ul className="divide-y divide-gray-200">
          {history.map((item) => (
            <li key={item.id} className="py-3">
              <button
                onClick={() => onSelectQuery(item)}
                disabled={isLoading}
                className="w-full text-left hover:bg-gray-50 p-2 rounded transition-colors duration-200"
              >
                <p className="text-sm font-medium text-gray-800 truncate">{item.query}</p>
                <p className="text-xs text-gray-500 mt-1">
                  {new Date(item.timestamp * 1000).toLocaleString()}
                </p>
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default ChatHistory;