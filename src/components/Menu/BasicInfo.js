import React from "react";
import "./BasicInfo.css";

function BasicInfo() {
  return (
    <div className="basic-info">
      <h2 className="place-title1">Location</h2>
      <p className="place-title">라온센터 위치</p>
      <p className="place-num">덕성 하나 누리관 라온센터 2층</p>

      <h2 className="section-title1">Laon Center Time Table</h2>
      <p className="sub-title">라온센터 이용시간</p>
      <table className="info-table">
        <thead>
          <tr>
            <th>요일</th>
            <th>이용시간</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>주중 4일</td>
            <td>
              9:00 ~ 20:00 <br />
              교양수업 관계로 매 학기 휴관되는 요일 변동
            </td>
          </tr>
          <tr>
            <td>토, 일요일 및 법정공휴일</td>
            <td>휴무</td>
          </tr>
          <tr>
            <td>방학기간 (월~금)</td>
            <td>9:00 ~ 18:00</td>
          </tr>
        </tbody>
      </table>

      <h2 className="section-title">How to Use Laon Center</h2>
      <p className="sub-title">라온센터 이용규칙</p>
      <div className="rule-list">
        <div className="rule">
          <span className="rule-number">0</span>
          <p className="rule-description">이용방법</p>
          <p className="rule-content">
            학생증 또는 교직원증을 맡기고
            <br /> 탈의실 락커를 이용
          </p>
        </div>
        <div className="rule">
          <span className="rule-number">1</span>
          <p className="rule-description">준비물</p>
          <p className="rule-content">
            교직원증(학생증), 실내용 운동화, 운동복,
            <br /> 수건, 세면도구 등
          </p>
        </div>
        <div className="rule">
          <span className="rule-number">2</span>
          <p className="rule-description">이용복장</p>
          <p className="rule-content">
            반드시 실내 전용 운동화와 운동복을 착용
          </p>
        </div>
      </div>
      <div className="rule-list">
        <div className="rule">
          <span className="rule-number">3</span>
          <p className="rule-description">준비운동</p>
          <p className="rule-content">충분한 준비 운동 후 운동을 시작하기</p>
        </div>
        <div className="rule">
          <span className="rule-number">4</span>
          <p className="rule-description">뒷정리는 필수!</p>
          <p className="rule-content">사용한 운동 기구는 제자리에 놓아두기</p>
        </div>
      </div>
      <h2 className="section-title">Matters for inquiry</h2>
      <p className="sub-title">라온센터 문의사항</p>
      <p className="school-num">901-8599</p>
    </div>
  );
}

export default BasicInfo;
