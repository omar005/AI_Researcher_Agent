// frontend/src/services/api.js (updated)
import axios from 'axios';
import { io } from 'socket.io-client';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
const WS_URL = process.env.REACT_APP_WS_URL || 'http://localhost:5000';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': process.env.REACT_APP_API_KEY
  }
});

// Add interceptor to include user ID in requests if available
apiClient.interceptors.request.use(config => {
  const userId = localStorage.getItem('user_id');
  if (userId) {
    config.headers['X-User-ID'] = userId;
  }
  return config;
});

// Create socket.io connection
let socket = null;

const getSocket = () => {
  if (!socket) {
    socket = io(WS_URL, {
      extraHeaders: {
        'X-API-Key': process.env.REACT_APP_API_KEY
      }
    });
    
    socket.on('disconnect', () => {
      console.log('WebSocket disconnected');
    });
  }
  
  return socket;
};

export const researchService = {
  /**
   * Get available models
   * @returns {Promise} Promise with available models
   */
  getModels: async () => {
    try {
      const response = await apiClient.get('/models');
      return response.data;
    } catch (error) {
      console.error('Error getting models:', error);
      throw error;
    }
  },
  
  
  

  /**
   * Start a research task
   * @param {string} query - The research query
   * @param {string} model - The model to use
   * @returns {Promise} - Promise with the task ID and initial status
   */
  startResearch: async (query, model) => {
    try {
      const response = await apiClient.post('/research', { query, model });
      
      // Store user ID if returned
      if (response.data.user_id) {
        localStorage.setItem('user_id', response.data.user_id);
      }
      
      return response.data;
    } catch (error) {
      console.error('Error starting research:', error);
      throw error;
    }
  },
  
  /**
   * Subscribe to research progress updates
   * @param {string} taskId - The task ID
   * @param {Function} callback - Callback function for updates
   * @returns {Function} - Unsubscribe function
   */
  subscribeToProgress: (taskId, callback) => {
    const socket = getSocket();
    
    // Join task room
    socket.emit('join_task', { task_id: taskId });
    
    // Set up progress event handler
    const handleProgress = (data) => {
      if (data.task_id === taskId) {
        callback(data);
      }
    };
    
    // Subscribe to progress events
    socket.on('research_progress', handleProgress);
    
    // Return unsubscribe function
    return () => {
      socket.off('research_progress', handleProgress);
    };
  },
  
  /**
   * Get research history
   * @returns {Promise} - Promise with research history
   */
  getHistory: async () => {
    try {
      const response = await apiClient.get('/history');
      return response.data.history;
    } catch (error) {
      console.error('Error getting history:', error);
      throw error;
    }
  },
  
  /**
   * Clear research history
   * @returns {Promise} - Promise with success status
   */
  clearHistory: async () => {
    try {
      const response = await apiClient.delete('/history');
      return response.data;
    } catch (error) {
      console.error('Error clearing history:', error);
      throw error;
    }
  }
};
