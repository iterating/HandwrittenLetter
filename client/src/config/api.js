/**
 * API configuration for the application
 */

// Use environment variable for API URL in production
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

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
