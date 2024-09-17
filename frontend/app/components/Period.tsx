import React from 'react';

interface PeriodProps {
  number: number;
  isActive: boolean;
  onClick: () => void;
}

const Period: React.FC<PeriodProps> = ({ number, isActive, onClick }) => {
  return (
    <button
      onClick={onClick}
      className={`
        w-16 h-16 rounded-full
        flex items-center justify-center
        text-2xl font-bold font-heading
        transition-all duration-300 ease-in-out
        ${isActive 
          ? 'bg-teamRed text-white shadow-lg scale-110' 
          : 'bg-orange-200 text-orange-800 hover:bg-orange-300'}
        border-4 border-orange-700
        relative overflow-hidden
      `}
    >
      <span className="z-10">{number}</span>
      {/* Basketball lines */}
      <div className="absolute w-full h-0.5 bg-orange-700 top-1/2 transform -translate-y-1/2"></div>
      <div className="absolute w-0.5 h-full bg-orange-700 left-1/2 transform -translate-x-1/2"></div>
      <div className="absolute w-full h-full border-2 border-orange-700 rounded-full"></div>
    </button>
  );
};

export default Period;
