import React, { useState } from "react";
import { Link } from "react-router-dom";
import Form from "react-bootstrap/Form";
import "./Login.css";

function Login() {
  const [user, setUser] = useState({
    fullName: "",
    email: "",
    password: "",
  });

  const handleLogin = () => {
    // 로그인 로직 처리
    // ...

    // 유저 정보를 state에 저장
    setUser({
      fullName: "John Doe",
      email: "johndoe",
      password: "yourpassword",
    });
  };
  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setUser((prevUser) => ({
      ...prevUser,
      [name]: value,
    }));
  };

  return (
    <div className="login-container">
      <div className="login-left">
        <img src="/img/images.jpeg" alt="Login" />
      </div>
      <div className="login-right">
        <h2 className="welcome-title">Welcome to Laon Center</h2>

        <Form className="login-form">
          <Form.Group>
            <Form.Label htmlFor="inputName">Full Name</Form.Label>
            <Form.Control
              type="text"
              id="input"
              name="fullName"
              placeholder="John Doe"
              value={user.fullName}
              onChange={handleInputChange}
            />
            <Form.Label htmlFor="inputPassword">Password</Form.Label>
            <Form.Control
              type="password"
              id="input"
              name="password"
              placeholder="Enter your Password"
              value={user.password}
              onChange={handleInputChange}
            />
          </Form.Group>
        </Form>
        <button className="login-button">Log In</button>
        <p className="signup-message">
          If you have no account, <Link to="/Login/Signup">sign up</Link>
        </p>
      </div>
    </div>
  );
}

export default Login;
