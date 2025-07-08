import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // You can add custom styles here

function App() {
  const [text, setText] = useState('');
  const [prediction, setPrediction] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  // The frontend calls the backend and displays the prediction 
  const handlePredict = async () => {
    // Simple validation
    if (!text.trim()) {
      setError('Please enter some text.');
      return;
    }

    setIsLoading(true);
    setError('');
    setPrediction(null);

    try {
      // The backend service will be available at http://localhost:8000
      const response = await axios.post('http://localhost:8000/predict', { text });
      // Display of returned label & score [cite: 28]
      setPrediction(response.data);
    } catch (err) {
      setError('Failed to get prediction. Is the backend running?');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Sentiment Analysis</h1>
      {/* One page with a Textarea + Predict button [cite: 26, 27] */}
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter text for sentiment analysis..."
        rows="4"
      />
      <button onClick={handlePredict} disabled={isLoading}>
        {isLoading ? 'Analyzing...' : 'Predict'}
      </button>

      {error && <p className="error">{error}</p>}

      {prediction && (
        <div className="result">
          <p><strong>Label:</strong> <span className={prediction.label}>{prediction.label}</span></p>
          <p><strong>Score:</strong> {prediction.score.toFixed(4)}</p>
        </div>
      )}
    </div>
  );
}

export default App;