'use client'

import React, { Suspense, useState } from 'react';
import { Upload } from 'lucide-react';
import { useSearchParams } from 'next/navigation'


function VideoPlayer() {
  const searchParams = useSearchParams()
  const file = searchParams.get('file')
  
  const [settings, setSettings] = useState({
    generateSummary: false,
    createFlashcards: false,
    highlightKeyPoints: false,
    processingSpeed: 1
  });

  const handleCheckbox = (key: keyof typeof settings) => {
    setSettings(prev => ({
      ...prev,
      [key]: !prev[key]
    }));
  };

  const handleSlider = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSettings(prev => ({
      ...prev,
      processingSpeed: parseFloat(event.target.value)
    }));
  };

  return (
    <Suspense fallback={<div>Loading...</div>}>
      <div className="max-w-6xl mx-auto p-6 space-y-8 bg-gradient-to-b from-blue-50 to-purple-50 min-h-screen">
        <div className="text-center">
          <div className="flex justify-center items-center mb-2">
            <Upload className="w-8 h-8 text-purple-600" />
            <span className="text-3xl font-bold text-purple-600 ml-2">LECTUREBOOST</span>
          </div>
          <h2 className="text-xl text-gray-600">Upload your lecture video to get started</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white rounded-lg shadow-md p-4">
            <div className="aspect-video bg-gray-100 rounded-lg flex items-center justify-center">
              <video
                className="VideoInput_video"
                width={500}
                height={300}
                controls
                src={file ?? undefined}
              /> 
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6 space-y-6">
            <div className="space-y-4">
              <div className="flex items-center space-x-2">
                <input 
                  type="checkbox" 
                  checked={settings.generateSummary}
                  onChange={() => handleCheckbox('generateSummary')}
                  className="w-4 h-4 text-purple-600" 
                />
                <span>Generate Summary</span>
              </div>
              <div className="flex items-center space-x-2">
                <input 
                  type="checkbox" 
                  checked={settings.createFlashcards}
                  onChange={() => handleCheckbox('createFlashcards')}
                  className="w-4 h-4 text-purple-600" 
                />
                <span>Create Flashcards</span>
              </div>
              <div className="flex items-center space-x-2">
                <input 
                  type="checkbox" 
                  checked={settings.highlightKeyPoints}
                  onChange={() => handleCheckbox('highlightKeyPoints')}
                  className="w-4 h-4 text-purple-600" 
                />
                <span>Highlight Key Points</span>
              </div>
            </div>

            <div className="space-y-2">
              <label>Processing Speed: {settings.processingSpeed}x</label>
              <input 
                type="range" 
                min="0.5" 
                max="2" 
                step="0.1" 
                value={settings.processingSpeed}
                onChange={handleSlider}
                className="w-full"
              />
            </div>

            <button className="w-full bg-purple-600 text-white py-2 rounded-md hover:bg-purple-700">
              Continue
            </button>
          </div>
        </div>

        <div className="text-center text-sm text-gray-500 space-y-1">
          <p>Your video will be processed securely and privately.</p>
          <p>The processing time depends on the video length and selected options.</p>
        </div>
      </div>
    </Suspense>
  );
}

const Page = () => {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <VideoPlayer />
    </Suspense>
  );
}

export default Page;