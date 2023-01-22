import * as React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import FormLabel from '@mui/material/FormLabel';
import FormControl from '@mui/material/FormControl';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormHelperText from '@mui/material/FormHelperText';
import Slider from '@mui/material/Slider';
import Checkbox from '@mui/material/Checkbox';
import axios from "axios"

export default function CheckBoxes(props) {
  const [state, setState] = React.useState({
    whitespace: true,
    whitespace_val: 0.3,
    subtitles: false,
    transcribe: false,
    slides: false,
  });

  const handleChange = (event) => {
    setState({
      ...state,
      [event.target.name]: event.target.checked,
    });
  };
  
  const submit = (event) => {
    let formData = new FormData();
    formData.append("file", props.file);
    axios.post('http://127.0.0.1:8001/file', formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      }
    });

    axios.post(`http://127.0.0.1:8001/methods/${whitespace}/${whitespace_val}/${subtitles}/${transcribe}/${slides}`)
  };

  const handleSlider = (event, value) => {
    setState({...state, whitespace_val: value})
  };

  const { whitespace, whitespace_val, subtitles, transcribe, slides } = state;

  return (
    <>
      <Box sx={{ display: 'flex', width: 1000 }}>
        <FormControl
          required
          component="fieldset"
          sx={{ m: 3 }}
          variant="standard"
        >
          <FormLabel component="legend">Choose your options</FormLabel>
          <FormGroup>
            <FormControlLabel
              control={
                <Checkbox checked={whitespace} onChange={handleChange} name="whitespace" />
              }
              label="Remove Whitespaces"
            />
            {whitespace && <Slider 
              defaultValue={0.3} 
              aria-label="Default" 
              valueLabelDisplay="auto" 
              step={0.05}
              min={0.3}
              max={1}
              value={state.whitespace_val}
              onChange={handleSlider}
            />}
            <FormControlLabel
              control={
                <Checkbox checked={subtitles} onChange={handleChange} name="subtitles" />
              }
              label="Add Subtitles"
            />
            <FormControlLabel
              control={
                <Checkbox checked={transcribe} onChange={handleChange} name="transcribe" />
              }
              label="Generate Transcription"
            />
            <FormControlLabel
              control={
                <Checkbox checked={slides} onChange={handleChange} name="slides" />
              }
              label="Generate Slideshow"
            />
          </FormGroup>
          <FormHelperText>Choose at least 1</FormHelperText>
        </FormControl>
      </Box>
      <Button variant="contained" onClick={submit}>Submit</Button>
    </>
  );
}