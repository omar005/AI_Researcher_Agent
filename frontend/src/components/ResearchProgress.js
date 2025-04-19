// frontend/src/components/ResearchProgress.js
import React from 'react';

const ResearchProgress = ({ progressData }) => {
  // Don't render if no progress data
  if (!progressData) return null;

  const { status, message, progress } = progressData;

  // Determine status color
  const getStatusColor = (status) => {
    switch (status) {
      case 'planning':
        return 'bg-blue-500';
      case 'searching':
        return 'bg-purple-500';
      case 'synthesizing':
        return 'bg-teal-500';
      case 'reflecting':
        return 'bg-orange-500';
      case 'completed':
        return 'bg-green-500';
      case 'error':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };

  // Format status name for display
  const formatStatus = (status) => {
    if (!status) return 'Preparing';
    return status.charAt(0).toUpperCase() + status.slice(1);
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-md mb-6">
      <h2 className="text-xl font-bold mb-4 text-gray-800">Research Progress</h2>
      
      <div className="mb-2 flex justify-between">
        <span className="text-sm font-medium text-gray-700">
          {formatStatus(status)}
        </span>
        <span className="text-sm font-medium text-gray-700">
          {Math.round(progress)}%
        </span>
      </div>
      
      <div className="w-full bg-gray-200 rounded-full h-2.5">
        <div 
          className={`h-2.5 rounded-full ${getStatusColor(status)}`} 
          style={{ width: `${progress}%` }}
        ></div>
      </div>
      
      <p className="mt-2 text-sm text-gray-600">{message}</p>
      
      {status === 'error' && (
        <div className="mt-4 p-3 bg-red-100 border border-red-200 text-red-700 rounded">
          {message}
        </div>
      )}
    </div>
  );
};

export default ResearchProgress;