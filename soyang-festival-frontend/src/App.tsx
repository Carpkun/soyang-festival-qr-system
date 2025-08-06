import { useState } from 'react'
import './App.css'
import NicknameForm from './components/NicknameForm'
import QRScanner from './components/QRScanner'
import { apiService } from './services/api'
import DetailedStampStatus from './components/DetailedStampStatus';
import AdminQRManager from './components/AdminQRManager';

function App() {
  const [participantId, setParticipantId] = useState<string | null>(null)
  const [participantNickname, setParticipantNickname] = useState<string | null>(null)
  const [stamps, setStamps] = useState<any[]>([])
  const [scanMessage, setScanMessage] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<'scan' | 'status'>('scan')
  
  // URL 파라미터에서 관리자 모드 확인
  const isAdminMode = new URLSearchParams(window.location.search).get('admin') === 'true'

  const handleParticipantCreated = (id: string, nickname: string) => {
    setParticipantId(id)
    setParticipantNickname(nickname)
    console.log(`참여자 생성됨: ${nickname} (ID: ${id})`)
  }

  const handleQRScan = async (qrData: string) => {
    if (!participantId) return

    try {
      // QR 데이터에서 부스 ID 추출 (URL 형태 또는 booth_ 형태 모두 지원)
      let boothId = '';
      if (qrData.includes('boothId=')) {
        // URL 형태: https://domain.com/?boothId=123
        const url = new URL(qrData);
        boothId = url.searchParams.get('boothId') || '';
      } else if (qrData.startsWith('booth_')) {
        // 기존 형태: booth_123
        boothId = qrData.replace('booth_', '');
      } else {
        // 그냥 ID 값인 경우
        boothId = qrData;
      }
      
      const response = await apiService.createStamp(participantId, boothId)
      // 실제 스탬프 데이터를 다시 가져오기
      const participantData = await apiService.getParticipant(participantId)
      setStamps(participantData.stamps || [])
      setScanMessage(`🎉 스탬프를 획득했습니다! (${response.total_stamps}개)`)
      
      // 3초 후 메시지 제거
      setTimeout(() => setScanMessage(null), 3000)
      
    } catch (error: any) {
      if (error.response?.data?.error) {
        setScanMessage(`❌ ${error.response.data.error}`)
      } else {
        setScanMessage('❌ 스탬프 획득에 실패했습니다.')
      }
      
      // 3초 후 메시지 제거
      setTimeout(() => setScanMessage(null), 3000)
    }
  }

  return (
    <div className="app">
      {isAdminMode ? (
        <AdminQRManager />
      ) : (!participantId ? (
        <NicknameForm onParticipantCreated={handleParticipantCreated} />
      ) : (
        <div className="main-content">
          <h1>환영합니다, {participantNickname}님!</h1>
          
          {/* 탭 네비게이션 */}
          <div className="tab-navigation">
            <button 
              className={`tab-button ${activeTab === 'scan' ? 'active' : ''}`}
              onClick={() => setActiveTab('scan')}
            >
              📱 QR 스캔
            </button>
            <button 
              className={`tab-button ${activeTab === 'status' ? 'active' : ''}`}
              onClick={() => setActiveTab('status')}
            >
              🏆 스탬프 현황 ({stamps.length}/8)
            </button>
          </div>

          {/* 탭 컨텐츠 */}
          <div className="tab-content">
            {activeTab === 'scan' ? (
              <div className="scan-tab">
                <p>QR 코드를 스캔하여 스탬프를 수집하세요.</p>
                
                {scanMessage && (
                  <div className="scan-message">
                    {scanMessage}
                  </div>
                )}
                
                <QRScanner onScanSuccess={handleQRScan} />
              </div>
            ) : (
              <DetailedStampStatus 
                participantId={participantId!}
                stamps={stamps}
                onRefresh={() => {
                  // 실제 환경에서는 API를 호출하여 스탬프 데이터를 새로고침
                  console.log('스탬프 데이터 새로고침');
                }}
              />
            )}
          </div>
        </div>
      ))}
    </div>
  )
}

export default App
