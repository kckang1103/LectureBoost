import React from "react";
import { useNavigate } from 'react-router-dom';
import logo from "../assets/logo.png";


export default function Logo() {
  const navigate = useNavigate();
  return (
  <center>
    <img onClick={() => {
      navigate("/");
      window.location.reload();
    }} src={logo} alt="logo" height="100%" width="500" class="logo"/>
  </center>);
}