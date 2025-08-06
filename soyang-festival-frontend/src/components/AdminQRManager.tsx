import React, { useState, useEffect } from 'react';
import QRCodeGenerator from './QRCodeGenerator';
import AdminDashboard from './AdminDashboard';
import BoothManager from './BoothManager';
import { apiService } from '../services/api';
import '../styles/AdminQRManager.css';

interface Booth {
  id: string;
  name: string;
  description: string;
}

const AdminQRManager: React.FC = () => {
  const [selectedBooth, setSelectedBooth] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'booths' | 'qr' | 'dashboard'>('booths');
  const [booths, setBooths] = useState<Booth[]>([]);

  useEffect(() => {
    fetchBooths();
  }, []);

  const fetchBooths = async () => {
    try {
      const data = await apiService.getBooths();
      setBooths(data);
    } catch (error) {
      console.error('Failed to fetch booths:', error);
    }
  };

  const handlePrintQR = (boothId: string) => {
    const printWindow = window.open('', '', 'height=600,width=800');
    const booth = booths.find(b => b.id === boothId);
    
    if (printWindow && booth) {
      printWindow.document.write(`
        <html>
          <head>
            <title>${booth.name} QR 코드</title>
            <style>
              body { 
                font-family: Arial, sans-serif; 
                text-align: center; 
                padding: 20px;
                margin: 0;
              }
              .qr-print-container {
                border: 2px solid #333;
                padding: 20px;
                margin: 20px auto;
                max-width: 400px;
                border-radius: 10px;
              }
              h1 { color: #333; margin-bottom: 10px; }
              h2 { color: #666; margin-bottom: 20px; }
              .qr-code { margin: 20px 0; }
              .info { margin-top: 15px; font-size: 14px; color: #666; }
              .footer { margin-top: 30px; font-size: 12px; color: #999; }
            </style>
          </head>
          <body>
            <div class="qr-print-container">
              <h1>소양강문화제</h1>
              <h2>${booth.name}</h2>
              <div class="qr-code" id="qr-container"></div>
              <div class="info">
                <p><strong>부스 ID:</strong> ${booth.id}</p>
                <p><strong>설명:</strong> ${booth.description}</p>
                <p><strong>QR 데이터:</strong> https://ccculture.pythonanywhere.com/?boothId=${booth.id}</p>
              </div>
              <div class="footer">
                <p>QR 코드를 스캔하여 스탬프를 획득하세요!</p>
              </div>
            </div>
          </body>
        </html>
      `);
      
      // QR 코드를 생성하여 삽입
      import('react-qr-code').then(() => {
        // 실제 구현에서는 QR 코드를 이미지로 변환하여 삽입
        const qrContainer = printWindow.document.getElementById('qr-container');
        if (qrContainer) {
          qrContainer.innerHTML = `<canvas id="qr-canvas"></canvas>`;
          // Canvas를 사용하여 QR 코드 그리기 (여기서는 간단히 텍스트로 표시)
          qrContainer.innerHTML = `<div style="border: 1px solid #ccc; padding: 20px; background: #f9f9f9;">QR 코드 영역<br/>https://ccculture.pythonanywhere.com/?boothId=${booth.id}</div>`;
        }
      });
      
      printWindow.document.close();
      setTimeout(() => {
        printWindow.print();
      }, 500);
    }
  };

  const handlePrintAll = () => {
    const printWindow = window.open('', '', 'height=800,width=1000');
    
    if (printWindow) {
      printWindow.document.write(`
        <html>
          <head>
            <title>소양강문화제 - 전체 QR 코드</title>
            <style>
              body { 
                font-family: Arial, sans-serif; 
                padding: 20px;
                margin: 0;
              }
              .header { text-align: center; margin-bottom: 30px; }
              .qr-grid { 
                display: grid; 
                grid-template-columns: repeat(2, 1fr); 
                gap: 20px; 
                max-width: 800px;
                margin: 0 auto;
              }
              .qr-item {
                border: 2px solid #333;
                padding: 15px;
                text-align: center;
                border-radius: 8px;
                page-break-inside: avoid;
              }
              .qr-item h3 { margin: 0 0 10px 0; font-size: 16px; }
              .qr-item p { margin: 5px 0; font-size: 12px; color: #666; }
              .qr-placeholder { 
                border: 1px solid #ccc; 
                padding: 15px; 
                background: #f9f9f9;
                margin: 10px 0;
                font-size: 12px;
              }
              @media print {
                .qr-grid { grid-template-columns: repeat(2, 1fr); }
              }
            </style>
          </head>
          <body>
            <div class="header">
              <h1>소양강문화제 QR 코드 모음</h1>
              <p>각 부스에서 사용할 QR 코드입니다</p>
            </div>
            <div class="qr-grid">
              ${booths.map(booth => `
                <div class="qr-item">
                  <h3>${booth.name}</h3>
                  <div class="qr-placeholder">QR 코드 영역<br/>https://ccculture.pythonanywhere.com/?boothId=${booth.id}</div>
                  <p><strong>부스 ID:</strong> ${booth.id}</p>
                  <p>${booth.description}</p>
                  <p><strong>QR 데이터:</strong> https://ccculture.pythonanywhere.com/?boothId=${booth.id}</p>
                </div>
              `).join('')}
            </div>
          </body>
        </html>
      `);
      
      printWindow.document.close();
      setTimeout(() => {
        printWindow.print();
      }, 500);
    }
  };

  return (
    <div className="admin-qr-manager">
      <div className="admin-header">
        <h2>관리자 패널</h2>
        <div className="tab-navigation">
          <button 
            className={`tab-button ${activeTab === 'booths' ? 'active' : ''}`} 
            onClick={() => setActiveTab('booths')}
          >
            부스 관리
          </button>
          <button 
            className={`tab-button ${activeTab === 'qr' ? 'active' : ''}`} 
            onClick={() => setActiveTab('qr')}
          >
            QR 코드 관리
          </button>
          <button 
            className={`tab-button ${activeTab === 'dashboard' ? 'active' : ''}`} 
            onClick={() => setActiveTab('dashboard')}
          >
            관리자 대시보드
          </button>
        </div>
      </div>

      {activeTab === 'booths' && (
        <BoothManager />
      )}

      {activeTab === 'qr' && (
        <div className="qr-tab-content">
          <div className="qr-tab-header">
            <h3>🎪 부스별 QR 코드 관리</h3>
            <p>각 부스의 QR 코드를 생성하고 출력할 수 있습니다.</p>
            <button className="print-all-button" onClick={handlePrintAll}>
              🖨️ 전체 QR 코드 출력
            </button>
          </div>

          <div className="booth-list">
            {booths.map(booth => (
              <div key={booth.id} className="booth-item">
                <div className="booth-info">
                  <h3>{booth.name}</h3>
                  <p>{booth.description}</p>
                  <div className="booth-controls">
                    <button 
                      className={`view-qr-button ${selectedBooth === booth.id ? 'active' : ''}`}
                      onClick={() => setSelectedBooth(selectedBooth === booth.id ? null : booth.id)}
                    >
                      {selectedBooth === booth.id ? '🔽 QR 숨기기' : '👁️ QR 보기'}
                    </button>
                    <button 
                      className="print-qr-button"
                      onClick={() => handlePrintQR(booth.id)}
                    >
                      🖨️ 출력
                    </button>
                  </div>
                </div>
                
                {selectedBooth === booth.id && (
                  <div className="qr-display">
                    <QRCodeGenerator boothId={booth.id} boothName={booth.name} />
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {activeTab === 'dashboard' && (
        <AdminDashboard />
      )}
    </div>
  );
};

export default AdminQRManager;
