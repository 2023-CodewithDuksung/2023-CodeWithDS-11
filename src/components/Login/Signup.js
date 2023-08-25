import React, { useState } from "react";
import { Link } from "react-router-dom";
import Form from "react-bootstrap/Form";
import axios from "axios";

import "./Signup.css";

function Signup() {
  const fixedEmailPart = "@duksung.ac.kr";
  const [userInput, setUserInput] = useState("");

  const handleUserInputChange = (event) => {
    setUserInput(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const finalEmail = `${userInput}${fixedEmailPart}`;
    console.log("Submitted email:", finalEmail);
  };
  const getDataFromServer = async () => {
    try {
      const response = await axios.post(
        "https://ece5-203-252-223-253.ngrok.io/machine/1"
      );
      const intResult = response.data;
      console.log("Received int value:", intResult);
      console.log("버튼 눌림");
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="login-container">
      <div className="signup-left">
        <img src="/img/images.jpeg" alt="Login" />
      </div>
      <div className="signup-right">
        <h2 className="welcome-title">Welcome to Laon Center</h2>

        <Form onSubmit={handleSubmit} className="signup-form">
          <Form.Group>
            <Form.Label htmlFor="inputName">Full Name</Form.Label>
            <Form.Control type="text" id="input" placeholder="John Doe" />

            <Form.Label htmlFor="inputEmail">Email</Form.Label>
            <div className="email-input">
              <Form.Control
                type="text"
                id="input-email"
                value={userInput}
                onChange={handleUserInputChange}
                placeholder="Enter your email here"
              />
              {fixedEmailPart}

              <button className="code-send">인증코드발송</button>
            </div>
            <Form.Label htmlFor="inputEmail">Email</Form.Label>
            <div className="email-input">
              <Form.Control
                type="email"
                id="input-email2"
                placeholder="Enter your validation code"
              />
              <button type="submit" className="email-confirm">
                인증
              </button>
            </div>

            <Form.Label htmlFor="inputPassword">Password</Form.Label>
            <Form.Control
              type="text"
              id="input"
              placeholder="Enter your Password"
            />
          </Form.Group>
        </Form>
        <button className="signup-button" onClick={getDataFromServer}>
          Create Account
        </button>
        <p className="login-message">
          Already have an account? <Link to="/Login/Login">Log In</Link>
        </p>
      </div>
    </div>
  );
}
export default Signup;
