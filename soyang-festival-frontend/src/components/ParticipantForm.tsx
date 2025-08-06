import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { apiService } from '../services/api';
import '../styles/ParticipantForm.css';

const ParticipantForm: React.FC = () => {
  const [nickname, setNickname] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!nickname.trim()) {
      setError('닉네임을 입력해주세요.');
      return;
    }

    if (nickname.trim().length < 2) {
      setError('닉네임은 2글자 이상 입력해주세요.');
      return;
    }

    if (nickname.trim().length > 20) {
      setError('닉네임은 20글자 이하로 입력해주세요.');
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      // 참가자 생성 API 호출
      const participant = await apiService.createParticipant(nickname.trim());
      
      // 성공 시 참가자 ID를 localStorage에 저장하고 스탬프 페이지로 이동
      localStorage.setItem('participantId', participant.id);
      localStorage.setItem('participantNickname', participant.nickname);
      
      navigate('/stamps');
    } catch (error) {
      console.error('참가자 생성 실패:', error);
      setError('참가자 등록에 실패했습니다. 다시 시도해주세요.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="participant-form-container">
      <div className="form-header">
        <h1>🎪 소양강문화제</h1>
        <h2>QR 스탬프 랠리</h2>
        <p>8개 부스를 모두 방문하여 스탬프를 모아보세요!</p>
      </div>

      <form onSubmit={handleSubmit} className="participant-form">
        <div className="form-group">
          <label htmlFor="nickname">닉네임</label>
          <input
            type="text"
            id="nickname"
            value={nickname}
            onChange={(e) => setNickname(e.target.value)}
            placeholder="참가자 닉네임을 입력하세요"
            maxLength={20}
            disabled={isLoading}
            className={error ? 'error' : ''}
          />
          {error && <div className="error-message">{error}</div>}
          <div className="input-help">
            2-20글자로 입력해주세요. ({nickname.length}/20)
          </div>
        </div>

        <button 
          type="submit" 
          className="submit-button"
          disabled={isLoading || !nickname.trim()}
        >
          {isLoading ? (
            <>
              <span className="spinner"></span>
              등록 중...
            </>
          ) : (
            <>
              🚀 스탬프 랠리 시작하기
            </>
          )}
        </button>
      </form>

      <div className="info-section">
        <div className="info-card">
          <div className="info-icon">🎯</div>
          <div className="info-content">
            <h3>참여 방법</h3>
            <p>각 부스에서 QR 코드를 스캔하여 스탬프를 모으세요</p>
          </div>
        </div>
        
        <div className="info-card">
          <div className="info-icon">🏆</div>
          <div className="info-content">
            <h3>완주 조건</h3>
            <p>8개 부스를 모두 방문하면 완주 인증서를 받을 수 있어요</p>
          </div>
        </div>
        
        <div className="info-card">
          <div className="info-icon">🎁</div>
          <div className="info-content">
            <h3>완주 혜택</h3>
            <p>완주자에게는 특별한 기념품을 드립니다</p>
          </div>
        </div>
      </div>

      <div className="admin-link">
        <button 
          onClick={() => navigate('/admin')}
          className="admin-button"
        >
          관리자 페이지
        </button>
      </div>
    </div>
  );
};

export default ParticipantForm;
