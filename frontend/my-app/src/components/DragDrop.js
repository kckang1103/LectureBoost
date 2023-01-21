import React from "react";
import { AiOutlineCloudUpload } from 'react-icons/ai';
import CheckBoxes from "./CheckBoxes";


export default function DragDrop() {
  const height = 400;
  const width = 500;

  const [dragActive, setDragActive] = React.useState(false);
  const inputRef = React.useRef(null);
  const [source, setSource] = React.useState();


  // handle drag events
  const handleDrag = function (e) {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleFile = function (files) {
    // alert("Number of files: " + files.length);

    const url = URL.createObjectURL(files[0]);
    setSource(url);
    // var video = document.createElement("video");
    // video.controls = true;
    // video.src = window.URL.createObjectURL(file);
    // document.body.appendChild(video);
  }

  // triggers when file is dropped
  const handleDrop = function (e) {
    console.log('handledrop')
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      console.log(e.dataTransfer.files.length)
      handleFile(e.dataTransfer.files);
    }
  };

  // triggers when file is selected with click
  const handleChange = function (e) {
    console.log('handlechange')
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e);
    }
  };

  // triggers the input when the button is clicked
  const onButtonClick = () => {
    inputRef.current.click();
  };

  return (
    <>
      {!source &&
        <form id="form-file-upload" onDragEnter={handleDrag} onSubmit={(e) => e.preventDefault()}>
          <input ref={inputRef} type="file" id="input-file-upload" multiple={true} accept=".mov,.mp4" onChange={handleChange} />
          <label id="label-file-upload" htmlFor="input-file-upload" className={dragActive ? "drag-active" : ""}>
            <div>
              <AiOutlineCloudUpload size={70} />
              <p>Drag and drop your video here or</p>
              <button className="upload-button" onClick={onButtonClick}>Choose a video</button>
            </div>
          </label>
          {dragActive && <div id="drag-file-element" onDragEnter={handleDrag} onDragLeave={handleDrag} onDragOver={handleDrag} onDrop={handleDrop}></div>}
        </form>
      }
      {source && (
        <>
          <CheckBoxes className="CheckBoxes" />
          <video
            className="VideoInput_video"
            width={width}
            height={height}
            controls
            src={source}
          />
        </>
      )}
    </>
  );
};