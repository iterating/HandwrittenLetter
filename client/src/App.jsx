import React, { useState, useRef, useEffect } from 'react';
import DrawingCanvas from './components/DrawingCanvas';
import apiService from './services/api';
import logger from './utils/logger';
import './App.css';

const LETTER_LIST = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

function App() {
  const [text, setText] = useState('');
  const [message, setMessage] = useState('');
  const [currentLetter, setCurrentLetter] = useState(LETTER_LIST[0]);
  const [letterIndex, setLetterIndex] = useState(0);
  const [renderedHtml, setRenderedHtml] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const canvasRef = useRef(null);
  const iframeRef = useRef(null);
  
  useEffect(() => {
    // Check server health on component mount
    const checkHealth = async () => {
      try {
        await apiService.healthCheck();
        logger.info('Server connection established');
      } catch (error) {
        logger.error('Server connection failed:', error.message);
        setMessage('Warning: Cannot connect to server. Some features may not work.');
      }
    };
    
    checkHealth();
  }, []);
  
  const generateTestDataset = async () => {
    try {
      setIsLoading(true);
      logger.info('Generating test dataset');
      
      const data = await apiService.generateTestDataset(LETTER_LIST);
      
      setMessage(data.success ? `${data.message}. Try drawing or rendering some text!` : data.error);
      logger.info('Test dataset generated successfully');
    } catch (error) {
      logger.error('Failed to generate test dataset:', error.message);
      setMessage('Error: ' + error.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDrawingSave = async (imageData) => {
    try {
      setIsLoading(true);
      logger.info(`Saving letter: ${currentLetter}`);
      
      const data = await apiService.saveLetter(currentLetter, imageData);
      
      if (data.success) {
        setMessage(`Saved letter ${currentLetter}`);
        logger.info(`Letter ${currentLetter} saved successfully`);
        
        // Move to next letter
        const nextIndex = letterIndex + 1;
        if (nextIndex < LETTER_LIST.length) {
          setLetterIndex(nextIndex);
          setCurrentLetter(LETTER_LIST[nextIndex]);
          logger.debug(`Moving to next letter: ${LETTER_LIST[nextIndex]}`);
        } else {
          setMessage('Completed all letters! Try rendering some text.');
          logger.info('All letters completed');
        }
        
        // Clear canvas
        canvasRef.current?.clear();
      } else {
        logger.warn('Failed to save letter:', data.error);
        setMessage(data.error || 'Error saving letter');
      }
    } catch (error) {
      logger.error('Error saving letter:', error.message);
      setMessage('Error: ' + error.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleRender = async () => {
    if (!text.trim()) {
      logger.warn('No text provided for rendering');
      setMessage('Please enter some text to render');
      return;
    }
    
    try {
      setIsLoading(true);
      logger.info(`Rendering text: ${text.substring(0, 50)}${text.length > 50 ? '...' : ''}`);
      
      const data = await apiService.renderHandwriting(text);
      
      if (data.success) {
        setRenderedHtml(data.html_content);
        const container = document.getElementById('rendered-output');
        if (container) {
          const iframe = document.createElement('iframe');
          iframeRef.current = iframe;
          Object.assign(iframe.style, {
            width: '100%',
            height: '500px',
            border: '1px solid #ccc',
            borderRadius: '4px'
          });
          
          container.innerHTML = '';
          container.appendChild(iframe);
          
          const doc = iframe.contentDocument || iframe.contentWindow.document;
          doc.open();
          doc.write(data.html_content);
          doc.close();
          
          setMessage('Handwriting rendered successfully');
          logger.info('Handwriting rendered successfully');
        }
      } else {
        logger.warn('Failed to render handwriting:', data.error);
        setMessage(data.error || 'Error rendering handwriting');
      }
    } catch (error) {
      logger.error('Error rendering handwriting:', error.message);
      setMessage('Error: ' + error.message);
    } finally {
      setIsLoading(false);
    }
  };

  const copyToClipboard = async () => {
    try {
      if (!renderedHtml) {
        logger.warn('No rendered content to copy');
        setMessage('Please render some text first');
        return;
      }

      const iframe = iframeRef.current;
      if (iframe) {
        const doc = iframe.contentDocument || iframe.contentWindow.document;
        const content = doc.body.innerHTML;
        await navigator.clipboard.writeText(content);
        setMessage('Copied to clipboard!');
        logger.info('Content copied to clipboard');
      }
    } catch (error) {
      logger.error('Error copying to clipboard:', error.message);
      setMessage('Error copying to clipboard: ' + error.message);
    }
  };

  return (
    <div className="app">
      <h1>Handwriting Generator</h1>
      
      <div className="drawing-section">
        <h2>Draw Letters</h2>
        <div className="current-letter">
          <p>Current Letter: <strong>{currentLetter}</strong></p>
          <p className="progress">Progress: {letterIndex + 1} / {LETTER_LIST.length}</p>
        </div>
        <DrawingCanvas ref={canvasRef} onSave={handleDrawingSave} />
      </div>
      
      <div className="actions">
        <button 
          onClick={generateTestDataset} 
          className="test-button"
          disabled={isLoading}
        >
          {isLoading ? 'Processing...' : 'Generate Test Dataset'}
        </button>
      </div>
      
      <div className="text-input">
        <h2>Render Text</h2>
        <textarea 
          value={text} 
          onChange={e => setText(e.target.value)}
          placeholder="Enter text to render in handwriting..."
          rows={4}
        />
        <div className="text-actions">
          <button 
            onClick={handleRender} 
            className="render-button"
            disabled={isLoading}
          >
            {isLoading ? 'Rendering...' : 'Render Handwriting'}
          </button>
          <button 
            onClick={copyToClipboard} 
            className="copy-button"
            disabled={isLoading || !renderedHtml}
          >
            Copy to Clipboard
          </button>
        </div>
      </div>
      
      <div id="rendered-output" className="rendered-output" />
      {message && <p className="message">{message}</p>}
    </div>
  );
}

export default App;