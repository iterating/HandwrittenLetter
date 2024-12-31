import React, { useState, useRef } from 'react';
import DrawingCanvas from './components/DrawingCanvas';
import { API_BASE_URL, API_ENDPOINTS } from './config/api';
import './App.css';

const LETTER_LIST = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

const storage = {
  saveLetter: (letter, imageData) => {
    try {
      localStorage.setItem(`letter-${letter}`, imageData);
      return true;
    } catch (error) {
      return false;
    }
  },
  getLetter: (letter) => {
    try {
      return localStorage.getItem(`letter-${letter}`);
    } catch (error) {
      return null;
    }
  }
};

function App() {
  const [text, setText] = useState('');
  const [message, setMessage] = useState('');
  const [currentLetter, setCurrentLetter] = useState(LETTER_LIST[0]);
  const [letterIndex, setLetterIndex] = useState(0);
  const [renderedHtml, setRenderedHtml] = useState('');
  const canvasRef = useRef(null);
  const iframeRef = useRef(null);
  
  const generateTestDataset = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.GENERATE_TEST_DATASET}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ letterlist: LETTER_LIST })
      });
      
      const data = await response.json();
      setMessage(data.success ? `${data.message}. Try drawing or rendering some text!` : data.error);
    } catch (error) {
      setMessage('Error: ' + error.message);
    }
  };

  const handleDrawingSave = async (imageData) => {
    try {
        // Save to localStorage first
        const saved = storage.saveLetter(currentLetter, imageData);
        if (!saved) {
            setMessage('Error saving to local storage');
            return;
        }

        // Also save to server if available
        const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.SAVE_LETTER}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ letter: currentLetter, imageData })
        });
        
        const data = await response.json();
        if (data.success) {
            setMessage(`Saved letter ${currentLetter}`);
            
            // Move to next letter
            const nextIndex = letterIndex + 1;
            if (nextIndex < LETTER_LIST.length) {
                setLetterIndex(nextIndex);
                setCurrentLetter(LETTER_LIST[nextIndex]);
            } else {
                setMessage('Completed all letters! Try rendering some text.');
            }
            
            // Clear canvas
            canvasRef.current?.clear();
        } else {
            setMessage(data.error || 'Error saving letter on server');
        }
    } catch (error) {
        // If server save fails, at least we have local storage backup
        setMessage('Saved locally only. Server error: ' + error.message);
    }
  };

  const handleRender = async () => {
    if (!text.trim()) {
        setMessage('Please enter some text to render');
        return;
    }
    
    try {
        // First try to render using locally stored letters
        const letters = text.split('').map(letter => ({
            letter,
            imageData: storage.getLetter(letter)
        }));

        // Check if we have all letters locally
        const missingLetters = letters.filter(l => !l.imageData);
        if (missingLetters.length === 0) {
            // We can render locally
            // Create a canvas to combine the letters
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            canvas.width = letters.length * 100; // Adjust size as needed
            canvas.height = 100;

            // Draw each letter
            let x = 0;
            for (const { imageData } of letters) {
                const img = new Image();
                img.src = imageData;
                await new Promise(resolve => {
                    img.onload = () => {
                        ctx.drawImage(img, x, 0);
                        x += img.width;
                        resolve();
                    };
                });
            }

            // Display the result
            const container = document.getElementById('rendered-output');
            if (container) {
                container.innerHTML = '';
                container.appendChild(canvas);
            }
            setMessage('Rendered using locally stored letters');
            return;
        }

        // If we don't have all letters locally, fall back to server
        const response = await fetch(`${API_BASE_URL}${API_ENDPOINTS.RENDER}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        
        const data = await response.json();
        if (data.success) {
            setRenderedHtml(data.html_content);
            const container = document.getElementById('rendered-output');
            if (container) {
                const iframe = document.createElement('iframe');
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
                
                setMessage('Rendered using server (some letters were not found locally)');
            }
        } else {
            setMessage(data.error || 'Error rendering handwriting');
        }
    } catch (error) {
        setMessage('Error: ' + error.message);
    }
  };

  const copyToClipboard = async () => {
    try {
      if (!renderedHtml) {
        setMessage('Please render some text first');
        return;
      }

      const iframe = iframeRef.current;
      if (iframe) {
        const doc = iframe.contentDocument || iframe.contentWindow.document;
        const content = doc.body.innerHTML;
        await navigator.clipboard.writeText(content);
        setMessage('Copied to clipboard!');
      }
    } catch (error) {
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
        <button onClick={generateTestDataset} className="test-button">
          Generate Test Dataset
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
          <button onClick={handleRender} className="render-button">
            Render Handwriting
          </button>
          <button onClick={copyToClipboard} className="copy-button">
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