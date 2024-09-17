import React from 'react';

interface GameCardProps {
  id: string;
  date: string;
  homeTeam?: { name: string; score: number };
  awayTeam?: { name: string; score: number };
  onClick?: () => void;
}

const GameCard: React.FC<GameCardProps> = ({ id, date, homeTeam, awayTeam, onClick }) => {
  if (!homeTeam || !awayTeam) {
    return (
      <div className="bg-red-100 p-4 rounded-lg">
        Error: Incomplete game data for game {id}
      </div>
    );
  }

  return (
    <div 
      className="bg-white p-4 rounded-lg shadow-md cursor-pointer hover:shadow-lg transition-shadow duration-300"
      onClick={onClick}
    >
      <div className="text-sm text-gray-500 mb-2">{date}</div>
      <div className="flex justify-between items-center">
        <div className="text-lg font-semibold">{homeTeam.name}</div>
        <div className="text-xl font-bold">{homeTeam.score}</div>
      </div>
      <div className="flex justify-between items-center mt-2">
        <div className="text-lg font-semibold">{awayTeam.name}</div>
        <div className="text-xl font-bold">{awayTeam.score}</div>
      </div>
    </div>
  );
};

export default GameCard;

