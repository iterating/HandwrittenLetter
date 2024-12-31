/**
 * API configuration and storage utilities for the application
 */

// In production (Vercel), the API is served from the same domain
// In development, we need to specify the full URL
export const API_BASE_URL = import.meta.env.PROD ? '' : 'http://localhost:5000';

export const API_ENDPOINTS = {
    SAVE_LETTER: '/api/save-letter',
    RENDER: '/api/render',
    GENERATE_TEST_DATASET: '/api/generate-test-dataset',
    HEALTH: '/api/health'
};

// LocalStorage keys
const STORAGE_KEYS = {
    LETTERS: 'handwritten_letters',
    SETTINGS: 'handwritten_settings'
};

// Storage utility functions
export const storage = {
    // Save a letter to localStorage
    saveLetter: (letter, imageData, color = 'black') => {
        try {
            const letters = storage.getAllLetters();
            letters[`${letter}_${color}`] = imageData;
            localStorage.setItem(STORAGE_KEYS.LETTERS, JSON.stringify(letters));
            return true;
        } catch (error) {
            console.error('Error saving letter:', error);
            return false;
        }
    },

    // Get a specific letter from localStorage
    getLetter: (letter, color = 'black') => {
        try {
            const letters = storage.getAllLetters();
            return letters[`${letter}_${color}`] || null;
        } catch (error) {
            console.error('Error getting letter:', error);
            return null;
        }
    },

    // Get all stored letters
    getAllLetters: () => {
        try {
            const letters = localStorage.getItem(STORAGE_KEYS.LETTERS);
            return letters ? JSON.parse(letters) : {};
        } catch (error) {
            console.error('Error getting all letters:', error);
            return {};
        }
    },

    // Clear all stored letters
    clearLetters: () => {
        try {
            localStorage.removeItem(STORAGE_KEYS.LETTERS);
            return true;
        } catch (error) {
            console.error('Error clearing letters:', error);
            return false;
        }
    },

    // Save settings
    saveSettings: (settings) => {
        try {
            localStorage.setItem(STORAGE_KEYS.SETTINGS, JSON.stringify(settings));
            return true;
        } catch (error) {
            console.error('Error saving settings:', error);
            return false;
        }
    },

    // Get settings
    getSettings: () => {
        try {
            const settings = localStorage.getItem(STORAGE_KEYS.SETTINGS);
            return settings ? JSON.parse(settings) : null;
        } catch (error) {
            console.error('Error getting settings:', error);
            return null;
        }
    }
};

// Helper function to check if API is available
export const checkApiHealth = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.HEALTH}`);
        const data = await response.json();
        return data.status === 'healthy';
    } catch (error) {
        console.error('API Health Check Failed:', error);
        return false;
    }
};
