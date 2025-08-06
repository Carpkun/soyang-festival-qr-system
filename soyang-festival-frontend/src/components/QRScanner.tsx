import React, { useRef, useEffect, useState } from 'react';
import { BrowserMultiFormatReader } from '@zxing/library';

interface QRScannerProps {
  onScanSuccess: (data: string) => void;
  onScanError?: (error: string) => void;
}

const QRScanner: React.FC<QRScannerProps> = ({ onScanSuccess, onScanError }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isScanning, setIsScanning] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const codeReader = useRef<BrowserMultiFormatReader | null>(null);

  useEffect(() => {
    codeReader.current = new BrowserMultiFormatReader();
    return () => {
      if (codeReader.current) {
        codeReader.current.reset();
      }
    };
  }, []);

  const startScanning = async () => {
    if (!videoRef.current || !codeReader.current) return;

    try {
      setIsScanning(true);
      setError(null);

      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment' }
      });

      videoRef.current.srcObject = stream;
      videoRef.current.play();

      codeReader.current.decodeFromVideoDevice(null, videoRef.current, (result, error) => {
        if (result) {
          onScanSuccess(result.getText());
          stopScanning();
        }
        if (error && error.name !== 'NotFoundException') {
          console.warn('QR scan error:', error);
        }
      });

    } catch (err: any) {
      const errorMessage = '카메라 접근 권한이 필요합니다.';
      setError(errorMessage);
      onScanError?.(errorMessage);
      setIsScanning(false);
    }
  };

  const stopScanning = () => {
    if (codeReader.current) {
      codeReader.current.reset();
    }
    
    if (videoRef.current && videoRef.current.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream;
      const tracks = stream.getTracks();
      tracks.forEach(track => track.stop());
      videoRef.current.srcObject = null;
    }
    
    setIsScanning(false);
  };

  return (
    <div className="qr-scanner">
      <div className="scanner-container">
        {!isScanning ? (
          <div className="scanner-placeholder">
            <div className="scan-icon">📱</div>
            <p>QR 코드를 스캔하여 스탬프를 획득하세요</p>
            <button 
              className="scan-button"
              onClick={startScanning}
            >
              QR 스캔 시작
            </button>
          </div>
        ) : (
          <div className="video-container">
            <video 
              ref={videoRef}
              className="scanner-video"
              muted
              playsInline
            />
            <div className="scan-overlay">
              <div className="scan-frame"></div>
            </div>
            <button 
              className="stop-button"
              onClick={stopScanning}
            >
              스캔 중지
            </button>
          </div>
        )}
        
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}
      </div>
    </div>
  );
};

export default QRScanner;
