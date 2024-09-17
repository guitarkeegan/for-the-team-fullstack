import React from 'react';

interface TimeRangeProps {
  startTime: number; // Time in seconds
  endTime: number; // Time in seconds
  isActive: boolean;
  onClick: () => void;
}

const formatTime = (seconds: number): string => {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
};

const TimeRange: React.FC<TimeRangeProps> = ({ startTime, endTime, isActive, onClick }) => {
  return (
    <button
      onClick={onClick}
      className={`
        px-3 py-1 rounded-full
        text-sm font-bold
        transition-all duration-300 ease-in-out
        ${isActive 
          ? 'bg-teamRed text-white shadow-md' 
          : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}
      `}
    >
      {formatTime(startTime)} - {formatTime(endTime)}
    </button>
  );
};

export default TimeRange;
