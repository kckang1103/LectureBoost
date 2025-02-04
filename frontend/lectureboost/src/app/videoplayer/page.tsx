'use client'

import React, { Suspense, useState } from 'react';
import { Upload } from 'lucide-react';
import { useSearchParams } from 'next/navigation'
import axios from "axios"
import Link from 'next/link'


function VideoPlayer() {
  const searchParams = useSearchParams()
  const file = searchParams.get('file')
  
  const [settings, setSettings] = useState({
    addSubtitles: false,
    sendEmail: false,
    email: '',
    addSlideshow: false,
    silentPeriod: 0.5
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

  async function submit() {
    const formData = new FormData();
    const fetchedFile = await fetch(file ?? '').then(res => res.blob())
    formData.append("file", fetchedFile);
    // setLoading(true);

    try {
      let emailToSend = settings.email;
      console.log(settings.email)
      if (settings.email.localeCompare("") === 0) {
        emailToSend = "fake"
      }
      const { data } = await axios.post(process.env.NEXT_PUBLIC_BACKEND_URL
        + `/file/${true}/${settings.silentPeriod}/${settings.addSubtitles}/${false}/${settings.addSlideshow}/${settings.sendEmail}/${emailToSend}`, 
        formData, 
        {
          headers: {
            "Content-Type": "multipart/form-data",
          }
        }
      );

      console.log(data.slides);
      console.log(data.transcript);
      console.log(data.video);

      // setLoading(false);

      // Switch to Display page and send all response links and variables
      // navigate("/Display", {
      //   state: {
      //     whitespace: whitespace,
      //     whitespace_val: whitespace_val,
      //     transcribe: transcribe,
      //     slides: slides,
      //     subtitles: subtitles,
      //     video_link: data.video,
      //     slides_link: data.slides,
      //     transcript_link: data.transcript,
      //   }
      // });
    } catch (err) {
      console.error(err);
      // show error message when error is caught
      // setOpen(true);
    }
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
                  checked={settings.addSubtitles}
                  onChange={() => handleCheckbox('addSubtitles')}
                  className="w-4 h-4 text-purple-600" 
                />
                <span>Add Subtitles</span>
              </div>
              <div className="flex items-center space-x-2">
                <input 
                  type="checkbox" 
                  checked={settings.sendEmail}
                  onChange={() => handleCheckbox('sendEmail')}
                  className="w-4 h-4 text-purple-600" 
                />
                <span>Email Me</span>
              </div>
              <div className="flex items-center space-x-2">
                <input 
                  type="checkbox" 
                  checked={settings.addSlideshow}
                  onChange={() => handleCheckbox('addSlideshow')}
                  className="w-4 h-4 text-purple-600" 
                />
                <span>Generate Slideshow</span>
              </div>
            </div>

            <div className="space-y-2">
              <label>Minimum Silent Period : {settings.silentPeriod}x</label>
              <input 
                type="range" 
                min="0.1" 
                max="3" 
                step="0.1" 
                value={settings.silentPeriod}
                onChange={handleSlider}
                className="w-full"
              />
            </div>

            {/* <button className="w-full bg-purple-600 text-white py-2 rounded-md hover:bg-purple-700">
              Continue
            </button> */}
            <Link 
              href={{
                pathname: 'loading',
              }} 
              onClick={submit}
              className={'w-full px-8 py-3 rounded-lg transition-colors font-medium items-center bg-purple-600 text-white hover:bg-purple-700$'}
            >
              Continue
            </Link>
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