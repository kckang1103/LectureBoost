import * as React from 'react';
import { useNavigate } from "react-router-dom";
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import FormLabel from '@mui/material/FormLabel';
import FormControl from '@mui/material/FormControl';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormHelperText from '@mui/material/FormHelperText';
import Grid from '@mui/material/Grid'; // Grid version 1
import Slider from '@mui/material/Slider';
import Checkbox from '@mui/material/Checkbox';
import TextField from '@mui/material/TextField';
import axios from "axios"
import { LinearProgress } from '@mui/material';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';

const Alert = React.forwardRef(function Alert(props, ref) {
  return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

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

  const [loading, setLoading] = React.useState(false)

  const [open, setOpen] = React.useState(false) // snackbar for error message

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
    setLoading(true);

    try {
      var emailToSend = email;
      console.log(email)
      if (email.localeCompare("") === 0) {
        emailToSend = "fake"
      }
      const { data } = await axios.post(process.env.REACT_APP_BACKEND_ENDPOINT + `file/${whitespace}/${whitespace_val}/${subtitles}/${transcribe}/${slides}/${send_email}/${emailToSend}`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        }
      });

      console.log(data.slides);
      console.log(data.transcript);
      console.log(data.video);

      setLoading(false);

      // Switch to Display page and send all response links and variables
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
      // show error message when error is caught
      setOpen(true);
    }
  };

  const handleSlider = (event, value) => {
    setState({ ...state, whitespace_val: value });
  };

  const handleEmailChange = (event) => {
    setState({ ...state, email: event.target.value });
  }

  const { whitespace, whitespace_val, subtitles, transcribe, slides, send_email, email } = state;

  return (
    <>
      {!loading && <><Box sx={{ display: 'flex', width: '100%', justifyContent: 'flex-start' }}>
        <FormControl
          required
          component="fieldset"
          sx={{ m: 3 }}
          variant="standard"
        >
          <FormLabel component="legend" sx={{ color: "black" }} >Choose your options</FormLabel>
          <FormGroup>
            <FormControlLabel
              control={
                <Checkbox checked={whitespace} onChange={handleChange} name="whitespace" />
              }
              label="Remove Silence"
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
          <FormHelperText>We highly suggest you select email as well</FormHelperText>
          <Button variant="contained" onClick={submit} sx={{ marginTop: '5%' }} >Submit</Button>
        </FormControl>
      </Box>
      </>}
      {loading && <><Grid spacing={1} container>
        <Grid xs item>
          <LinearProgress title="hey what's up" />
        </Grid>
      </Grid><h4 style={{ textAlign: "center" }}>Your lecture video is currently being processed.<br />If you have selected the email notification option, you will receive an email with the contents when the processing is complete.</h4></>}
      <Snackbar
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
        autoHideDuration={5000}
        severity="error"
        open={open}
      ><Alert severity="error">An error occurred while processing. Please try again.</Alert></Snackbar>
    </>
  );
}