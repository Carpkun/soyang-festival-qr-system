import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import type { Booth } from '../services/api';

interface DetailedStampStatusProps {
  participantId: string;
  stamps: any[];
  onRefresh?: () => void;
}

const DetailedStampStatus: React.FC<DetailedStampStatusProps> = ({ 
  stamps, 
  onRefresh 
}) => {
  const [booths, setBooths] = useState<Booth[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchBooths = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const boothsData = await apiService.getBooths();
      setBooths(boothsData);
    } catch (err) {
      console.error('부스 데이터 로딩 실패:', err);
      setError('부스 정보를 불러오는데 실패했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchBooths();
  }, []);

  const getStampForBooth = (boothId: string) => {
    return stamps.find(stamp => stamp.booth === boothId);
  };

  const completionRate = (stamps.length / booths.length) * 100;
  const isCompleted = stamps.length === booths.length;

  if (isLoading) {
    return <div className="loading">부스 정보를 불러오는 중...</div>;
  }

  if (error) {
    return (
      <div className="error-container">
        <div className="error-message">
          <h3>⚠️ 오류 발생</h3>
          <p>{error}</p>
          <button onClick={fetchBooths} className="retry-button">
            🔄 다시 시도
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="detailed-stamp-status">
      <div className="status-header">
        <h2>🎪 스탬프 수집 현황</h2>
        <div className="completion-info">
          <div className="progress-circle">
            <svg width="120" height="120" viewBox="0 0 120 120">
              <circle
                cx="60"
                cy="60"
                r="50"
                fill="none"
                stroke="#e5e5e5"
                strokeWidth="8"
              />
              <circle
                cx="60"
                cy="60"
                r="50"
                fill="none"
                stroke="#007bff"
                strokeWidth="8"
                strokeDasharray={`${completionRate * 3.14} 314`}
                strokeDashoffset="0"
                transform="rotate(-90 60 60)"
                className="progress-ring"
              />
              <text x="60" y="65" textAnchor="middle" className="progress-text">
                {Math.round(completionRate)}%
              </text>
            </svg>
          </div>
          <div className="completion-text">
            <h3>{stamps.length} / {booths.length}</h3>
            <p>스탬프 수집 완료</p>
            {isCompleted && (
              <div className="completion-badge">
                🎉 전체 완주!
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="booth-grid">
        {booths.map(booth => {
          const stamp = getStampForBooth(booth.id);
          const isCollected = !!stamp;
          
          return (
            <div 
              key={booth.id} 
              className={`booth-card ${isCollected ? 'collected' : 'not-collected'}`}
            >
              <div className="booth-header">
                <div className="booth-number">부스 {booth.id}</div>
                <div className="stamp-icon">
                  {isCollected ? '✅' : '⭕'}
                </div>
              </div>
              <div className="booth-content">
                <h4>{booth.name}</h4>
                <p>{booth.description}</p>
                {isCollected && stamp && (
                  <div className="stamp-info">
                    <small>획득 시간: {new Date(stamp.created_at).toLocaleString('ko-KR')}</small>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {isCompleted && (
        <div className="completion-message">
          <h3>🎊 축하합니다!</h3>
          <p>모든 스탬프를 수집하셨습니다!</p>
          <p>기념품 부스에서 상품을 받아가세요!</p>
        </div>
      )}
      
      <button 
        className="refresh-button" 
        onClick={onRefresh}
      >
        🔄 새로고침
      </button>
    </div>
  );
};

export default DetailedStampStatus;
