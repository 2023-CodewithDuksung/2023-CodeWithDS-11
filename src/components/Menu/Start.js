import React, { useState } from "react";
import "./Start.css";

function Start() {
  const [isTimerRunning, setIsTimerRunning] = useState(false);
  const [startTime, setStartTime] = useState(0);
  const [endTime, setEndTime] = useState(0);

  const handleStartClick = () => {
    setIsTimerRunning(true);
    setStartTime(Date.now());
  };

  const handleEndClick = () => {
    if (isTimerRunning) {
      setEndTime(Date.now());
      setIsTimerRunning(false);

      for (let i = 0; i < 100000000; i++) {
        // j += i;
      }

      const parsedStartTime = parseInt(startTime, 10);
      const parsedEndTime = parseInt(endTime, 10);

      const elapsedMilliseconds = parsedStartTime - parsedEndTime;
      const elapsedMinutes = (elapsedMilliseconds / (1000 * 60)) % 60;

      console.log(typeof parsedStartTime);
      console.log("Elapsed Time:", elapsedMinutes.toFixed(2), "minutes");
    }
  };

  return (
    <div className="center-container">
      <button id="btn-start" onClick={handleStartClick}>
        운동 시작
      </button>
      <button id="btn-end" onClick={handleEndClick}>
        운동 끝
      </button>
    </div>
  );
}

export default Start;
