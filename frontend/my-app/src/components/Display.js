import React from "react";
import ReactPlayer from 'react-player';
import { useLocation } from 'react-router-dom';

export default function Display(props) {
    const { state } = useLocation();

    return (
        <div>
            <center><img src="https://lecture-boost.s3.us-east-2.amazonaws.com/Screenshot+2023-01-22+at+4.11.30+AM.png" alt="what image shows" height="100%" width="500" /></center>
            {!state.slides &&
                <div className='player-wrapper'>
                    <ReactPlayer
                        className='react-player fixed-bottom'
                        url={state.video_link}
                        width='100%'
                        height='100%'
                        controls={true}
                    />
                </div>}
            {state.slides &&
                <div class="grid-container">
                    <div class="grid-child purple">
                        <div className='player-wrapper'>
                            <ReactPlayer
                                className='react-player fixed-bottom'
                                url={state.video_link}
                                width='100%'
                                height='100%'
                                controls={true}
                            />
                        </div>
                    </div>

                    <div class="grid-child green">
                        <object width="100%" height="99%" data={state.slides_link} type="application/pdf" />
                    </div>
                </div>}

            <div>
                <object data={state.transcript_link} width="100%" height="200" />
            </div>
        </div>
    )
}