// frontend/src/components/ResearchResults.js
import React from 'react';
import ReactMarkdown from 'react-markdown';
import DownloadOptions from './DownloadOptions';

const ResearchResults = ({ results, isLoading }) => {
  if (isLoading) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md">
        <div className="flex items-center justify-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
          <span className="ml-2 text-gray-600">Researching... This may take a minute or two.</span>
        </div>
      </div>
    );
  }

  if (!results) {
    return null;
  }

  if (results.error) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-bold mb-4 text-red-600">Error</h2>
        <p className="text-gray-700">{results.error}</p>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold text-gray-800">Research Results</h2>
        <DownloadOptions results={results} />
      </div>
      
      <div className="mb-6">
        <h3 className="font-semibold text-gray-800 mb-2">Query:</h3>
        <p className="text-gray-700">{results.query}</p>
      </div>
      
      <div className="mb-6">
        <h3 className="font-semibold text-gray-800 mb-2">Research:</h3>
        <div className="prose max-w-none text-gray-700">
          <ReactMarkdown>{results.research}</ReactMarkdown>
        </div>
      </div>
      
      <div className="mb-6">
        <h3 className="font-semibold text-gray-800 mb-2">Search Queries Used:</h3>
        <ul className="list-disc pl-5 text-gray-700">
          {results.search_queries.map((query, index) => (
            <li key={index}>{query}</li>
          ))}
        </ul>
      </div>
      
      <div>
        <h3 className="font-semibold text-gray-800 mb-2">Sources:</h3>
        <ul className="list-disc pl-5 text-gray-700">
          {results.search_results.map((result, index) => (
            <li key={index}>
              <a 
                href={result.link} 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-blue-600 hover:underline"
              >
                {result.title || 'Untitled Source'}
              </a>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default ResearchResults;