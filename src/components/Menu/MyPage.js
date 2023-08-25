import axios from "axios";

import React, { useState, useEffect } from "react";
import Form from "react-bootstrap/Form";
import "./MyPage.css";

function MyPage() {
  const [user, setUser] = useState({
    fullName: "John Doe",
    email: "johndoe",
  });

  const [userData, setUserData] = useState({
    fullName: "",
    email: "",
    height: "",
    weight: "",
    calorie: "",
  });
  useEffect(() => {
    // 로그인한 유저 정보를 받아와 userData 업데이트
    setUserData((prevUserData) => ({
      ...prevUserData,
      fullName: user.fullName,
      email: user.email,
    }));

    // 기타 유저 정보 업데이트 로직 추가
  }, [user]);

  const [intData, setIntData] = useState(null);

  useEffect(() => {
    getDataFromServer();
  }, []);

  const getDataFromServer = async () => {
    try {
      const response = await axios.get(
        "https://ece5-203-252-223-253.ngrok.io/machine/1"
      );
      const intResult = response.data; // 서버에서 받아온 int값
      setIntData(intResult); // 상태 업데이트
      console.log("Received int value:", intResult); // 콘솔창에 출력
      console.log("버튼 눌림");
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <Form className="mypage-form">
      <Form.Group>
        <Form.Label htmlFor="inputName">Full Name</Form.Label>
        <Form.Control
          type="text"
          id="input"
          placeholder="John Doe"
          value={userData.fullName}
          readOnly
        />
        <Form.Label htmlFor="inputEmail">Email</Form.Label>
        <div className="email-input">
          <Form.Control
            type="email"
            id="input"
            value={userData.email}
            readOnly
          />
          <span>@duksung.ac.kr</span>
        </div>
        <Form.Label htmlFor="input">오늘 운동 시간</Form.Label>
        <p className="smallbox-description">
          {intData !== null ? intData + "시간" : "오늘 운동 시간"}
        </p>{" "}
        <Form.Label htmlFor="input">누적 운동시간</Form.Label>
        <p className="smallbox-description">
          {intData !== null ? intData + "시간" : "누적 운동 시간"}
        </p>
      </Form.Group>
    </Form>
  );
}

export default MyPage;
