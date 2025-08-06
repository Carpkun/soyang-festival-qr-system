import React, { useState } from 'react';
import { apiService } from '../services/api';

interface NicknameFormProps {
  onParticipantCreated: (participantId: string, nickname: string) => void;
}

const NicknameForm: React.FC<NicknameFormProps> = ({ onParticipantCreated }) => {
  const [nickname, setNickname] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!nickname.trim()) {
      setError('닉네임을 입력해주세요.');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const participant = await apiService.createParticipant(nickname.trim());
      
      // localStorage에 참여자 정보 저장
      localStorage.setItem('participantId', participant.id);
      localStorage.setItem('participantNickname', participant.nickname);
      
      onParticipantCreated(participant.id, participant.nickname);
    } catch (err: any) {
      if (err.response?.data?.error) {
        setError(err.response.data.error);
      } else {
        setError('참여자 등록 중 오류가 발생했습니다.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="nickname-form-container">
      <div className="nickname-form">
        <h1>소양강문화제 QR 스탬프 랠리</h1>
        <p>스탬프를 모아서 상품을 받아보세요!</p>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="nickname">닉네임을 입력하세요</label>
            <input
              type="text"
              id="nickname"
              value={nickname}
              onChange={(e) => setNickname(e.target.value)}
              placeholder="예: 춘천사는반달곰"
              maxLength={50}
              disabled={isLoading}
            />
          </div>
          
          {error && <div className="error-message">{error}</div>}
          
          <button type="submit" disabled={isLoading}>
            {isLoading ? '등록 중...' : '시작하기'}
          </button>
        </form>
      </div>
    </div>
  );
};

export default NicknameForm;
