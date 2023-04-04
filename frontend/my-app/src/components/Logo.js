import React from "react";
import { useNavigate } from 'react-router-dom';
import logo from "../assets/logo.png";


export default function Logo() {
  const navigate = useNavigate();
  return (<center><img onClick={() => {
    window.location.reload();
    navigate("/");
  }} src={logo} alt="logo" height="100%" width="500" /></center>);
}