import React from 'react';
import Image from 'next/image';

interface GameCardProps {
  date: string;
  homeTeam: {
    name: string;
    logo: string;
    score: number;
  };
  awayTeam: {
    name: string;
    logo: string;
    score: number;
  };
}

const GameCard: React.FC<GameCardProps> = ({ date, homeTeam, awayTeam }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-4 w-full max-w-sm">
      <div className="text-sm text-gray-500 mb-2">{date}</div>
      <div className="flex justify-between items-center">
        <div className="flex flex-col items-center w-2/5">
          <Image src={homeTeam.logo} alt={homeTeam.name} width={50} height={50} />
          <div className="font-bold mt-2">{homeTeam.name}</div>
          <div className="text-2xl font-bold mt-1">{homeTeam.score}</div>
        </div>
        <div className="text-xl font-bold">VS</div>
        <div className="flex flex-col items-center w-2/5">
          <Image src={awayTeam.logo} alt={awayTeam.name} width={50} height={50} />
          <div className="font-bold mt-2">{awayTeam.name}</div>
          <div className="text-2xl font-bold mt-1">{awayTeam.score}</div>
        </div>
      </div>
    </div>
  );
};

export default GameCard;
