import React from 'react';

interface StampStatusProps {
  stamps: any[];
  totalBooths: number;
}

const StampStatus: React.FC<StampStatusProps> = ({ stamps, totalBooths }) => {
  const collectedIds = stamps.map(stamp => stamp.booth_id);

  return (
    <div className="stamp-status">
      <h2>스탬프 현황</h2>
      <ul>
        {[...Array(totalBooths).keys()].map(boothId => (
          <li key={boothId} className={collectedIds.includes(boothId) ? 'collected' : 'not-collected'}>
            {collectedIds.includes(boothId) ? `✅ 부스 ${boothId + 1} - 획득!` : `❌ 부스 ${boothId + 1} - 미획득`}
          </li>
        ))}
      </ul>
      <div className="progress">
        <div className="progress-bar" style={{ width: `${(stamps.length / totalBooths) * 100}%` }}>
          {stamps.length} / {totalBooths}
        </div>
      </div>
    </div>
  );
};

export default StampStatus;

