import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // You can add custom styles here
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { BackgroundBeams } from "@/components/ui/background-beams";
import ColourfulText from "@/components/ui/colourful-text";
import { motion } from "motion/react";



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
    <div className="relative flex flex-col items-center min-h-screen gap-10 bg-[#101010] antialiased">
      <a target="_blank" href="https://electronix.ai/" className='z-10 hover:cursor-pointer'>
        <div className='flex items-center gap-1 text-2xl text-white mb-[180px] border-1 border-white rounded-2xl bg-black p-5 mt-2 hover:cursor-pointer'>
          <img src="https://electronix.ai/assets/e-logo.png" alt="" className='w-10 h-10' />
          electronix.ai
        </div>
      </a>
      

      {/* Background with lowest z-index */}
      <div className="absolute inset-0 z-0">
        <BackgroundBeams />
      </div>

      {/* Foreground content above background */}
      <div className="z-10 flex flex-col items-center gap-10">
        <h1 className="text-4xl font-extrabold text-white md:text-5xl"><ColourfulText text="Sentiment Analysis" /></h1>

        <div className="grid w-xs gap-6 text-white md:w-md">
          <Textarea 
            placeholder="Enter text for sentiment analysis..." 
            value={text} 
            onChange={(e) => setText(e.target.value)} 
            className="h-25"
          />
          
          <Button 
            onClick={handlePredict} 
            disabled={isLoading} 
            className="bg-white text-black hover:text-white cursor-pointer"
          >
            {isLoading ? 'Analyzing...' : 'Predict'}
          </Button>
        </div>

        {error && <p className="text-red-600">{error}</p>}

        {prediction && (
          <div className="text-white">
            <p><strong>Label:</strong> <span className={prediction.label === 'positive' ? 'text-green-500' : 'text-red-500'}>{prediction.label}</span></p>
            <p className='text-blue-500'><strong className='text-white'>Score:</strong> {prediction.score.toFixed(4)}</p>
          </div>
        )}
      </div>
    </div>

  );
}

export default App;