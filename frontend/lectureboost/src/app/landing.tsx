'use client'

import React from 'react';
import { Gauge, Upload, Clock, Sparkles, ArrowRight } from 'lucide-react';
import { Card } from '@/components/ui/card';
import Link from 'next/link'

const LandingPage = () => {

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 via-indigo-50 to-purple-50">
      {/* Navigation */}
      <nav className="p-6">
        <div className="max-w-6xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-purple-600 flex items-center justify-center">
              <Gauge className="w-5 h-5 text-white" />
            </div>
            <span className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-purple-800 bg-clip-text text-transparent">
              LECTUREBOOST
            </span>
          </div>
          <button className="px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors">
            Get Started
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="px-8 py-16">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h1 className="text-6xl font-bold mb-6 bg-gradient-to-r from-purple-600 to-purple-800 bg-clip-text text-transparent">
              Enhance Your Lecture Videos
            </h1>
            <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
              Transform lengthy lectures into engaging, accessible content with AI-powered processing.
              Save time and boost learning effectiveness.
            </p>
            <Link href="/upload" passHref={true} className="px-8 py-4 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors text-lg font-medium inline-flex items-center gap-2">
              Start Processing <ArrowRight className="w-5 h-5" />
            </Link>
          </div>

          {/* Features */}
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: Clock,
                title: "Remove Silence",
                description: "Automatically detect and remove silent periods to create concise, engaging content."
              },
              {
                icon: Sparkles,
                title: "Generate Slideshows",
                description: "Extract key frames and create a synchronized slideshow from your lecture video."
              },
              {
                icon: Upload,
                title: "Easy Sharing",
                description: "Get instant access to your processed content with shareable links and downloads."
              }
            ].map((feature, index) => (
              <Card key={index} className="p-6 hover:shadow-lg transition-shadow">
                <div className="w-12 h-12 rounded-full bg-purple-100 flex items-center justify-center mb-4">
                  <feature.icon className="w-6 h-6 text-purple-600" />
                </div>
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </Card>
            ))}
          </div>

          {/* Statistics */}
          <div className="mt-16 text-center">
            <div className="grid md:grid-cols-3 gap-8">
              {[
                { value: "500+", label: "Videos Processed" },
                { value: "1,000+", label: "Hours Saved" },
                { value: "98%", label: "Satisfaction Rate" }
              ].map((stat, index) => (
                <div key={index} className="p-6">
                  <div className="text-4xl font-bold text-purple-600 mb-2">{stat.value}</div>
                  <div className="text-gray-600">{stat.label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default LandingPage;