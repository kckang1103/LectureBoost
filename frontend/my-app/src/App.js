import React from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
} from "react-router-dom";
import Grid from '@mui/material/Grid'; // Grid version 1
import { ThemeProvider, createTheme } from '@mui/material/styles';

import "./index.css";
import Logo from "./components/Logo";
import DragDrop from "./components/DragDrop";
import Display from "./components/Display"
import Statistics from "./components/Statistics";

const theme = createTheme({
  palette: {
    primary: {
      main: "#015b94"
    }
  }
});

function Home() {
  return (
    <ThemeProvider theme={theme}>
      <div className="wave"></div>
      <div className="wave"></div>
      <div className="wave"></div>
      <div className="App">
        <Grid
          container
          direction="column"
          justifyContent="center"
          alignItems="center"
        >
          <Logo />
          <Statistics />
          <DragDrop />
        </Grid>
      </div>
    </ThemeProvider>
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