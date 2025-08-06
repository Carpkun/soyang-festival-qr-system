import React from 'react';
import QRCode from 'react-qr-code';
import '../styles/QRCodeGenerator.css';

interface QRCodeGeneratorProps {
  boothId: number;
  boothName: string;
}

const QRCodeGenerator: React.FC<QRCodeGeneratorProps> = ({ boothId, boothName }) => {
  const qrData = `https://ccculture.pythonanywhere.com/?boothId=${boothId}`; // Generate QR code URL

  return (
    <div className="qr-generator">
      <div className="qr-info">
        <h4>{boothName}</h4>
        <p>부스 ID: {boothId}</p>
      </div>
      <div className="qr-code-container">
        <div className="qr-code-wrapper">
          <QRCode value={qrData} size={150} level="H" />
        </div>
        <div className="qr-data-info">
          <p><strong>QR 데이터:</strong> {qrData}</p>
        </div>
      </div>
    </div>
  );
};

export default QRCodeGenerator;

