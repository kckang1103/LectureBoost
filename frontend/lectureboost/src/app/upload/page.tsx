'use client'

import React, { useState, useCallback } from 'react';
import { Gauge, Upload, X, FileVideo, AlertCircle } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import Link from 'next/link'


interface FileWithPreview extends File {
  preview?: string;
}

const UploadPage = () => {
  const [isDragging, setIsDragging] = useState(false);
  const [file, setFile] = useState<FileWithPreview | null>(null);
  const [fileURL, setFileURL] = useState<string | null>(null);
  const [error, setError] = useState<string>('');

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDragIn = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragOut = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const validateFile = (file: File): boolean => {
    if (!file.type.startsWith('video/')) {
      setError('Please upload a video file');
      return false;
    }
    if (file.size > 500 * 1024 * 1024) { // 500MB limit
      setError('File size must be less than 500MB');
      return false;
    }
    return true;
  };

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    setError('');

    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && validateFile(droppedFile)) {
      const fileURL = URL.createObjectURL(droppedFile);
      setFileURL(fileURL);
      setFile(droppedFile)
    }
  }, []);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    setError('');
    const selectedFile = e.target.files?.[0];
    if (selectedFile && validateFile(selectedFile)) {
      const fileURL = URL.createObjectURL(selectedFile);
      setFileURL(fileURL);
      setFile(selectedFile)
    }
  };

  const removeFile = () => {
    setFile(null);
    setError('');
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 via-indigo-50 to-purple-50 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="w-12 h-12 rounded-full bg-purple-600 flex items-center justify-center">
              <Gauge className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-purple-800 bg-clip-text text-transparent">
              LECTUREBOOST
            </h1>
          </div>
          <p className="text-xl text-gray-700">Upload your lecture video to get started</p>
        </div>

        {/* Upload Area */}
        <Card className="p-8">
          <div
            className={`border-2 border-dashed rounded-lg p-8 transition-colors ${
              isDragging 
                ? 'border-purple-600 bg-purple-50' 
                : 'border-gray-300 hover:border-purple-400'
            }`}
            onDragEnter={handleDragIn}
            onDragLeave={handleDragOut}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            {!file ? (
              <div className="text-center">
                <Upload className="w-12 h-12 text-purple-600 mx-auto mb-4" />
                <p className="text-lg mb-2">
                  Drag and drop your video file here
                </p>
                <p className="text-gray-500 mb-4">
                  or
                </p>
                <label className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors cursor-pointer">
                  Browse Files
                  <input
                    type="file"
                    className="hidden"
                    accept="video/*"
                    onChange={handleFileSelect}
                  />
                </label>
                <p className="text-sm text-gray-500 mt-4">
                  Supported formats: MP4, AVI, MOV (max 500MB)
                </p>
              </div>
            ) : (
              <div className="flex items-center justify-between p-4 bg-purple-50 rounded-lg">
                <div className="flex items-center gap-4">
                  <FileVideo className="w-8 h-8 text-purple-600" />
                  <div>
                    <p className="font-medium">{file.name}</p>
                    <p className="text-sm text-gray-500">
                      {(file.size / (1024 * 1024)).toFixed(2)} MB
                    </p>
                  </div>
                </div>
                <button
                  onClick={removeFile}
                  className="p-2 hover:bg-purple-100 rounded-full transition-colors"
                >
                  <X className="w-5 h-5 text-gray-500" />
                </button>
              </div>
            )}
          </div>

          {error && (
            <Alert variant="destructive" className="mt-4">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <div className="mt-6">
            {/* <button
              disabled={!file}
              className={`w-full py-3 rounded-lg transition-colors font-medium ${
                file
                  ? 'bg-purple-600 text-white hover:bg-purple-700'
                  : 'bg-gray-200 text-gray-500 cursor-not-allowed'
              }`}
            >
              Continue
            </button> */}
            <Link 
              // aria-disabled={!!file} 
              // tabIndex={!file ? -1 : undefined}
              href={{
                pathname: 'videoplayer',
                query: {
                  file: fileURL,
                },
              }} 
              style={{
                pointerEvents: !file ? 'none' : 'auto',
              }}
              className={`w-full px-8 py-3 rounded-lg transition-colors font-medium items-center ${
                file
                  ? 'bg-purple-600 text-white hover:bg-purple-700'
                  : 'bg-gray-200 text-gray-500 cursor-not-allowed'
              }`}
            >
              Continue
            </Link>
          </div>
        </Card>

        {/* Instructions */}
        <div className="mt-8 text-center text-gray-600">
          <p>Your video will be processed securely and privately.</p>
          <p>The processing time depends on the video length and selected options.</p>
        </div>
      </div>
    </div>
  );
};

export default UploadPage;