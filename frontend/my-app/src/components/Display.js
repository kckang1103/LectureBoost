import React from "react";
import ReactPlayer from 'react-player';
import { useLocation } from 'react-router-dom';
import Logo from "./Logo";

export default function Display(props) {
    const { state } = useLocation();

    return (
        <div>
            <Logo />
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
                        <object width="100%" height="99%" data={state.slides_link} type="application/pdf">Slides</object>
                    </div>
                </div>}
            {state.transcribe &&
                <div>
                    <object data={state.transcript_link} width="100%" height="200">Transcript</object>
                </div>
            }
        </div>
    )
}