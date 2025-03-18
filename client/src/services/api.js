import { API_BASE_URL, API_ENDPOINTS } from '../config/api';
import logger from '../utils/logger';

// Log the API base URL for debugging
console.log('API Base URL:', API_BASE_URL);
logger.info('API Base URL:', API_BASE_URL);

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
    console.log(`Making API request to: ${url}`);
    
    const options = {
      method,
      headers: {
        'Content-Type': 'application/json',
      },
      mode: 'cors',
      credentials: 'omit'
    };

    if (data) {
      options.body = JSON.stringify(data);
    }

    logger.apiRequest(endpoint, method, data);

    try {
      // Add timeout to the fetch request
      const timeoutPromise = new Promise((_, reject) => 
        setTimeout(() => reject(new Error('Request timeout - server might be down or unreachable')), 10000)
      );
      
      const response = await Promise.race([
        fetch(url, options),
        timeoutPromise
      ]);
      
      // For non-JSON responses or empty responses
      if (!response.ok) {
        if (response.status === 0) {
          throw new Error('Network error - check if the API server is running and CORS is configured correctly');
        }
        
        let errorMessage;
        try {
          const errorData = await response.json();
          errorMessage = errorData.error || `Server error: ${response.status}`;
        } catch (e) {
          errorMessage = `HTTP error: ${response.status} ${response.statusText}`;
        }
        
        throw new Error(errorMessage);
      }
      
      // Handle empty responses
      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        logger.warn(`Response is not JSON: ${contentType}`);
        return { success: true };
      }
      
      const responseData = await response.json();
      logger.apiResponse(endpoint, response.status, responseData);
      
      return responseData;
    } catch (error) {
      logger.error('API request failed:', error.message);
      console.error('API request failed:', error);
      
      // Provide more helpful error messages based on error type
      if (error.name === 'TypeError' && error.message === 'Failed to fetch') {
        console.error('Network error details:', {
          apiUrl: API_BASE_URL,
          endpoint,
          fullUrl: url,
          mode: options.mode
        });
      }
      
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
    // Use a simpler endpoint for health check
    return this.request('/health', 'GET').catch(error => {
      logger.error('Health check failed:', error.message);
      throw error;
    });
  }
}

export default new ApiService();
