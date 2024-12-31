import React, { useState } from 'react';
import DrawingCanvas from './components/DrawingCanvas';
import './App.css';

const LETTER_LIST = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

function App() {
  const [text, setText] = useState('');
  const [message, setMessage] = useState('');
  
  const generateTestDataset = async () => {
    try {
      const response = await fetch('/api/generate-test-dataset', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ letterlist: LETTER_LIST })
      });
      
      const data = await response.json();
      setMessage(data.success ? `${data.message}. Try rendering some text!` : data.error);
    } catch (error) {
      setMessage('Error: ' + error.message);
    }
  };

  const handleRender = async () => {
    if (!text.trim()) {
      setMessage('Please enter some text to render');
      return;
    }
    
    try {
      const response = await fetch('/api/render', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      });
      
      const data = await response.json();
      if (data.success) {
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
          
          setMessage('Handwriting rendered successfully');
        }
      } else {
        setMessage(data.error || 'Error rendering handwriting');
      }
    } catch (error) {
      setMessage('Error: ' + error.message);
    }
  };

  return (
    <div className="app">
      <h1>Handwriting Generator</h1>
      <div className="actions">
        <button onClick={generateTestDataset} className="test-button">
          Generate Test Dataset
        </button>
      </div>
      <div className="text-input">
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
        </div>
      </div>
      <div id="rendered-output" className="rendered-output" />
      {message && <p className="message">{message}</p>}
    </div>
  );
}

export default App;