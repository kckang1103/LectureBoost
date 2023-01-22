import React from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
} from "react-router-dom";
import DragDrop from "./components/DragDrop";
import Display from "./components/Display"
import "./index.css";

function Home() {
  return (
    <div className="App">
      <center><img src="https://lecture-boost.s3.us-east-2.amazonaws.com/Screenshot+2023-01-22+at+4.11.30+AM.png" alt="what image shows" height="100%" width="400" /></center>
      <DragDrop />
    </div>
  );
};

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path='/Display' element={<Display />} />
      </Routes>
    </Router>
  );
}