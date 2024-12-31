/**
 * API configuration for the application
 */

// In production (Vercel), the API is served from the same domain
// In development, we need to specify the full URL
export const API_BASE_URL = import.meta.env.PROD ? '' : 'http://localhost:5000';

export const API_ENDPOINTS = {
    SAVE_LETTER: '/api/save-letter',
    RENDER: '/api/render',
    GENERATE_TEST_DATASET: '/api/generate-test-dataset'
};
