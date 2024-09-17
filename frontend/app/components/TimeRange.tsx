import React from 'react';

type TimeRangeProps = {
  startTime: number;
  endTime: number;
  isActive: boolean;
  onClick: () => void;
};

const formatTime = (seconds: number): string => {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
};

const TimeRange: React.FC<TimeRangeProps> = ({ startTime, endTime, isActive, onClick }) => {
  const displayStartTime = formatTime(720 - startTime);
  const displayEndTime = formatTime(720 - endTime);

  return (
    <button
      className={`px-2 py-1 rounded ${
        isActive ? 'bg-teamBlue text-white' : 'bg-gray-200 text-gray-800'
      }`}
      onClick={onClick}
    >
      {displayStartTime} - {displayEndTime}
    </button>
  );
};

export default TimeRange;
