import React, { useState } from "react";
import { QrReader } from "react-qr-reader";
import "./Qrcode.css";

function Qrcode() {
  const [qrResult, setQrResult] = useState(null);

  const handleScan = (data) => {
    if (data) {
      setQrResult(data);
    }
  };

  const handleError = (err) => {
    console.error(err);
  };

  return (
    <div className="qrcode-container">
      <h2 className="qr-title">QR Code Scanner</h2>
      <div className="qr-scanner">
        <QrReader
          delay={300}
          onError={handleError}
          onScan={handleScan}
          style={{ width: "100%" }}
        />
      </div>
      {qrResult && <p className="qr-result">QR Code Result: {qrResult}</p>}
    </div>
  );
}

export default Qrcode;
