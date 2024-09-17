import React from 'react';

interface GameCardProps {
  date: string;
  homeTeam: {
    name: string;
    score: number;
  };
  awayTeam: {
    name: string;
    score: number;
  };
}

const GameCard: React.FC<GameCardProps> = ({ date, homeTeam, awayTeam }) => {
  return (
    <section className="bg-white rounded-lg shadow-md p-4 w-full max-w-sm">
      <div className="text-sm font-sans font-bold text-gray-500 mb-2">{date}</div>
      <div className="flex justify-between items-center">
        <div className="flex flex-col items-center w-2/5 text-gray-700">
          <div className="font-bold text-lg">{homeTeam.name}</div>
          <div className="text-2xl font-bold mt-1">{homeTeam.score}</div>
        </div>
        <div className="text-xl font-bold text-gray-700">VS</div>
        <div className="flex flex-col items-center w-2/5 text-gray-700">
          <div className="font-bold text-lg">{awayTeam.name}</div>
          <div className="text-2xl font-bold mt-1">{awayTeam.score}</div>
        </div>
      </div>
    </section>
  );
};

export default GameCard;
