/**
 * API configuration for the application
 */

// Determine if we're in development or production
const isDevelopment = import.meta.env.DEV;

// In production, we'll use the API URL from environment variables
// In development, we'll use the proxy set up in vite.config.js (empty base URL)
export const API_BASE_URL = isDevelopment ? '' : (import.meta.env.VITE_API_URL || 'https://handwrittenletter.onrender.com');

// Log the environment and API configuration
console.log('Environment:', isDevelopment ? 'Development' : 'Production');
console.log('API Base URL:', API_BASE_URL || '(using proxy)');

export const API_ENDPOINTS = {
    SAVE_LETTER: '/api/save-letter',
    RENDER: '/api/render',
    GENERATE_TEST_DATASET: '/api/generate-test-dataset',
    GET_IMAGES_DIR: '/api/images-dir',
    SET_IMAGES_DIR: '/api/images-dir'
};

// Local storage key for images directory
export const IMAGES_DIR_KEY = 'handwritten_images_dir';

// Get images directory from localStorage or null if not set
export const getImagesDir = () => {
    return localStorage.getItem(IMAGES_DIR_KEY);
};

// Set images directory in localStorage
export const setImagesDir = (dir) => {
    localStorage.setItem(IMAGES_DIR_KEY, dir);
};
