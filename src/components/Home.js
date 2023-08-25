import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Header from "./Header";
import MainContent from "./Main/MainContent";
import MainImage from "./Main/MainImage";
import BasicInfo from "./Menu/BasicInfo";
import Ranking from "./Menu/Ranking";
import MyPage from "./Menu/MyPage";
import Login from "./Login/Login";
import Signup from "./Login/Signup";
import Status from "./Menu/Status";
import Qrcode from "./Menu/Qrcode";
import Start from "./Menu/Start";

function Home() {
  return (
    <Router>
      <div>
        <Header />
        <Routes>
          <Route path="/" element={<MainContentWithImage />} />
          <Route path="/Menu/BasicInfo" element={<BasicInfo />} />
          <Route path="/Menu/Ranking" element={<Ranking />} />
          <Route path="/Menu/Status" element={<Status />} />
          <Route path="/Menu/MyPage" element={<MyPage />} />
          <Route path="/Menu/Start" element={<Start />} />
          <Route path="/Menu/Qrcode" element={<Qrcode />} />
          <Route path="/Login/Login" element={<Login />} />
          <Route path="/Login/Signup" element={<Signup />} />
        </Routes>
      </div>
    </Router>
  );
}
function MainContentWithImage() {
  return (
    <div>
      <div style={{ display: "flex" }}>
        <MainContent />
        <MainImage />
      </div>
    </div>
  );
}
export default Home;
