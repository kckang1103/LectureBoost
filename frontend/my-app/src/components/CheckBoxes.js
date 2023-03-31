import * as React from 'react';
import { useNavigate } from "react-router-dom";
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import FormLabel from '@mui/material/FormLabel';
import FormControl from '@mui/material/FormControl';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormHelperText from '@mui/material/FormHelperText';
import Slider from '@mui/material/Slider';
import Checkbox from '@mui/material/Checkbox';
import TextField from '@mui/material/TextField';
import axios from "axios"
import { LinearProgress } from '@mui/material';


export default function CheckBoxes(props) {
  const [state, setState] = React.useState({
    whitespace: true,
    whitespace_val: 0.3,
    subtitles: false,
    transcribe: false,
    slides: false,
    send_email: false,
    email: "",
  });


  // const [linkState, setLinkState] = React.useState({
  //   video_link: '',
  //   slides_link: '',
  //   transcript_link: '',
  // })

  const [loading, setLoading] = React.useState(false)
  const navigate = useNavigate();


  const handleChange = (event) => {
    setState({
      ...state,
      [event.target.name]: event.target.checked,
    });
  };
  
  async function submit() {
    let formData = new FormData();
    formData.append("file", props.file);
    setLoading(true)
    
    try {
      console.log(email);
      const {data} = await axios.post(`http://127.0.0.1:8080/file/${whitespace}/${whitespace_val}/${subtitles}/${transcribe}/${slides}/${send_email}/${email}`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        }
      });
      
      console.log(data.slides);
      console.log(data.transcript);
      console.log(data.video);

      setLoading(false)

      navigate("/Display", {
        state: {
          whitespace: whitespace,
          whitespace_val: whitespace_val,
          transcribe: transcribe,
          slides: slides,
          subtitles: subtitles,
          video_link: data.video,
          slides_link: data.slides,
          transcript_link: data.transcript,
        }
      });
    } catch (err) {
      console.error(err);
    }
  };

  const handleSlider = (event, value) => {
    setState({...state, whitespace_val: value});
  };

  const handleEmailChange = (event) => {
    setState({...state, email: event.target.value});
  }

  const { whitespace, whitespace_val, subtitles, transcribe, slides, send_email, email } = state;

  return (
    <>
      {!loading && <><Box sx={{ display: 'flex', width: 1000 }}>
        <FormControl
          required
          component="fieldset"
          sx={{ m : 3 }}
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
            <FormControlLabel
              control={
                <Checkbox checked={send_email} onChange={handleChange} name="send_email" />
              }
              label="Email Links"
            />

            {send_email && <TextField
              id="email"
              label="Email"
              value={state.email}
              onChange={handleEmailChange}
              margin="normal"
            />}
          </FormGroup>
          <FormHelperText>Choose at least 1 except for email</FormHelperText>
        </FormControl>
      </Box>
      <Button variant="contained" onClick={submit}>Submit</Button></>}
      {loading && <LinearProgress />}
    </>
  );
}