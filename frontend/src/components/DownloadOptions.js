// frontend/src/components/DownloadOptions.js
import React, { useState } from 'react';
import { downloadAsText, downloadAsPDF, downloadAsJSON, downloadAsMarkdown } from '../utils/download';

const DownloadOptions = ({ results }) => {
  const [isOpen, setIsOpen] = useState(false);
  
  if (!results || !results.research) {
    return null;
  }
  
  const handleDownload = (format) => {
    const title = `Research: ${results.query}`;
    const filename = `research-${Date.now()}`;
    
    switch (format) {
      case 'text':
        downloadAsText(results.research, `${filename}.txt`);
        break;
      case 'pdf':
        downloadAsPDF(results.research, title, `${filename}.pdf`);
        break;
      case 'json':
        downloadAsJSON(results, `${filename}.json`);
        break;
      case 'markdown':
        downloadAsMarkdown(results.research, title, `${filename}.md`);
        break;
      default:
        break;
    }
    
    setIsOpen(false);
  };
  
  return (
    <div className="relative inline-block text-left">
      <div>
        <button
          type="button"
          className="inline-flex justify-center w-full rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          onClick={() => setIsOpen(!isOpen)}
        >
          Download
          <svg className="-mr-1 ml-2 h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
            <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        </button>
      </div>
      
      {isOpen && (
        <div className="origin-top-right absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 z-10">
          <div className="py-1" role="menu" aria-orientation="vertical" aria-labelledby="options-menu">
            <button
              onClick={() => handleDownload('text')}
              className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
              role="menuitem"
            >
              Download as Text (.txt)
            </button>
            <button
              onClick={() => handleDownload('pdf')}
              className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
              role="menuitem"
            >
              Download as PDF (.pdf)
            </button>
            <button
              onClick={() => handleDownload('markdown')}
              className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
              role="menuitem"
            >
              Download as Markdown (.md)
            </button>
            <button
              onClick={() => handleDownload('json')}
              className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
              role="menuitem"
            >
              Download Full Results as JSON (.json)
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default DownloadOptions;