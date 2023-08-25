import React, { useState, useEffect } from "react";
import "./Ranking.css";

import axios from "axios";

function Ranking() {
  const [intData, setIntData] = useState(null);
  const [intData2, setIntData2] = useState(null);
  const [intData3, setIntData3] = useState(null);
  const [intData4, setIntData4] = useState(null);
  const [intData5, setIntData5] = useState(null);
  const [intData6, setIntData6] = useState(null);

  useEffect(() => {
    getDataFromServer();
    getDataFromServer2();
    getDataFromServer3();
    getDataFromServer4();
    getDataFromServer5();
    getDataFromServer6();
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

  const getDataFromServer2 = async () => {
    try {
      const response = await axios.get(
        "https://ece5-203-252-223-253.ngrok.io/machine/2"
      );
      const intResult2 = response.data; // 서버에서 받아온 int값
      setIntData(intResult2); // 상태 업데이트
      console.log("Received int value:", intResult2); // 콘솔창에 출력
      console.log("버튼 눌림");
    } catch (error) {
      console.error(error);
    }
  };

  const getDataFromServer3 = async () => {
    try {
      const response = await axios.get(
        "https://ece5-203-252-223-253.ngrok.io/machine/3"
      );
      const intResult3 = response.data; // 서버에서 받아온 int값
      setIntData(intResult3); // 상태 업데이트
      console.log("Received int value:", intResult3); // 콘솔창에 출력
      console.log("버튼 눌림");
    } catch (error) {
      console.error(error);
    }
  };

  const getDataFromServer4 = async () => {
    try {
      const response = await axios.get(
        "https://ece5-203-252-223-253.ngrok.io/mypage/rank"
      );
      const intResult4 = response.data; // 서버에서 받아온 int값
      setIntData(intResult4); // 상태 업데이트
      console.log("Received int value:", intResult4); // 콘솔창에 출력
      console.log("버튼 눌림");
    } catch (error) {
      console.error(error);
    }
  };

  const getDataFromServer5 = async () => {
    try {
      const response = await axios.get(
        "https://ece5-203-252-223-253.ngrok.io/machine/5"
      );
      const intResult5 = response.data; // 서버에서 받아온 int값
      setIntData(intResult5); // 상태 업데이트
      console.log("Received int value:", intResult5); // 콘솔창에 출력
      console.log("버튼 눌림");
    } catch (error) {
      console.error(error);
    }
  };

  const getDataFromServer6 = async () => {
    try {
      const response = await axios.get(
        "https://ece5-203-252-223-253.ngrok.io/machine/6"
      );
      const intResult6 = response.data; // 서버에서 받아온 int값
      setIntData(intResult6); // 상태 업데이트
      console.log("Received int value:", intResult6); // 콘솔창에 출력
      console.log("버튼 눌림");
    } catch (error) {
      console.error(error);
    }
  };
  return (
    <div className="Lank">
      <section className="lanking-page">
        <h1 className="title">랭킹</h1>
        <div className="lanking-description">
          <div className="lankbox first-box">
            <div>
              <div className="crop">
                <img className="image" src="/img/1.jpg" alt="1" />
              </div>
              <div className="lank-smallbox">
                <p className="lank-smallbox-line">사이클</p>
              </div>
            </div>
            <div className="ranking">
              <div className="ranking1">
                {" "}
                {intData !== null ? intData + "등" : "남은 기구"}
              </div>
            </div>
          </div>

          <div className="lankbox first-box">
            <div>
              <div className="crop">
                <img className="image" src="/img/2.jpg" alt="2" />
              </div>
              <div className="lank-smallbox">
                <p className="lank-smallbox-line">스탭퍼</p>
              </div>
            </div>
            <div className="ranking">
              <div className="ranking1">0등</div>
            </div>
          </div>

          <div className="lankbox first-box">
            <div>
              <div className="crop">
                <img className="image" src="/img/3.jpg" alt="3" />
              </div>
              <div className="lank-smallbox">
                <p className="lank-smallbox-line">웨이트머신</p>
              </div>
            </div>
            <div className="ranking">
              <div className="ranking1">0등</div>
            </div>
          </div>
          <div className="lankbox first-box">
            <div>
              <div className="crop">
                <img className="image" src="/img/4.jpg" alt="4" />
              </div>
              <div className="lank-smallbox">
                <p className="lank-smallbox-line">트레드밀</p>
              </div>
            </div>
            <div className="ranking">
              <div className="ranking1">0등</div>
            </div>
          </div>
          <div className="lankbox first-box">
            <div>
              <div className="crop">
                <img className="image" src="/img/5.jpeg" alt="5" />
              </div>
              <div className="lank-smallbox">
                <p className="lank-smallbox-line">레그프레스</p>
              </div>
            </div>
            <div className="ranking">
              <div className="ranking1">0등</div>
            </div>
          </div>
          <div className="lankbox first-box">
            <div>
              <div className="crop">
                <img className="image" src="/img/6.jpeg" alt="6" />
              </div>
              <div className="lank-smallbox">
                <p className="lank-smallbox-line">어시스트 풀업</p>
              </div>
            </div>
            <div className="ranking">
              <div className="ranking1">0등</div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Ranking;
