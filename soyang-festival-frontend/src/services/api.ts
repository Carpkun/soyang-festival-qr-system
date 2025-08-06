import axios from 'axios';

// API 기본 설정
// 환경에 따라 API URL 설정
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'https://ccculture.pythonanywhere.com/api'  // PythonAnywhere URL
  : 'http://192.168.0.13:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 타입 정의
export interface Participant {
  id: string;
  nickname: string;
  stamp_count: number;
  is_mission_complete: boolean;
  created_at: string;
  stamps?: Stamp[];
}

export interface Stamp {
  id: number;
  participant: string;
  booth: string;
  booth_name: string;
  created_at: string;
}

export interface CreateStampResponse {
  status: string;
  total_stamps: number;
  is_mission_complete: boolean;
}

export interface Booth {
  id: string;
  name: string;
  description: string;
  is_active: boolean;
  created_at: string;
}

export interface AdminStats {
  total_participants: number;
  total_completions: number;
  booth_popularity: Array<{
    name: string;
    scan_count: number;
  }>;
}

// API 함수들
export const apiService = {
  // 참여자 생성
  createParticipant: async (nickname: string): Promise<Participant> => {
    const response = await api.post('/participants/', { nickname });
    return response.data;
  },

  // 참여자 조회
  getParticipant: async (participantId: string): Promise<Participant> => {
    const response = await api.get(`/participants/${participantId}/`);
    return response.data;
  },

  // 스탬프 생성
  createStamp: async (participantId: string, boothId: string): Promise<CreateStampResponse> => {
    const response = await api.post('/stamps/', {
      participant_id: participantId,
      booth_id: boothId,
    });
    return response.data;
  },

  // 관리자 통계 조회
  getAdminStats: async (): Promise<AdminStats> => {
    const response = await api.get('/admin/stats/');
    return response.data;
  },

  // 모든 참여자 목록 조회
  getAllParticipants: async () => {
    const response = await api.get('/participants/');
    return response.data;
  },

  // 부스별 통계 조회
  getBoothStats: async () => {
    const response = await api.get('/admin/booth-stats/');
    return response.data;
  },

  // 시간대별 통계 조회
  getTimeStats: async () => {
    const response = await api.get('/admin/time-stats/');
    return response.data;
  },

  // 참여자 상세 정보 조회
  getParticipantDetail: async (participantId: string) => {
    const response = await api.get(`/participants/${participantId}/`);
    return response.data;
  },

  // 부스 관련 API
  getBooths: async (): Promise<Booth[]> => {
    const response = await api.get('/booths/');
    return response.data;
  },

  createBooth: async (boothData: Partial<Booth>): Promise<Booth> => {
    const response = await api.post('/booths/', boothData);
    return response.data;
  },

  updateBooth: async (boothId: number, boothData: Partial<Booth>): Promise<Booth> => {
    const response = await api.put(`/booths/${boothId}/`, boothData);
    return response.data;
  },

  deleteBooth: async (boothId: number): Promise<void> => {
    await api.delete(`/booths/${boothId}/`);
  },

  // 스탬프 관련 API
  getParticipantStamps: async (participantId: string): Promise<Stamp[]> => {
    const response = await api.get(`/participants/${participantId}/stamps/`);
    return response.data;
  },
};

export default api;
