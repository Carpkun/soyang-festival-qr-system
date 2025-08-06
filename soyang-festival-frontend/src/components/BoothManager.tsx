import React, { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import '../styles/BoothManager.css';

interface Booth {
  id: number;
  name: string;
  description: string;
  location?: string;
  is_active: boolean;
  created_at?: string;
}

const BoothManager: React.FC = () => {
  const [booths, setBooths] = useState<Booth[]>([]);
  const [editingBooth, setEditingBooth] = useState<Booth | null>(null);
  const [showAddForm, setShowAddForm] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState({
    name: '',
    description: '',
    location: '',
    is_active: true
  });

  useEffect(() => {
    fetchBooths();
  }, []);

  const fetchBooths = async () => {
    try {
      setIsLoading(true);
      const data = await apiService.getBooths();
      setBooths(data);
      setError(null);
    } catch (error) {
      console.error('Failed to fetch booths:', error);
      setError('부스 정보를 불러오는데 실패했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      if (editingBooth) {
        // 수정
        await apiService.updateBooth(editingBooth.id, formData);
      } else {
        // 추가
        await apiService.createBooth(formData);
      }
      
      await fetchBooths();
      resetForm();
      setError(null);
    } catch (error) {
      console.error('Failed to save booth:', error);
      setError('부스 저장에 실패했습니다.');
    }
  };

  const handleEdit = (booth: Booth) => {
    setEditingBooth(booth);
    setFormData({
      name: booth.name,
      description: booth.description,
      location: booth.location || '',
      is_active: booth.is_active
    });
    setShowAddForm(true);
  };

  const handleDelete = async (boothId: number) => {
    if (!confirm('정말로 이 부스를 삭제하시겠습니까?')) {
      return;
    }

    try {
      await apiService.deleteBooth(boothId);
      await fetchBooths();
      setError(null);
    } catch (error) {
      console.error('Failed to delete booth:', error);
      setError('부스 삭제에 실패했습니다.');
    }
  };

  const resetForm = () => {
    setFormData({
      name: '',
      description: '',
      location: '',
      is_active: true
    });
    setEditingBooth(null);
    setShowAddForm(false);
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? (e.target as HTMLInputElement).checked : value
    }));
  };

  if (isLoading) {
    return <div className="loading">부스 정보를 불러오는 중...</div>;
  }

  return (
    <div className="booth-manager">
      <div className="booth-manager-header">
        <h3>🏪 부스 관리</h3>
        <button 
          className="add-booth-button"
          onClick={() => setShowAddForm(true)}
        >
          ➕ 새 부스 추가
        </button>
      </div>

      {error && (
        <div className="error-message">
          ⚠️ {error}
        </div>
      )}

      {showAddForm && (
        <div className="booth-form-overlay">
          <div className="booth-form">
            <h4>{editingBooth ? '부스 수정' : '새 부스 추가'}</h4>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="name">부스명 *</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleInputChange}
                  required
                  placeholder="부스명을 입력하세요"
                />
              </div>

              <div className="form-group">
                <label htmlFor="description">설명 *</label>
                <textarea
                  id="description"
                  name="description"
                  value={formData.description}
                  onChange={handleInputChange}
                  required
                  placeholder="부스에 대한 설명을 입력하세요"
                  rows={3}
                />
              </div>

              <div className="form-group">
                <label htmlFor="location">위치</label>
                <input
                  type="text"
                  id="location"
                  name="location"
                  value={formData.location}
                  onChange={handleInputChange}
                  placeholder="부스 위치를 입력하세요 (선택사항)"
                />
              </div>

              <div className="form-group checkbox-group">
                <label>
                  <input
                    type="checkbox"
                    name="is_active"
                    checked={formData.is_active}
                    onChange={handleInputChange}
                  />
                  활성화
                </label>
              </div>

              <div className="form-actions">
                <button type="button" onClick={resetForm} className="cancel-button">
                  취소
                </button>
                <button type="submit" className="submit-button">
                  {editingBooth ? '수정' : '추가'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="booth-list">
        {booths.length === 0 ? (
          <div className="empty-state">
            <p>등록된 부스가 없습니다.</p>
            <p>새 부스를 추가해보세요!</p>
          </div>
        ) : (
          booths.map(booth => (
            <div key={booth.id} className={`booth-item ${!booth.is_active ? 'inactive' : ''}`}>
              <div className="booth-info">
                <div className="booth-header">
                  <h4>{booth.name}</h4>
                  <div className="booth-status">
                    {booth.is_active ? (
                      <span className="status-active">🟢 활성</span>
                    ) : (
                      <span className="status-inactive">🔴 비활성</span>
                    )}
                  </div>
                </div>
                <p className="booth-description">{booth.description}</p>
                {booth.location && (
                  <p className="booth-location">📍 {booth.location}</p>
                )}
                {booth.created_at && (
                  <p className="booth-created">
                    생성일: {new Date(booth.created_at).toLocaleDateString('ko-KR')}
                  </p>
                )}
              </div>
              <div className="booth-actions">
                <button
                  className="edit-button"
                  onClick={() => handleEdit(booth)}
                >
                  ✏️ 수정
                </button>
                <button
                  className="delete-button"
                  onClick={() => handleDelete(booth.id)}
                >
                  🗑️ 삭제
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default BoothManager;
