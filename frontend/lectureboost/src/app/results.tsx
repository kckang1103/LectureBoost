'use client'

import React, { useState } from 'react';
import { Gauge, Download, Printer, MoreVertical } from 'lucide-react';
import { Card } from '@/components/ui/card';

const ResultsPage = () => {
  const [activeSlide, setActiveSlide] = useState(1);
  const totalSlides = 9;

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 via-indigo-50 to-purple-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="w-12 h-12 rounded-full bg-purple-600 flex items-center justify-center">
              <Gauge className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-purple-800 bg-clip-text text-transparent">
              LECTUREBOOST
            </h1>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-6">
          {/* Left Column */}
          <div className="space-y-6">
            {/* Original Video */}
            <Card className="overflow-hidden">
              <div className="bg-black aspect-video">
                <img 
                  src="/api/placeholder/640/360" 
                  alt="Video preview"
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="p-4 flex items-center justify-between bg-gray-900 text-white">
                <span>0:00 / 7:33</span>
                <div className="flex items-center gap-4">
                  <button className="hover:text-purple-300">
                    <Download className="w-5 h-5" />
                  </button>
                  <button className="hover:text-purple-300">
                    <MoreVertical className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </Card>

            {/* Transcription */}
            <Card className="overflow-hidden">
              <div className="p-4 bg-gray-900 text-white flex justify-between items-center">
                <h2 className="font-medium">Transcription</h2>
                <div className="flex gap-2">
                  <button className="hover:text-purple-300">
                    <Download className="w-5 h-5" />
                  </button>
                  <button className="hover:text-purple-300">
                    <Printer className="w-5 h-5" />
                  </button>
                </div>
              </div>
              <div className="p-4 max-h-[300px] overflow-y-auto space-y-4 text-sm">
                <div className="space-y-1">
                  <div className="text-gray-500">Time Stamp: 0:00:00-0:00:30</div>
                  <p>Okay let's get started good morning okay I'll try that again good morning okay welcome to 161 on your instructor dr. Joseph chenta fixing to do here just go through some basic course policies and let you know what does structure of the course is and then we'll do a little bit of review of calculus to finish out the day building room 848</p>
                </div>
                <div className="space-y-1">
                  <div className="text-gray-500">Time Stamp: 0:00:30-0:01:00</div>
                  <p>in the balcony 2L please find a seat in. I'll go back to hear my email change Aki purdue.edu my office hours are Tuesday Thursday 10:30 to 12:30 or if you need to see me but you can't make it to those hours send me an email I'll do my best to arrange a meeting with you have a quote page it's at math. Purdue.edu / ma161 reposting Gordon court documents and any updates and any announcement that always usually go in there and where to send out you know but now it's meant for you</p>
                </div>
              </div>
            </Card>
          </div>

          {/* Right Column - Slides */}
          <Card className="overflow-hidden">
            <div className="bg-gray-900 p-4 flex items-center justify-between text-white">
              <div className="flex items-center gap-4">
                <span>slides</span>
                <span>{activeSlide} / {totalSlides}</span>
              </div>
              <div className="flex items-center gap-4">
                <button className="hover:text-purple-300">60%</button>
                <button className="hover:text-purple-300">
                  <Download className="w-5 h-5" />
                </button>
                <button className="hover:text-purple-300">
                  <Printer className="w-5 h-5" />
                </button>
                <button className="hover:text-purple-300">
                  <MoreVertical className="w-5 h-5" />
                </button>
              </div>
            </div>
            <div className="bg-black p-4">
              <div className="bg-white p-6 min-h-[600px]">
                <h2 className="text-2xl text-yellow-500 mb-6">MA 16100 Spring 2022</h2>
                <ul className="space-y-4 text-lg">
                  <li className="text-yellow-500">Welcome!</li>
                  <li>Instructor: Dr. Joseph Chen</li>
                  <li>Office: Mathematical Sciences Building (MATH) Room 848</li>
                  <li>Email: <a href="#" className="text-blue-600">chenjk@purdue.edu</a></li>
                  <li>Office Hours:
                    <ul className="ml-6 mt-2">
                      <li className="text-red-600">Tue & Thu 10:30-12:30</li>
                      <li>or by email appointments</li>
                    </ul>
                  </li>
                  <li>Course web page:
                    <div className="ml-6 mt-2">
                      <a href="#" className="text-blue-600">http://www.math.purdue.edu/ma161</a>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default ResultsPage;