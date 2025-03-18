import { API_BASE_URL, API_ENDPOINTS } from '../config/api';
import logger from '../utils/logger';

/**
 * API service for making requests to the backend
 */
class ApiService {
  /**
   * Make a request to the API
   * @param {string} endpoint - API endpoint
   * @param {string} method - HTTP method
   * @param {object} data - Request data
   * @returns {Promise} - Response data
   */
  async request(endpoint, method = 'GET', data = null) {
    const url = `${API_BASE_URL}${endpoint}`;
    const options = {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
    };

    if (data) {
      options.body = JSON.stringify(data);
    }

    logger.apiRequest(endpoint, method, data);

    try {
      const response = await fetch(url, options);
      const responseData = await response.json();
      
      logger.apiResponse(endpoint, response.status, responseData);
      
      if (!response.ok) {
        throw new Error(responseData.error || 'An error occurred');
      }
      
      return responseData;
    } catch (error) {
      logger.error('API request failed:', error.message);
      throw error;
    }
  }

  /**
   * Save a letter drawing
   * @param {string} letter - The letter being saved
   * @param {string} imageData - Base64 encoded image data
   * @returns {Promise} - Response data
   */
  saveLetter(letter, imageData) {
    return this.request(API_ENDPOINTS.SAVE_LETTER, 'POST', { letter, imageData });
  }

  /**
   * Render handwritten text
   * @param {string} text - Text to render
   * @returns {Promise} - Response data with HTML content
   */
  renderHandwriting(text) {
    return this.request(API_ENDPOINTS.RENDER, 'POST', { text });
  }

  /**
   * Generate a test dataset
   * @param {string} letterlist - List of letters to generate
   * @returns {Promise} - Response data
   */
  generateTestDataset(letterlist) {
    return this.request(API_ENDPOINTS.GENERATE_TEST_DATASET, 'POST', { letterlist });
  }

  /**
   * Check server health
   * @returns {Promise} - Response data
   */
  healthCheck() {
    return this.request('/health', 'GET');
  }
}

export default new ApiService();
