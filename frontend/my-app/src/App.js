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
      <h1>Upload Video</h1>
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