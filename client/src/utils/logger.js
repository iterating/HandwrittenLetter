/**
 * Simple logging utility for the frontend
 */

// Log levels
export const LOG_LEVELS = {
  DEBUG: 'debug',
  INFO: 'info',
  WARN: 'warn',
  ERROR: 'error'
};

// Default log level (can be overridden with environment variable)
const DEFAULT_LOG_LEVEL = import.meta.env.VITE_LOG_LEVEL || LOG_LEVELS.INFO;

// Whether to enable logging to server
const ENABLE_REMOTE_LOGGING = import.meta.env.VITE_ENABLE_REMOTE_LOGGING === 'true';

// Remote logging endpoint
const REMOTE_LOG_ENDPOINT = `${import.meta.env.VITE_API_URL || ''}/api/log`;

/**
 * Determine if a log level should be displayed based on current settings
 */
const shouldLog = (level) => {
  const levels = Object.values(LOG_LEVELS);
  const currentLevelIndex = levels.indexOf(DEFAULT_LOG_LEVEL);
  const targetLevelIndex = levels.indexOf(level);
  
  return targetLevelIndex >= currentLevelIndex;
};

/**
 * Send log to remote server if enabled
 */
const remoteLog = async (level, ...args) => {
  if (!ENABLE_REMOTE_LOGGING) return;
  
  try {
    const message = args.map(arg => 
      typeof arg === 'object' ? JSON.stringify(arg) : String(arg)
    ).join(' ');
    
    // Use a timeout to prevent hanging requests
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 3000);
    
    await fetch(REMOTE_LOG_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        level,
        message,
        timestamp: new Date().toISOString(),
        userAgent: navigator.userAgent,
        url: window.location.href
      }),
      signal: controller.signal
    });
    
    clearTimeout(timeoutId);
  } catch (error) {
    // Silently fail - don't cause infinite loop of logging errors
    console.error('Remote logging failed:', error);
  }
};

/**
 * Logger object with methods for each log level
 */
const logger = {
  debug: (...args) => {
    if (shouldLog(LOG_LEVELS.DEBUG)) {
      console.debug('[DEBUG]', ...args);
      remoteLog(LOG_LEVELS.DEBUG, ...args);
    }
  },
  
  info: (...args) => {
    if (shouldLog(LOG_LEVELS.INFO)) {
      console.info('[INFO]', ...args);
      remoteLog(LOG_LEVELS.INFO, ...args);
    }
  },
  
  warn: (...args) => {
    if (shouldLog(LOG_LEVELS.WARN)) {
      console.warn('[WARN]', ...args);
      remoteLog(LOG_LEVELS.WARN, ...args);
    }
  },
  
  error: (...args) => {
    if (shouldLog(LOG_LEVELS.ERROR)) {
      console.error('[ERROR]', ...args);
      remoteLog(LOG_LEVELS.ERROR, ...args);
    }
  },
  
  // Log API request
  apiRequest: (endpoint, method, data) => {
    if (shouldLog(LOG_LEVELS.DEBUG)) {
      console.debug(`[API] ${method} ${endpoint}`, data);
      remoteLog(LOG_LEVELS.DEBUG, `API Request: ${method} ${endpoint}`, data);
    }
  },
  
  // Log API response
  apiResponse: (endpoint, status, data) => {
    const level = status >= 400 ? LOG_LEVELS.ERROR : LOG_LEVELS.DEBUG;
    if (shouldLog(level)) {
      console[level === LOG_LEVELS.ERROR ? 'error' : 'debug'](
        `[API] Response ${status} ${endpoint}`, data
      );
      remoteLog(level, `API Response: ${status} ${endpoint}`, data);
    }
  }
};

export default logger;
