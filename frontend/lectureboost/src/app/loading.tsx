'use client'

import React, { useState, useEffect } from 'react';
import { Gauge, Check, Clock, Subtitles, FileText, Images, Mail } from 'lucide-react';
import { Card } from '@/components/ui/card';


interface Task {
  id: string;
  name: string;
  icon: React.ElementType;
  progress: number;
  status: 'pending' | 'processing' | 'completed';
}

const LoadingPage = () => {
  const [tasks, setTasks] = useState<Task[]>([
    { id: 'silence', name: 'Removing Silence', icon: Clock, progress: 0, status: 'pending' },
    { id: 'subtitles', name: 'Adding Subtitles', icon: Subtitles, progress: 0, status: 'pending' },
    { id: 'transcript', name: 'Generating Transcription', icon: FileText, progress: 0, status: 'pending' },
    { id: 'slideshow', name: 'Creating Slideshow', icon: Images, progress: 0, status: 'pending' },
    { id: 'email', name: 'Preparing Email Links', icon: Mail, progress: 0, status: 'pending' },
  ]);

  // Simulate progress for demo purposes
  useEffect(() => {
    const intervals = tasks.map((task, index) => {
      return setTimeout(() => {
        const progressInterval = setInterval(() => {
          setTasks(prevTasks => {
            const newTasks = [...prevTasks];
            const taskIndex = newTasks.findIndex(t => t.id === task.id);
            
            if (newTasks[taskIndex].progress < 100) {
              newTasks[taskIndex] = {
                ...newTasks[taskIndex],
                status: 'processing',
                progress: Math.min(newTasks[taskIndex].progress + 2, 100)
              };
              
              if (newTasks[taskIndex].progress === 100) {
                newTasks[taskIndex].status = 'completed';
              }
            }
            
            return newTasks;
          });
        }, 100);

        return () => clearInterval(progressInterval);
      }, index * 2000);
    });

    return () => intervals.forEach(clearTimeout);
  }, []);

  const calculateOverallProgress = () => {
    const totalProgress = tasks.reduce((sum, task) => sum + task.progress, 0);
    return Math.round(totalProgress / tasks.length);
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 via-indigo-50 to-purple-50 p-8">
      <div className="max-w-2xl mx-auto">
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
          <p className="text-xl text-gray-700 mb-2">Processing your video</p>
          <p className="text-gray-600">This may take a few minutes</p>
        </div>

        {/* Overall Progress */}
        <Card className="mb-8 p-6">
          <div className="text-center mb-4">
            <div className="text-4xl font-bold text-purple-600 mb-2">
              {calculateOverallProgress()}%
            </div>
            <div className="text-gray-600">Overall Progress</div>
          </div>
          <div className="w-full bg-gray-100 rounded-full h-4 mb-4">
            <div 
              className="bg-purple-600 h-4 rounded-full transition-all duration-500"
              style={{ width: `${calculateOverallProgress()}%` }}
            />
          </div>
        </Card>

        {/* Individual Tasks */}
        <div className="space-y-4">
          {tasks.map((task) => (
            <Card key={task.id} className="p-4">
              <div className="flex items-center gap-4 mb-3">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center 
                  ${task.status === 'completed' 
                    ? 'bg-green-100' 
                    : task.status === 'processing'
                    ? 'bg-purple-100'
                    : 'bg-gray-100'
                  }`}>
                  {task.status === 'completed' ? (
                    <Check className="w-4 h-4 text-green-600" />
                  ) : (
                    <task.icon className={`w-4 h-4 
                      ${task.status === 'processing' ? 'text-purple-600' : 'text-gray-400'}`} 
                    />
                  )}
                </div>
                <div className="flex-1">
                  <div className="flex justify-between items-center mb-1">
                    <span className={`font-medium 
                      ${task.status === 'completed' 
                        ? 'text-green-600' 
                        : task.status === 'processing'
                        ? 'text-purple-600'
                        : 'text-gray-400'
                      }`}>
                      {task.name}
                    </span>
                    <span className="text-sm text-gray-500">{task.progress}%</span>
                  </div>
                  <div className="w-full bg-gray-100 rounded-full h-2">
                    <div 
                      className={`h-2 rounded-full transition-all duration-500
                        ${task.status === 'completed' 
                          ? 'bg-green-500' 
                          : 'bg-purple-600'
                        }`}
                      style={{ width: `${task.progress}%` }}
                    />
                  </div>
                </div>
              </div>
            </Card>
          ))}
        </div>

        <div className="text-center mt-8 text-sm text-gray-500">
          You'll be automatically redirected when processing is complete
        </div>
      </div>
    </div>
  );
};

export default LoadingPage;