import React from "react";
import { Link } from "react-router-dom";
import "./MainContent.css";

function MainContent() {
  return (
    <div className="main-content">
      <h2 className="lets-move">Let's move!</h2>
      <h2 className="stay-healthy">stay healthy</h2>
      <p className="hope">모든 학우들이 강한 여자가 되길 희망합니다!</p>
      <Link to="./Login/Login" className="sign-in-button">
        Sign In
      </Link>
    </div>
  );
}

export default MainContent;
