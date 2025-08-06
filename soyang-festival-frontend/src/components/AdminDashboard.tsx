import React, { useState, useEffect } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement,
} from 'chart.js';
import { Bar, Doughnut, Line } from 'react-chartjs-2';
import { apiService } from '../services/api';
import '../styles/AdminDashboard.css';

// Chart.js 등록
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PointElement,
  LineElement
);

interface DashboardStats {
  totalParticipants: number;
  totalStamps: number;
  completionRate: number;
  boothStats: Array<{
    booth_id: number;
    booth_name: string;
    stamp_count: number;
  }>;
  timeStats: Array<{
    hour: number;
    participant_count: number;
    stamp_count: number;
  }>;
  recentParticipants: Array<{
    id: string;
    nickname: string;
    stamp_count: number;
    created_at: string;
  }>;
}

const AdminDashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState<Date>(new Date());
  const [error, setError] = useState<string | null>(null);

  const fetchStats = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      // 실제 API 호출
      const adminStats = await apiService.getAdminStats();
      
      // API 데이터를 컴포넌트 인터페이스에 맞게 변환
      const transformedStats: DashboardStats = {
        totalParticipants: adminStats.total_participants || 0,
        totalStamps: 0, // API에서 제공되지 않으므로 계산 필요
        completionRate: adminStats.total_participants > 0 
          ? (adminStats.total_completions / adminStats.total_participants) * 100 
          : 0,
        boothStats: (adminStats.booth_popularity || []).map((booth: any, index: number) => ({
          booth_id: index + 1,
          booth_name: booth.name,
          stamp_count: booth.scan_count
        })),
        timeStats: [], // 시간대별 통계는 별도 API 호출 필요
        recentParticipants: [] // 최근 참여자는 별도 API 호출 필요
      };
      
      // 총 스탬프 수 계산
      transformedStats.totalStamps = transformedStats.boothStats.reduce(
        (sum, booth) => sum + booth.stamp_count, 
        0
      );
      
      setStats(transformedStats);
      setLastUpdated(new Date());
      
    } catch (err) {
      console.error('통계 데이터 로딩 실패:', err);
      setError('통계 데이터를 불러오는데 실패했습니다.');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
    // 30초마다 자동 새로고침
    const interval = setInterval(fetchStats, 30000);
    return () => clearInterval(interval);
  }, []);

  if (isLoading) {
    return (
      <div className="admin-dashboard loading">
        <h2>📊 통계 대시보드</h2>
        <div className="loading-spinner">데이터를 불러오는 중...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="admin-dashboard error">
        <h2>📊 통계 대시보드</h2>
        <div className="error-container">
          <div className="error-message">
            <h3>⚠️ 오류 발생</h3>
            <p>{error}</p>
            <button onClick={fetchStats} className="retry-button">
              🔄 다시 시도
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="admin-dashboard loading">
        <h2>📊 통계 대시보드</h2>
        <div className="loading-spinner">데이터가 없습니다.</div>
      </div>
    );
  }

  // 부스별 인기도 차트 데이터
  const boothChartData = {
    labels: stats.boothStats.map(booth => booth.booth_name.replace(' 부스', '')),
    datasets: [
      {
        label: '스탬프 수집 횟수',
        data: stats.boothStats.map(booth => booth.stamp_count),
        backgroundColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          '#4BC0C0',
          '#9966FF',
          '#FF9F40',
          '#FF6384',
          '#C9CBCF',
        ],
        borderColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          '#4BC0C0',
          '#9966FF',
          '#FF9F40',
          '#FF6384',
          '#C9CBCF',
        ],
        borderWidth: 1,
      },
    ],
  };

  // 완주율 도넛 차트 데이터
  const completionChartData = {
    labels: ['완주자', '미완주자'],
    datasets: [
      {
        data: [
          Math.round((stats.completionRate / 100) * stats.totalParticipants),
          stats.totalParticipants - Math.round((stats.completionRate / 100) * stats.totalParticipants),
        ],
        backgroundColor: ['#28a745', '#dc3545'],
        borderColor: ['#28a745', '#dc3545'],
        borderWidth: 2,
      },
    ],
  };

  // 시간대별 참여 현황 차트 데이터
  const timeChartData = {
    labels: stats.timeStats.map(stat => `${stat.hour}시`),
    datasets: [
      {
        label: '참여자 수',
        data: stats.timeStats.map(stat => stat.participant_count),
        borderColor: '#36A2EB',
        backgroundColor: 'rgba(54, 162, 235, 0.1)',
        tension: 0.4,
      },
      {
        label: '스탬프 획득 수',
        data: stats.timeStats.map(stat => stat.stamp_count),
        borderColor: '#FF6384',
        backgroundColor: 'rgba(255, 99, 132, 0.1)',
        tension: 0.4,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
    },
  };

  return (
    <div className="admin-dashboard">
      <div className="dashboard-header">
        <h2>📊 소양강문화제 실시간 통계</h2>
        <div className="dashboard-controls">
          <div className="last-updated">
            마지막 업데이트: {lastUpdated.toLocaleTimeString('ko-KR')}
          </div>
          <button className="refresh-btn" onClick={fetchStats}>
            🔄 새로고침
          </button>
        </div>
      </div>

      {/* 요약 통계 카드들 */}
      <div className="stats-cards">
        <div className="stat-card">
          <div className="stat-icon">👥</div>
          <div className="stat-content">
            <h3>총 참여자</h3>
            <div className="stat-number">{stats.totalParticipants.toLocaleString()}명</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">🏆</div>
          <div className="stat-content">
            <h3>총 스탬프</h3>
            <div className="stat-number">{stats.totalStamps.toLocaleString()}개</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">✅</div>
          <div className="stat-content">
            <h3>완주율</h3>
            <div className="stat-number">{stats.completionRate}%</div>
          </div>
        </div>
        <div className="stat-card">
          <div className="stat-icon">📈</div>
          <div className="stat-content">
            <h3>평균 스탬프</h3>
            <div className="stat-number">{(stats.totalStamps / stats.totalParticipants).toFixed(1)}개</div>
          </div>
        </div>
      </div>

      {/* 차트 섹션 */}
      <div className="charts-grid">
        <div className="chart-container">
          <h3>부스별 인기도</h3>
          <Bar data={boothChartData} options={chartOptions} />
        </div>
        
        <div className="chart-container">
          <h3>완주 현황</h3>
          <Doughnut data={completionChartData} options={chartOptions} />
        </div>
      </div>

      <div className="chart-container-wide">
        <h3>시간대별 참여 현황</h3>
        <Line data={timeChartData} options={chartOptions} />
      </div>

      {/* 최근 참여자 목록 */}
      <div className="recent-participants">
        <h3>최근 참여자</h3>
        <div className="participants-table">
          <div className="table-header">
            <div>닉네임</div>
            <div>스탬프 수</div>
            <div>참여 시간</div>
            <div>상태</div>
          </div>
          {stats.recentParticipants.map(participant => (
            <div key={participant.id} className="table-row">
              <div className="participant-nickname">{participant.nickname}</div>
              <div className="participant-stamps">{participant.stamp_count}/8</div>
              <div className="participant-time">
                {new Date(participant.created_at).toLocaleTimeString('ko-KR')}
              </div>
              <div className={`participant-status ${participant.stamp_count === 8 ? 'completed' : 'in-progress'}`}>
                {participant.stamp_count === 8 ? '완주' : '진행중'}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
